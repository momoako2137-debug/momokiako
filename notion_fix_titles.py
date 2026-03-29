"""
サブアイテムのタイトルから「動画」を削除する
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'


def get_all_subitems():
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
        for p in data.get('results', []):
            parent_rel = p['properties'].get('親アイテム', {}).get('relation', [])
            if parent_rel:
                title = p['properties']['回']['title']
                title_text = title[0]['plain_text'] if title else ''
                results.append({'id': p['id'], 'title': title_text})
        if not data.get('has_more'):
            break
        cursor = data.get('next_cursor')
    return results


def update_title(page_id, new_title):
    r = requests.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=HEADERS,
        json={
            'properties': {
                '回': {'title': [{'text': {'content': new_title}}]}
            }
        }
    )
    return r.status_code == 200


if __name__ == '__main__':
    print('サブアイテムを取得中...')
    items = get_all_subitems()

    for item in items:
        title = item['title']
        if title.startswith('動画'):
            new_title = title.replace('動画', '', 1).strip()
            if update_title(item['id'], new_title):
                print(f'更新: 「{title}」→「{new_title}」')

    print('\n完了！')
