"""
各回にサブアイテム（動画①②③・ワーク・中間週）を追加する
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'
PARENT_PROP = '親アイテム'

SUBITEMS = {
    '第0回': ['動画① AIを味方にするために', '動画② この講座の使い方・傾聴AI', 'ワーク', '中間週'],
    '第1回': ['動画① 疲れない脳と身体を戦略的につくる', '動画② 自分らしさって何だろう', '動画③ 中核的感情欲求①安心して感情を表現したい', 'ワーク', '中間週'],
    '第2回': ['動画① ストレスに気づく・自動思考をつかまえる', '動画② 捉え方の構造・心の応急処置', '動画③ ネガティブな気持ちを抱えて生きる', 'ワーク', '中間週'],
    '第3回': ['動画① 中核的感情欲求とは', '動画② 自分で安心をつくる・自分の味方になる', '動画③ 中核的感情欲求③自律性のある人間になりたい', 'ワーク', '中間週'],
    '第4回': ['動画① 生きづらさを手放す・捉え方を変える', '動画② ぐるぐる思考を手放す', '動画③ 中核的感情欲求④有能な自分になりたい', 'ワーク', '中間週'],
    '第5回': ['動画① 幸せは自分でつくる', '動画② （準備中）', '動画③ 中核的感情欲求⑤自由にのびのび遊びたい', 'ワーク', '中間週'],
    '第6回': ['動画① 「孤独」について', '動画② 心の病気について・専門家につながる勇気', '動画③ （準備中）', 'ワーク', '中間週'],
    '第7回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）', 'ワーク', '中間週'],
    '第8回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）', 'ワーク', '中間週'],
    '第9回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）', 'ワーク', '中間週'],
    '第10回': ['動画① （準備中）', '動画② （準備中）', 'ワーク', '中間週'],
}


def get_all_pages():
    response = requests.post(
        f'https://api.notion.com/v1/databases/{DB_ID}/query',
        headers=HEADERS,
        json={}
    )
    pages = response.json().get('results', [])
    result = {}
    for p in pages:
        kai = p['properties']['回']['title']
        if kai:
            result[kai[0]['plain_text']] = p['id']
    return result


def add_subitem(parent_id, title):
    data = {
        'parent': {'database_id': DB_ID},
        'properties': {
            '回': {'title': [{'text': {'content': title}}]},
            PARENT_PROP: {'relation': [{'id': parent_id}]},
        }
    }
    r = requests.post('https://api.notion.com/v1/pages', headers=HEADERS, json=data)
    return r.status_code == 200


if __name__ == '__main__':
    print('ページ一覧を取得中...')
    pages = get_all_pages()

    for kai, subitems in SUBITEMS.items():
        if kai not in pages:
            print(f'-- {kai}: 見つかりません')
            continue
        parent_id = pages[kai]
        ok_count = 0
        for title in subitems:
            if add_subitem(parent_id, title):
                ok_count += 1
        print(f'OK {kai}: {ok_count}/{len(subitems)}個 追加')

    print('\n完了！Notionを確認してください。')
