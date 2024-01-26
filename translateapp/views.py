# モジュールインポート
from translateapp import app
from flask import render_template, request
import boto3
import json

from . import key # AWS認証用

# AWS認証・リージョン
aws_access_key_id = key.AWS_ACCESS_KEY_ID  # ID
aws_secret_access_key = key.AWS_SECRET_ACCESS_KEY  # アクセスキー
region = key.AWS_REGION  # リージョン

# AWS Translateを初期化
translate = boto3.client('translate', 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key, 
                        region_name=region)
# Comprehendクライアントを初期化
comprehend = boto3.client('comprehend', 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key, 
                        region_name=region)

# トップページ
@app.route('/')
def index():
    return render_template('translateapp/index.html')

# 翻訳ページ
@app.post('/main')
@app.get('/main')
def main():
    if request.method == "GET":
        return render_template('translateapp/main.html')
    
    if request.method == 'POST':
        # ソース言語 (日本語)
        source_lang = "ja"
        
        # 翻訳したい日本語テキストを取得
        input_text = request.form['text']
        target_lang = request.form['target_lang']
        
        # テキストを指定された言語に翻訳
        translate_result = translate.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
        translate_text = translate_result['TranslatedText']

        # 翻訳結果ページを表示
        return render_template('translateapp/result.html', original_text=input_text, translate_text=translate_text, source_language_code=target_lang)