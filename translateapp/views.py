from translateapp import app
from flask import redirect, render_template, request, session, url_for
import boto3

# AWSクライアントの動的初期化関数
def get_aws_client(service_name):
    if 'aws_access_key_id' in session and 'aws_secret_access_key' in session and 'aws_region' in session:
        return boto3.client(
            service_name,
            aws_access_key_id=session['aws_access_key_id'],
            aws_secret_access_key=session['aws_secret_access_key'],
            region_name=session['aws_region']
        )
    return None  # またはデフォルトの認証情報を使用

@app.route('/')
def index():
    return render_template('translateapp/index.html')

# @app.route('/set_credentials', methods=['GET', 'POST'])
# def set_credentials():
#     if request.method == 'POST':
#         session['aws_access_key_id'] = request.form.get('aws_access_key_id')
#         session['aws_secret_access_key'] = request.form.get('aws_secret_access_key')
#         session['aws_region'] = request.form.get('aws_region')
#         return redirect(url_for('main'))
#     return render_template('translateapp/set_credentials.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('translateapp/main.html')

    if request.method == 'POST':
        # 認証情報の検証とセッションへの保存
        session['aws_access_key_id'] = request.form.get('aws_access_key_id')
        session['aws_secret_access_key'] = request.form.get('aws_secret_access_key')
        session['aws_region'] = request.form.get('aws_region')

        try:
            translate = get_aws_client('translate')
            if translate:
                source_lang = "ja"
                input_text = request.form['text']
                target_lang = request.form['target_lang']
                translate_result = translate.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                translate_text = translate_result['TranslatedText']
                return render_template('translateapp/result.html', original_text=input_text, translate_text=translate_text, source_language_code=target_lang)
            else:
                return 'AWS認証情報が設定されていません。'
        except Exception as e:
            return f'エラーが発生しました: {e}'
    return render_template('translateapp/main.html')

# @app.route('/set_credentials', methods=['GET', 'POST'])
# def set_credentials():
#     if request.method == 'POST':
#         access_key = request.form.get('aws_access_key_id')
#         secret_key = request.form.get('aws_secret_access_key')
#         region = request.form.get('aws_region')

#         # ここで入力値のバリデーションを行う
#         if not access_key or not secret_key or not region:
#             # 不正な入力の場合はエラーページへリダイレクト
#             return render_template('translateapp/error_credentials.html')

#         session['aws_access_key_id'] = access_key
#         session['aws_secret_access_key'] = secret_key
#         session['aws_region'] = region
#         return redirect(url_for('main'))

#     return render_template('translateapp/set_credentials.html')
