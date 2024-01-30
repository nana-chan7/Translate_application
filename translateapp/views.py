# モジュールインポート
from translateapp import app
from flask import render_template, request
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# 認証情報 初期化関数
def aws_initialization(aws_id, aws_key, region):
    # AWS Translateを初期化
    translate = boto3.client('translate', 
                            aws_access_key_id=aws_id, 
                            aws_secret_access_key=aws_key, 
                            region_name=region)
    # Comprehendクライアントを初期化
    comprehend = boto3.client('comprehend', 
                            aws_access_key_id=aws_id, 
                            aws_secret_access_key=aws_key, 
                            region_name=region)
    
    return translate, comprehend

# トップページ
@app.route('/')
def index():
    return render_template('translateapp/index.html')

@app.post('/main')
@app.get('/main')
def main():
    if request.method == "GET":
        return render_template('translateapp/main.html')
    
    if request.method == 'POST':
        
        # 認証情報を取得
        res_id = request.form['aws_access_key_id']
        res_key = request.form['aws_secret_access_key']
        res_region = request.form['region']
        
        # 翻訳したい日本語テキストを取得
        input_text = request.form['text']
        target_lang = request.form['target_lang']
        
        # AWS認証とクライアントの初期化
        translate, _ = aws_initialization(res_id, res_key, res_region)  
        
        # ソース言語 (日本語)
        source_lang = "ja"
        
        try:
            # テキストを指定された言語に翻訳
            translate_result = translate.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
            translate_text = translate_result['TranslatedText']
        except (BotoCoreError, ClientError) as error:
            # AWSからのエラーを処理
            error_message = f"翻訳サービスエラー: {str(error)}"
            return render_template('translateapp/error.html', error_message=error_message)
        
        # 翻訳結果ページを表示
        return render_template('translateapp/result.html', original_text=input_text, translate_text=translate_text, source_language_code=target_lang)