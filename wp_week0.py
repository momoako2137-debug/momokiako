"""
第0回｜オリエンテーション WordPress LP作成スクリプト（SWELL）
使い方:
  python wp_week0.py          # 新規作成（下書き）
  python wp_week0.py update   # 既存ページを上書き更新
"""

import sys
import requests
from requests.auth import HTTPBasicAuth
from wp_config import WP_URL, WP_USER, WP_APP_PASSWORD

YOUTUBE_ID = 'FLpzWWAq2ks'       # 動画③「AIを味方にするために」
KEICHO_AI_URL = 'https://gemini.google.com/gem/19Yht4_vUONwMu5yYM_Uk8sqsXnnXT8Mh?usp=sharing'
EXISTING_POST_ID = 1362            # 既存下書きID（update モード用）


# ── Gutenberg ブロック記法で生成 ─────────────────────────────────
# ブロックコメントで囲むことでビジュアルエディターで手直しできる

def h2(text):
    return (
        '<!-- wp:heading {"className":"wp-block-heading"} -->\n'
        f'<h2 class="wp-block-heading">{text}</h2>\n'
        '<!-- /wp:heading -->'
    )


def p(html):
    return f'<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->'


def sep():
    return (
        '<!-- wp:separator -->\n'
        '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
        '<!-- /wp:separator -->'
    )


def group_pink(inner_blocks):
    style = (
        'background-color:#fdf6f7;border-radius:8px;'
        'padding-top:28px;padding-right:32px;padding-bottom:28px;padding-left:32px'
    )
    return (
        '<!-- wp:group {"style":{"color":{"background":"#fdf6f7"},"border":{"radius":"8px"},'
        '"spacing":{"padding":{"top":"28px","right":"32px","bottom":"28px","left":"32px"}}},'
        '"layout":{"type":"constrained"}} -->\n'
        f'<div class="wp-block-group" style="{style}">\n'
        + '\n\n'.join(inner_blocks) + '\n'
        '</div>\n'
        '<!-- /wp:group -->'
    )


def youtube_embed(video_id):
    url = f'https://www.youtube.com/watch?v={video_id}'
    return (
        f'<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube",'
        '"responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
        '<figure class="wp-block-embed is-type-video is-provider-youtube '
        'wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">'
        '<div class="wp-block-embed__wrapper">\n'
        f'{url}\n'
        '</div></figure>\n'
        '<!-- /wp:embed -->'
    )


def button(label, href):
    return (
        '<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->\n'
        '<div class="wp-block-buttons">'
        '<!-- wp:button {"style":{"border":{"radius":"4px"},'
        '"color":{"background":"#e07b8a","text":"#ffffff"}}} -->\n'
        '<div class="wp-block-button">'
        f'<a class="wp-block-button__link wp-element-button" '
        f'href="{href}" target="_blank" rel="noreferrer noopener" '
        'style="border-radius:4px;background-color:#e07b8a;color:#ffffff">'
        f'{label}</a></div>\n'
        '<!-- /wp:button --></div>\n'
        '<!-- /wp:buttons -->'
    )


# ── コンテンツ本文 ────────────────────────────────────────────────

def build_content():
    blocks = [

        # ── はじめに ──
        h2('はじめに'),
        p('さあ、いよいよセルフケア講座が始まります！'),
        p('私たち母親って、ほんとうにいろんな役割がありますよね。母親として、妻として、娘として——'
          'そんな中でいろいろと揺れるのが、私たちの世代。自分自身だって更年期の変化があるのに、'
          '思春期の子どもとも向き合っていかないといけない。'),
        p('<strong>何があっても大丈夫</strong>と思えるスキルを、この講座でお渡ししていきます。'),
        p('6ヶ月という長丁場だからこそ、じっくり身につけていただけると思っています。'
          '一方で、長いからこそモチベーションが下がることもあると思います。'
          'だから、学習コンテンツとは別に、毎週私からのメールが届くように工夫していきますね。'),
        p('また、受講していくなかで「こうしてほしい」「ここがわかりにくい」と感じたことがあったら、'
          'どんどん教えてください。みなさんの声を聞きながら、より良い講座にしていきたいと思っています。'),
        p('では、さっそく始めましょう！'),

        sep(),

        # ── この講座の使い方 ──
        h2('この講座の使い方'),
        p('毎週1回、メルマガが届きます。メルマガのリンクをクリックすると、このようなページに来られます。'),
        group_pink([
            p('メルマガが届く<br>↓<br>リンクをクリック<br>↓<br>このページを開く<br>↓<br>動画を見る・ワークをやってみる'),
        ]),
        p('これだけです。難しい操作はありません。'),
        p('<strong>「全部やらなきゃ」と思わなくて大丈夫</strong><br>'
          '動画1本だけでもOK。ワークは後日まとめてでもOK。'
          'この講座のゴールは、半年後の自分が今より少しだけ楽になっていること。完璧にやることではありません。'),

        sep(),

        # ── 動画 ──
        h2('動画｜AIを味方にするために'),
        p('この講座では、自分のモヤモヤした気持ちを<strong>言葉にする練習</strong>を大切にしています。'
          'その練習相手として、<strong>傾聴AI</strong>を活用していただきたいと思っています。'),
        p('「AIに悩みを話して大丈夫？」と感じている方もいると思います。'
          'まずはこの動画で、傾聴AIとは何か・安心して使うために知っておいてほしいことを確認してください。'),
        youtube_embed(YOUTUBE_ID),
        group_pink([
            p('<strong>大切にしてほしい3つのこと</strong>'),
            p('<strong>① ハンドルは、いつも自分が持つ</strong><br>'
              'AIはあなたの気持ちを引き出してくれる道具です。でも、判断するのはあなた自身。'
              'AIに言われたことを鵜呑みにしないで、「参考にする」くらいの距離感で使ってください。'),
            p('<strong>② 頼る先は、ひとつにしない</strong><br>'
              'AIは頼りになる仲間の一つです。でも、AIだけに話すようになると、かえって孤独感が増すことも。'
              '家族・友人・この講座——いろんな場所に緩く広く頼ることが、長い目で見て大切です。'),
            p('<strong>③ 深刻なときは、人に・専門家に</strong><br>'
              '気持ちが追い詰められているとき、死にたいという気持ちがあるときは、'
              'AIではなく必ず人に相談してください。かかりつけの医師・相談窓口・信頼できる人に連絡を。'),
        ]),

        sep(),

        # ── 受講の心構え ──
        h2('受講の心構え'),
        p('3つだけ、覚えておいてください。'),
        p('<strong>① 比べない</strong><br>'
          '他の受講者とも、SNSの理想のお母さん像とも、比べなくて大丈夫。'
          'この講座で、あなた自身のあり方を一緒に探していきましょう。'),
        p('<strong>② 小さく試す</strong><br>'
          '動画もワークも、全部一度にやらなくて構いません。「これだけやってみよう」と一つ決めるだけで、十分です。'),
        p('<strong>③ 困ったらひとりで抱え込まない</strong><br>'
          '感想・疑問・「うまくいかなかった」——どんなことでもメルマガへの返信で送ってください。'),

        sep(),

        # ── 今週のワーク ──
        h2('今週のワーク'),
        p('傾聴AIに、今の気持ちを話してみてください。'),
        p('「申し込んでみたけど、ちゃんとできるかな」「なんだかモヤモヤしている」——'
          'そんなちょっとした気持ちで大丈夫です。うまく話せなくてもOK。'
          'まず話しかけてみることが、この講座の最初の一歩です。'),
        p('話し終わったら、最後に「終わり」と伝えてみてください。'),
        button('▶ 傾聴AIを使ってみる', KEICHO_AI_URL),

        sep(),

        p('ワークが進んだら、メールを返信する形でご連絡くださると嬉しいです。'
          '気がついたことなどありましたら、何でも伝えてくださいね。'
          'ワークをご提出いただけましたら、必ずチェックしてお返しします。'),

        p('<small>※本記事はセルフケア講座オンラインコース受講生様のみに提供するために作成したものです。'
          '第三者への開示・シェアなどは固くお断りさせていただきます。</small>'),

    ]
    return '\n\n'.join(blocks)


# ── API 操作 ──────────────────────────────────────────────────────

def post_lp(title, content, status='draft'):
    """新規作成（固定ページ）"""
    url = f'{WP_URL}/wp-json/wp/v2/pages'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={'title': title, 'content': content, 'status': status}, auth=auth)
    _print_result(response, '作成')


def update_lp(post_id, title, content, status='draft'):
    """既存ページを上書き更新（通常の page として作成済みの場合）"""
    url = f'{WP_URL}/wp-json/wp/v2/pages/{post_id}'
    auth = HTTPBasicAuth(WP_USER, WP_APP_PASSWORD)
    response = requests.post(url, json={'title': title, 'content': content, 'status': status}, auth=auth)
    _print_result(response, '更新')


def _print_result(response, action):
    if response.status_code in (200, 201):
        r = response.json()
        print(f'{action}完了: {r["title"]["rendered"]}')
        print(f'公開URL: {r["link"]}')
        print(f'編集URL: {WP_URL}/wp-admin/post.php?post={r["id"]}&action=edit')
    else:
        print(f'エラー: {response.status_code}')
        print(response.text)


# ── エントリポイント ──────────────────────────────────────────────

if __name__ == '__main__':
    title = '第0回｜オリエンテーション'
    content = build_content()

    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        print(f'既存ページ（ID: {EXISTING_POST_ID}）を更新中...')
        update_lp(EXISTING_POST_ID, title, content)
    else:
        print('WordPressに接続中...')
        post_lp(title, content)
