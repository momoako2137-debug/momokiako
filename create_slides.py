"""
思春期ママのセルフケア講座 — Googleスライド自動生成スクリプト
使い方: python create_slides.py
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 設定
SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')
TEMPLATE_ID = '1lzAYDMz4QCojM0y5LcqVElNJTjVi_KJdsoY7TFJNONk'


def get_credentials():
    """Google APIの認証を行う"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds


def copy_template(drive_service, title):
    """テンプレートをコピーして新しいスライドを作る"""
    body = {'name': title}
    copied = drive_service.files().copy(fileId=TEMPLATE_ID, body=body).execute()
    return copied['id']


def get_slide_ids(slides_service, presentation_id):
    """スライドのIDリストを取得"""
    presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    return [slide['objectId'] for slide in slides]


def update_text(requests, object_id, new_text):
    """テキストを置き換えるリクエストを追加"""
    requests.append({
        'deleteText': {
            'objectId': object_id,
            'textRange': {'type': 'ALL'}
        }
    })
    requests.append({
        'insertText': {
            'objectId': object_id,
            'text': new_text,
            'insertionIndex': 0
        }
    })


def create_lesson_slides(lesson_data):
    """
    講座スライドを自動生成する

    lesson_data の例:
    {
        "title": "第1回｜「私を大切にする」ということ",
        "slides": [
            {
                "heading": "疲れない脳と身体を戦略的につくる",
                "points": ["睡眠の基本", "軽い動き・休憩の入れ方", "からだの声に耳を傾ける"]
            },
            ...
        ]
    }
    """
    creds = get_credentials()
    slides_service = build('slides', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    print(f"テンプレートをコピー中: {lesson_data['title']}")
    new_id = copy_template(drive_service, lesson_data['title'])
    print(f"新しいスライドID: {new_id}")
    print(f"URL: https://docs.google.com/presentation/d/{new_id}/edit")

    return new_id


if __name__ == '__main__':
    # テスト用サンプル
    sample = {
        "title": "第1回｜「私を大切にする」ということ（テスト）",
        "slides": [
            {
                "heading": "疲れない脳と身体を戦略的につくる",
                "points": ["睡眠の基本", "軽い動き・休憩の入れ方", "からだの声に耳を傾ける"]
            }
        ]
    }

    new_presentation_id = create_lesson_slides(sample)
    print("\n完了！上のURLをブラウザで開いてください。")
