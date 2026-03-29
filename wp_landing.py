"""
思春期ママのセルフケア講座｜講座案内ランディングページ作成スクリプト
使い方: python wp_landing.py
"""

import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

FORM_URL = 'https://momoako.com/p/r/xRaLxj7a'


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


def update_page(page_id, title, content, status='draft'):
    url = f'{WP_URL}/wp-json/wp/v2/pages/{page_id}'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    data = {
        'title': title,
        'content': content,
        'status': status,
    }
    response = requests.post(url, json=data, auth=auth)
    if response.status_code == 200:
        result = response.json()
        print(f'更新完了: {result["title"]["rendered"]}')
        print(f'公開URL: {result["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={result["id"]}&action=edit')
        return result
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)
        return None


if __name__ == '__main__':
    title = '思春期ママのセルフケア講座｜講座ご案内'

    content = f'''
<p style="text-align:center; font-size:28px; font-weight:bold; margin: 40px 0; line-height:1.6;">
何があっても大丈夫な私になろう
</p>

<hr>

<h2>6ヶ月後のあなたへ</h2>

<ul style="line-height:2.2; font-size:16px;">
<li>何が起きても「大丈夫」と思える自分がいる</li>
<li>自分の感情を上手に扱えている</li>
<li>からだの変化にも早く気づいて、自分でケアできている</li>
<li>気持ちよく、自分らしく毎日を過ごせている</li>
</ul>

<hr>

<h2>この講座について</h2>

<p>認知行動療法・スキーマ療法・解決志向ブリーフセラピーをベースに、<br>
6ヶ月かけて「自分が自分の味方になる」スキルを育てる講座です。</p>

<p>毎週メールが届きます。動画を見て、ワークに取り組む。<br>
できる週も、できない週もあっていい。<br>
あなたのペースで進めてください。</p>

<hr>

<p style="font-size:15px; line-height:1.9;">
あなたと一緒に歩めることが、私はとても嬉しいです。<br>
<strong>桃木亜子</strong>
</p>

<hr>

<p style="font-size:13px; color:#888;">
※ @icloud.com・@me.com などApple系アドレスにはメールが届きません。Gmailなど別のアドレスでご登録ください。
</p>

<p style="text-align:center; margin: 50px 0;">
<a href="{FORM_URL}"
   style="display:inline-block; background-color:#e07b8a; color:#fff; padding:18px 48px; border-radius:4px; text-decoration:none; font-size:17px; font-weight:bold; letter-spacing:0.05em;">
登録はこちら
</a>
</p>

<p style="text-align:center; font-size:13px; color:#aaa;">桃木亜子 / 思春期ママのセルフケア講座</p>
'''

    print('WordPressに接続中...')
    update_page(1352, title, content, status='draft')
