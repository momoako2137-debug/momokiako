"""
Notion接続テスト＆カリキュラム管理データベース作成
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}


def search_pages():
    """アクセス可能なページを検索してIDを返す"""
    response = requests.post(
        'https://api.notion.com/v1/search',
        headers=HEADERS,
        json={'query': 'セルフケア講座'}
    )
    if response.status_code == 200:
        results = response.json().get('results', [])
        for r in results:
            title = r.get('properties', {}).get('title', {}).get('title', [])
            if title and 'セルフケア講座 管理' in title[0]['plain_text']:
                return r['id']
    return None


def create_curriculum_database(parent_page_id):
    """カリキュラム管理データベースを作成"""
    data = {
        'parent': {'type': 'page_id', 'page_id': parent_page_id},
        'title': [{'type': 'text', 'text': {'content': 'カリキュラム管理'}}],
        'properties': {
            '回': {
                'title': {}
            },
            'タイトル': {
                'rich_text': {}
            },
            '動画①': {
                'rich_text': {}
            },
            '動画②': {
                'rich_text': {}
            },
            '動画③': {
                'rich_text': {}
            },
            'ワーク': {
                'rich_text': {}
            },
            '中間週内容': {
                'rich_text': {}
            },
            'ステータス': {
                'select': {
                    'options': [
                        {'name': '準備中', 'color': 'gray'},
                        {'name': '制作中', 'color': 'yellow'},
                        {'name': '完成', 'color': 'green'},
                        {'name': '配信済み', 'color': 'blue'},
                    ]
                }
            },
        }
    }

    response = requests.post(
        'https://api.notion.com/v1/databases',
        headers=HEADERS,
        json=data
    )

    if response.status_code == 200:
        db = response.json()
        print(f'データベース作成完了: {db["id"]}')
        return db['id']
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)
        return None


def add_curriculum_rows(db_id):
    """カリキュラムの行を追加"""
    sessions = [
        {'回': '第1回', 'タイトル': '「私を大切にする」ということ'},
        {'回': '第2回', 'タイトル': 'ストレスと上手につきあう'},
        {'回': '第3回', 'タイトル': '生きづらさとは（スキーマ療法）'},
        {'回': '第4回', 'タイトル': '自分は自分で守る（認知行動療法）心の境界線'},
        {'回': '第5回', 'タイトル': '幸せのつくり方'},
        {'回': '第6回', 'タイトル': '「対話」は万能薬'},
        {'回': '第7回', 'タイトル': '困った時の簡単で効果的なスキル'},
        {'回': '第8回', 'タイトル': '未来の私のために'},
        {'回': '第9回', 'タイトル': '（準備中）'},
        {'回': '第10回', 'タイトル': '（準備中）'},
    ]

    for s in sessions:
        data = {
            'parent': {'database_id': db_id},
            'properties': {
                '回': {
                    'title': [{'type': 'text', 'text': {'content': s['回']}}]
                },
                'タイトル': {
                    'rich_text': [{'type': 'text', 'text': {'content': s['タイトル']}}]
                },
                'ステータス': {
                    'select': {'name': '準備中'}
                }
            }
        }
        response = requests.post(
            'https://api.notion.com/v1/pages',
            headers=HEADERS,
            json=data
        )
        if response.status_code == 200:
            print(f'追加: {s["回"]} {s["タイトル"]}')
        else:
            print(f'エラー ({s["回"]}): {response.status_code}')

if __name__ == '__main__':
    print('Notionに接続中...')
    page_id = '332b5cff-9317-80a7-862b-e0fb3469ea9e'

    print(f'ページID取得: {page_id}')
    print('データベースを作成中...')
    db_id = create_curriculum_database(page_id)

    if db_id:
        print('カリキュラム行を追加中...')
        add_curriculum_rows(db_id)
        print('\n完了！Notionを確認してください。')
