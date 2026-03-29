"""
WordPress ページ自動作成スクリプト
使い方: python wp_post.py
"""

import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD


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
        print(f'URL: {result["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={result["id"]}&action=edit')
        return result
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)
        return None


if __name__ == '__main__':
    title = '思春期ママのセルフケア講座｜受講ガイド'

    content = '''
<h2>思春期の子育てを、楽に・楽しく・幸せに。</h2>
<p>親子の明るい未来を、6ヶ月かけて一緒に描いていきましょう。</p>
<p>そのために大切なのは、お母さん自身が安定していること。<br>
お母さんが安定していると、家族が安心できる場になります。<br>
そして、それが家族一人ひとりの力を引き出していきます。</p>
<p>この講座では、心とからだの両方から自分を整えるセルフケアのスキルを、6ヶ月かけて一緒に身につけていきます。</p>
<p>わからないことがあれば、いつでも聞いてくださいね。</p>
<p><strong>桃木亜子</strong></p>

<hr>

<h2>サポートの使い方</h2>

<h3>① Zoom個別相談（3回）</h3>
<p>受講中に3回、モモさんとの個別Zoom相談が受けられます。<br>
〔予約リンク・後日追加〕</p>

<h3>② メールで感想・要望を送る</h3>
<p>気づいたこと・感想・質問はメールでいつでも送ってください。<br>
いただいた内容は、皆さんの学びになるようQ&amp;Aページにまとめていきます（匿名掲載）。</p>

<h3>③ 込み入った個別相談</h3>
<p>深く話したい場合は、受講生優待価格の個別相談をご利用ください。<br>
〔詳細リンク・後日追加〕</p>

<p><strong>Zoom個別相談（3回）と個別相談優待価格は、受講開始から6ヶ月以内にご利用ください。</strong><br>
期間終了後はOKサロンでの継続をご案内します。</p>

<hr>

<h2>動画はメールで届きます</h2>
<p>毎週の動画コンテンツは、登録メールアドレスに届きます。<br>
メールを削除しないよう、大切に保管してください。</p>
<p>迷惑メールフォルダに入ってしまう場合は、<br>
<strong>info@momoako.com</strong> を受信許可設定してください。</p>

<hr>

<h2>カリキュラムと配信スケジュール</h2>
<p>※現在準備中です。確定次第更新します。</p>

<table>
<thead>
<tr><th>週</th><th>種別</th><th>内容</th></tr>
</thead>
<tbody>
<tr><td>1週目</td><td>動画週</td><td>第1回｜「私を大切にする」ということ</td></tr>
<tr><td>2週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>3週目</td><td>動画週</td><td>第2回｜ストレスと上手につきあう</td></tr>
<tr><td>4週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>5週目</td><td>動画週</td><td>第3回｜生きづらさとは（スキーマ療法）</td></tr>
<tr><td>6週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>7週目</td><td>動画週</td><td>第4回｜自分は自分で守る（認知行動療法）</td></tr>
<tr><td>8週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>9週目</td><td>動画週</td><td>第5回｜幸せのつくり方</td></tr>
<tr><td>10週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>11週目</td><td>動画週</td><td>第6回｜「対話」は万能薬</td></tr>
<tr><td>12週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>13週目</td><td>動画週</td><td>第7回｜「困った時」の簡単で効果的なスキル</td></tr>
<tr><td>14週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>15週目</td><td>動画週</td><td>第8回｜未来の私のために（まとめ）</td></tr>
<tr><td>16週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>17週目</td><td>動画週</td><td>第9回｜（準備中）</td></tr>
<tr><td>18週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>19週目</td><td>動画週</td><td>第10回｜（準備中）</td></tr>
<tr><td>20週目</td><td>中間週</td><td>（準備中）</td></tr>
<tr><td>21〜24週目</td><td>最終月</td><td>個別相談・各自の振り返り</td></tr>
</tbody>
</table>

<hr>

<h2>受講の心構え</h2>
<ul>
<li>できた週も、できなかった週もあると思います。自分のペースで進めてください。</li>
<li>動画は何度でも観られます。受講期間終了後も引き続きご覧いただけます。</li>
<li>感じたこと・気づいたことは、どんどんメールでアウトプットしてください。あなたの声が、みんなの学びになっていきます。</li>
</ul>

<hr>

<h2>OKサロンのご案内</h2>
<p>講座と並行して、オンラインの子育てサロン「ママがつながるOKサロン」に参加できます。</p>
<p><strong>月額 1,000円</strong></p>
<ul>
<li>月2回の定例会（話題提供＋対話会）</li>
<li>月2回の読書会（無料参加）</li>
<li>個別相談 1時間 2,500円（会員価格）</li>
</ul>
<p>講座受講中でも、終了後でも入れます。<br>
6ヶ月の講座が終わっても、学びと仲間が続く場所です。</p>
<p>〔OKサロンを見てみる・後日リンク追加〕</p>
'''

    print('WordPressに接続中...')
    create_page(title, content, status='draft')
