"""
重複したサブアイテムを削除する
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'


def get_all_pages():
    results = []
    cursor = None
    while True:
        body = {'page_size': 100}
        if cursor:
            body['start_cursor'] = cursor
        r = requests.post(
            f'https://api.notion.com/v1/databases/{DB_ID}/query',
            headers=HEADERS,
            json=body
        )
        data = r.json()
        results.extend(data.get('results', []))
        if not data.get('has_more'):
            break
        cursor = data.get('next_cursor')
    return results


def archive_page(page_id):
    r = requests.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=HEADERS,
        json={'archived': True}
    )
    return r.status_code == 200


if __name__ == '__main__':
    print('全ページを取得中...')
    pages = get_all_pages()

    # サブアイテムのみ（親アイテムがある）を抽出
    subitems = []
    for p in pages:
        parent_rel = p['properties'].get('親アイテム', {}).get('relation', [])
        if parent_rel:
            title = p['properties']['回']['title']
            title_text = title[0]['plain_text'] if title else ''
            parent_id = parent_rel[0]['id']
            subitems.append({
                'id': p['id'],
                'title': title_text,
                'parent_id': parent_id,
            })

    print(f'サブアイテム数: {len(subitems)}')

    # 重複を検出（同じtitle + 同じparent_id）
    seen = {}
    duplicates = []
    for item in subitems:
        key = f"{item['parent_id']}_{item['title']}"
        if key in seen:
            duplicates.append(item['id'])
        else:
            seen[key] = item['id']

    print(f'重複数: {len(duplicates)}')

    # 重複を削除
    for page_id in duplicates:
        if archive_page(page_id):
            print(f'削除: {page_id}')
        else:
            print(f'失敗: {page_id}')

    print('\n完了！Notionを確認してください。')
