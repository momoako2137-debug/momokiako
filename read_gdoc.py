"""
Google ドライブのドキュメントを読み込んでテキストファイルに保存するスクリプト
使い方: python read_gdoc.py
"""

import os
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive',
]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.json')


def get_credentials():
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


def extract_doc_id(url):
    match = re.search(r'/document/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None


def read_gdoc(url, save_folder):
    doc_id = extract_doc_id(url)
    if not doc_id:
        print("URLからIDを取得できませんでした")
        return

    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)

    # ファイル名を取得
    file_meta = drive_service.files().get(fileId=doc_id, fields='name').execute()
    file_name = file_meta.get('name', 'document')
    print(f"ファイル名: {file_name}")

    # テキストとしてエクスポート
    content = drive_service.files().export(
        fileId=doc_id,
        mimeType='text/plain'
    ).execute()

    # 保存
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, f"{file_name}.txt")
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(content.decode('utf-8'))

    print(f"保存完了: {save_path}")
    return save_path


if __name__ == '__main__':
    url = 'https://docs.google.com/document/d/1gQY8W1x1epRqxQjFI7ITDhzrDzp7ff-7OoS1upGuTW8/edit?usp=sharing'
    save_folder = os.path.join(os.path.dirname(__file__), 'references')
    read_gdoc(url, save_folder)
    print("\n完了！")
