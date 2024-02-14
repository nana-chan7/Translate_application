# モジュールインポート
from translateapp import app
from flask import render_template, request
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import re
import key

# バリデーション関数
def validate_aws_access_key_id(key_id):
    return len(key_id) == 20 and key_id.isalnum()

def validate_aws_secret_access_key(secret_key):
    return len(secret_key) == 40 and bool(re.match('^[a-zA-Z0-9/+]*={0,2}$', secret_key))

def validate_no_special_chars(input_text):
    return not bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', input_text))

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

# メインページ
@app.post('/main')
@app.get('/main')
def main():
    if request.method == "GET":
        return render_template('translateapp/main.html')
    
    if request.method == 'POST':
        # 認証情報を取得
        aws_access_key_id = request.form['aws_access_key_id']
        aws_secret_access_key = request.form['aws_secret_access_key']
        aws_region = request.form['region']
        
        # 翻訳したい日本語テキストを取得
        input_text = request.form['text']
        target_lang = request.form['target_lang']

        # エラーメッセージリストの初期化
        error_messages = []

        # 入力バリデーション
        if not validate_aws_access_key_id(aws_access_key_id):
            error_messages.append('AWS Access Key IDは20文字の英数字である必要があります。')
        
        if not validate_aws_secret_access_key(aws_secret_access_key):
            error_messages.append('AWS Secret Access Keyは40文字の英数字記号である必要があります。')

        if not validate_no_special_chars(aws_region):
            error_messages.append('AWS Regionに特殊記号を含めることはできません。')

        # エラーメッセージがある場合、エラーページを表示
        if error_messages:
            return render_template('translateapp/error.html', error_messages=error_messages)

        # AWS認証とクライアントの初期化
        translate, _ = aws_initialization(aws_access_key_id, aws_secret_access_key, aws_region)  
        
        # ソース言語 (日本語)
        source_lang = "ja"
        
        try:
            # テキストを指定された言語に翻訳
            translate_result = translate.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
            translate_text = translate_result['TranslatedText']
        except (BotoCoreError, ClientError) as error:
            error_code = error.response['Error']['Code']
            if error_code == 'ValidationException':
                # カスタムエラーメッセージを設定
                custom_error_message = "言語コードは５文字以内の文字列にしてください。詳しくはAmazon Translateのサイトを参照してください。"
                return render_template('translateapp/error.html', error_message=custom_error_message)
            else:
                # その他のAWSエラー
                error_message = f"翻訳サービスエラー: {str(error)}"
                return render_template('translateapp/error.html', error_message=error_message)
        
        # 翻訳結果ページを表示
        return render_template('translateapp/result.html', original_text=input_text, translate_text=translate_text, source_language_code=target_lang)
    
    
