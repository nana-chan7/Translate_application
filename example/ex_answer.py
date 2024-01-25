import boto3
import json

aws_access_key_id="aws_access_key_id",
aws_secret_access_key="aws_secret_access_key",
region="region"

#comprehend = boto3.client('comprehend', 'us-east-2')
comprehend = boto3.client('comprehend',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region)

text_j = "20%OFFクーポンを使用しようとしたのですが、10%しか割引にならず、注文できませんでした。"
text_ch = "在从中国入境时被告知携带被禁止，并被没收行李。"

translate = boto3.client('translate',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region)
result_en = translate.translate_text(
    Text=text_j,
    SourceLanguageCode='auto',
    TargetLanguageCode='en')

text = result_en["TranslatedText"]
print('translated text : ', text)


result = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
print(json.dumps(result, indent=4))

result_ch = translate.translate_text(
    Text=text_ch,
    SourceLanguageCode='auto',
    TargetLanguageCode='en')

text = result_ch["TranslatedText"]
print('translated text : ', text)
result = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
print(json.dumps(result, indent=4))