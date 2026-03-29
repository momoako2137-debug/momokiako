"""
中核的感情欲求①〜⑤のサブアイテムを第3〜7回に移動する
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'

# 移動先の親アイテムID（確認済み）
TARGET_PARENTS = {
    '①': '332b5cff-9317-8125-be1b-d0939b94dc0b',  # 第3回
    '②': '332b5cff-9317-8150-8d74-f420f67f40dd',  # 第4回
    '③': '332b5cff-9317-8114-9929-d94ba66c3172',  # 第5回
    '④': '332b5cff-9317-818d-87f5-ef767d93ac91',  # 第6回
    '⑤': '332b5cff-9317-81ae-a3dc-fa08a1054e98',  # 第7回
}


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


def update_parent(page_id, new_parent_id):
    r = requests.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=HEADERS,
        json={
            'properties': {
                '親アイテム': {'relation': [{'id': new_parent_id}]}
            }
        }
    )
    return r.status_code == 200


if __name__ == '__main__':
    SESSION_NAMES = {
        '332b5cff-9317-8125-be1b-d0939b94dc0b': '第3回',
        '332b5cff-9317-8150-8d74-f420f67f40dd': '第4回',
        '332b5cff-9317-8114-9929-d94ba66c3172': '第5回',
        '332b5cff-9317-818d-87f5-ef767d93ac91': '第6回',
        '332b5cff-9317-81ae-a3dc-fa08a1054e98': '第7回',
    }

    print('サブアイテムを取得中...')
    items = get_all_subitems()

    for item in items:
        title = item['title']
        if '中核的感情欲求' not in title:
            continue
        # 「中核的感情欲求」の直後の番号で判定
        import re
        m = re.search(r'中核的感情欲求([①②③④⑤])', title)
        if not m:
            continue
        num = m.group(1)
        target_parent = TARGET_PARENTS.get(num)
        target_num = num
        if not target_parent:
            continue
        if not target_parent:
            continue  # 「中核的感情欲求とは」など番号なしはスキップ

        target_name = SESSION_NAMES.get(target_parent, target_parent)
        if update_parent(item['id'], target_parent):
            print(f'OK: 「{title}」→ {target_name}')
        else:
            print(f'NG: 「{title}」')

    print('\n完了！Notionを確認してください。')
