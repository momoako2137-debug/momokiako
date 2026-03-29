"""
第0回｜オリエンテーション WordPress ページ作成スクリプト
使い方: python wp_week0.py
※ YouTubeのURLをアップロード後に差し替えてから実行すること
"""

import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

NOTION_URL = 'https://zippy-chocolate-e29.notion.site/332b5cff93178088baaad697aa7e6f05'

# YouTube動画IDをここに入れる（アップロード後に差し替え）
YOUTUBE_1 = 'XXXXXXXXXXXXXXX'  # 動画①「私からひとこと」
YOUTUBE_2 = 'XXXXXXXXXXXXXXX'  # 動画②「この講座の使い方」
YOUTUBE_3 = 'XXXXXXXXXXXXXXX'  # 動画③「傾聴AIを味方にするために」


def create_page(title, content, status='draft'):
    url = f'{WP_URL}/wp-json/wp/v2/pages'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    data = {
        'title': title,
        'content': content,
        'status': status,
    }
    response = requests.post(url, json=data, auth=auth)
    if response.status_code == 201:
        result = response.json()
        print(f'作成完了: {result["title"]["rendered"]}')
        print(f'公開URL: {result["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={result["id"]}&action=edit')
        return result
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)
        return None


if __name__ == '__main__':
    title = '第0回｜オリエンテーション'

    content = f'''
<p>こんにちは。桃木亜子です。</p>

<p>「思春期ママのセルフケア講座」へようこそ！<br>
まずはこの3本の動画を見てください。<br>
1本ずつでも大丈夫です。ゆっくり始めましょう。</p>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<h2>【目次】この講座のカリキュラム</h2>

<p>講座全体のカリキュラムはこちらから確認できます。</p>
<p><a href="{NOTION_URL}" target="_blank" rel="noopener">▶ カリキュラムを見る（Notion）</a></p>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<h2>動画①｜私からひとこと</h2>

<figure class="wp-block-embed is-type-video">
<div class="wp-block-embed__wrapper">
<iframe width="560" height="315"
  src="https://www.youtube.com/embed/{YOUTUBE_1}"
  title="私からひとこと"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen>
</iframe>
</div>
</figure>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<h2>動画②｜この講座の使い方</h2>

<figure class="wp-block-embed is-type-video">
<div class="wp-block-embed__wrapper">
<iframe width="560" height="315"
  src="https://www.youtube.com/embed/{YOUTUBE_2}"
  title="この講座の使い方"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen>
</iframe>
</div>
</figure>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<h2>動画③｜傾聴AIを味方にするために</h2>

<figure class="wp-block-embed is-type-video">
<div class="wp-block-embed__wrapper">
<iframe width="560" height="315"
  src="https://www.youtube.com/embed/{YOUTUBE_3}"
  title="傾聴AIを味方にするために"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowfullscreen>
</iframe>
</div>
</figure>

<hr class="wp-block-separator has-alpha-channel-opacity"/>

<h2>感想・質問はこちらへ</h2>

<p>動画を見て、気づいたこと・感じたことがあれば、<br>
届いたメールに返信して送ってください。<br>
読んでいます。</p>

<p>次回は1週間後、土曜日の朝10時にお届けします。</p>
'''

    print('WordPressに接続中...')
    create_page(title, content, status='draft')
