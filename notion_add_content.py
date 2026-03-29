"""
Notionカリキュラムに第0回を追加し、各回のページに詳細テンプレートを入れる
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'

# 各回の内容テンプレート
SESSIONS = [
    {
        '回': '第0回',
        'タイトル': 'オリエンテーション',
        '動画①': 'AIを味方にするために（既存動画）',
        '動画②': 'この講座の使い方・傾聴AIの渡し方',
        '動画③': '',
        'ワーク': '傾聴AIに今の気持ち・モヤモヤを話してみる',
        '中間週内容': '傾聴AI使ってみた感想・質問受付',
    },
    {
        '回': '第1回',
        'タイトル': '「私を大切にする」ということ',
        '動画①': '疲れない脳と身体を戦略的につくる（睡眠・軽い動き・からだの声）',
        '動画②': '自分らしさって何だろう',
        '動画③': '中核的感情欲求①安心して感情を表現したい',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第2回',
        'タイトル': 'ストレスと上手につきあう',
        '動画①': 'ストレスに気づく・自動思考をつかまえる',
        '動画②': '「捉え方」の構造・心の応急処置',
        '動画③': 'ネガティブな気持ちを抱えて生きる／中核的感情欲求②ありのままを愛してほしい',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第3回',
        'タイトル': '生きづらさとは（スキーマ療法）',
        '動画①': '中核的感情欲求とは',
        '動画②': '自分で安心をつくる・自分が自分の味方になる',
        '動画③': '中核的感情欲求③自律性のある人間になりたい',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第4回',
        'タイトル': '自分は自分で守る・心の境界線（CBT）',
        '動画①': '生きづらさを手放す・捉え方を変える',
        '動画②': 'ぐるぐる思考を手放す',
        '動画③': '中核的感情欲求④有能な自分になりたい',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第5回',
        'タイトル': '幸せのつくり方',
        '動画①': '幸せは自分でつくる',
        '動画②': '',
        '動画③': '中核的感情欲求⑤自由にのびのび遊びたい',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第6回',
        'タイトル': '「対話」は万能薬',
        '動画①': '「孤独」について',
        '動画②': '心の病気について・専門家につながる勇気',
        '動画③': '',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第7回',
        'タイトル': '関係を作る〜安心できるつながりの土台〜',
        '動画①': '',
        '動画②': '',
        '動画③': '',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第8回',
        'タイトル': '問題を整理する〜ブリーフセラピーで見えてくること〜',
        '動画①': '',
        '動画②': '',
        '動画③': '',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第9回',
        'タイトル': '解決策を導く〜思春期対応 作戦会議〜',
        '動画①': '',
        '動画②': '',
        '動画③': '',
        'ワーク': '',
        '中間週内容': '',
    },
    {
        '回': '第10回',
        'タイトル': '未来の私のために（まとめ）',
        '動画①': '',
        '動画②': '',
        '動画③': '',
        'ワーク': '',
        '中間週内容': '',
    },
]


def get_existing_pages():
    response = requests.post(
        f'https://api.notion.com/v1/databases/{DB_ID}/query',
        headers=HEADERS,
        json={}
    )
    pages = response.json().get('results', [])
    existing = {}
    for p in pages:
        kai = p['properties']['回']['title']
        if kai:
            existing[kai[0]['plain_text']] = p['id']
    return existing


def update_page(page_id, session):
    props = {}
    for field in ['タイトル', '動画①', '動画②', '動画③', 'ワーク', '中間週内容']:
        if session.get(field):
            props[field] = {
                'rich_text': [{'type': 'text', 'text': {'content': session[field]}}]
            }
    if props:
        requests.patch(
            f'https://api.notion.com/v1/pages/{page_id}',
            headers=HEADERS,
            json={'properties': props}
        )


def create_page(session):
    data = {
        'parent': {'database_id': DB_ID},
        'properties': {
            '回': {
                'title': [{'type': 'text', 'text': {'content': session['回']}}]
            },
            'タイトル': {
                'rich_text': [{'type': 'text', 'text': {'content': session['タイトル']}}]
            },
            'ステータス': {'select': {'name': '準備中'}}
        }
    }
    for field in ['動画①', '動画②', '動画③', 'ワーク', '中間週内容']:
        if session.get(field):
            data['properties'][field] = {
                'rich_text': [{'type': 'text', 'text': {'content': session[field]}}]
            }
    requests.post('https://api.notion.com/v1/pages', headers=HEADERS, json=data)


if __name__ == '__main__':
    print('既存ページを確認中...')
    existing = get_existing_pages()

    for session in SESSIONS:
        kai = session['回']
        if kai in existing:
            update_page(existing[kai], session)
            print(f'更新: {kai} {session["タイトル"]}')
        else:
            create_page(session)
            print(f'追加: {kai} {session["タイトル"]}')

    print('\n完了！Notionを確認してください。')
