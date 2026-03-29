"""
Notionのカリキュラムを更新するスクリプト
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'

NEW_TITLES = {
    '第7回': '関係を作る〜安心できるつながりの土台〜',
    '第8回': '問題を整理する〜ブリーフセラピーで見えてくること〜',
    '第9回': '解決策を導く〜思春期対応 作戦会議〜',
    '第10回': '未来の私のために（まとめ）',
}


def get_all_pages():
    response = requests.post(
        f'https://api.notion.com/v1/databases/{DB_ID}/query',
        headers=HEADERS,
        json={}
    )
    return response.json().get('results', [])


def update_page_title(page_id, new_title):
    data = {
        'properties': {
            'タイトル': {
                'rich_text': [{'type': 'text', 'text': {'content': new_title}}]
            }
        }
    }
    response = requests.patch(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=HEADERS,
        json=data
    )
    return response.status_code == 200


if __name__ == '__main__':
    print('Notionのカリキュラムを更新中...')
    pages = get_all_pages()

    for page in pages:
        kai = page['properties']['回']['title']
        if not kai:
            continue
        kai_text = kai[0]['plain_text']
        if kai_text in NEW_TITLES:
            new_title = NEW_TITLES[kai_text]
            success = update_page_title(page['id'], new_title)
            status = 'OK' if success else 'NG'
            print(f'{status} {kai_text}: {new_title}')

    print('\n完了！')
