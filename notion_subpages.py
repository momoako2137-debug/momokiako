"""
各回のNotionページにサブページ（動画①②③・ワーク・中間週）を作成する
"""

import requests
from notion_config import NOTION_TOKEN

HEADERS = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

DB_ID = '332b5cff-9317-81b6-9e25-d8da929022c7'

# 各回のサブページ構成
SUBPAGES = {
    '第0回': ['動画① AIを味方にするために', '動画② この講座の使い方・傾聴AI'],
    '第1回': ['動画① 疲れない脳と身体を戦略的につくる', '動画② 自分らしさって何だろう', '動画③ 中核的感情欲求①'],
    '第2回': ['動画① ストレスに気づく・自動思考をつかまえる', '動画② 捉え方の構造・心の応急処置', '動画③ ネガティブな気持ちを抱えて生きる'],
    '第3回': ['動画① 中核的感情欲求とは', '動画② 自分で安心をつくる・自分の味方になる', '動画③ 中核的感情欲求③'],
    '第4回': ['動画① 生きづらさを手放す・捉え方を変える', '動画② ぐるぐる思考を手放す', '動画③ 中核的感情欲求④'],
    '第5回': ['動画① 幸せは自分でつくる', '動画③ 中核的感情欲求⑤'],
    '第6回': ['動画① 「孤独」について', '動画② 心の病気について・専門家につながる勇気'],
    '第7回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）'],
    '第8回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）'],
    '第9回': ['動画① （準備中）', '動画② （準備中）', '動画③ （準備中）'],
    '第10回': ['動画① （準備中）', '動画② （準備中）'],
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


def add_subpages(parent_page_id, subpage_titles):
    success = True
    for title in subpage_titles:
        data = {
            'parent': {'page_id': parent_page_id},
            'properties': {
                'title': {'title': [{'text': {'content': title}}]}
            }
        }
        response = requests.post(
            'https://api.notion.com/v1/pages',
            headers=HEADERS,
            json=data
        )
        if response.status_code != 200:
            success = False
    return success


if __name__ == '__main__':
    print('ページ一覧を取得中...')
    pages = get_all_pages()

    for kai, subpage_titles in SUBPAGES.items():
        if kai in pages:
            success = add_subpages(pages[kai], subpage_titles)
            status = 'OK' if success else 'NG'
            print(f'{status} {kai}: サブページ {len(subpage_titles)}個 追加')
        else:
            print(f'-- {kai}: ページが見つかりませんでした')

    print('\n完了！Notionを確認してください。')
