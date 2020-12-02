from flask import current_app
import json
import requests
from flask_babel import _
import os
import time
# from app.get_token import get_token


def get_token(app):
    with app.app_context():
        req = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                          json={"yandexPassportOauthToken":"AgAAAAAKSLWQAATuwVv6n06gDkY7uKfAU-Bf1H0"})
        app.config['IAM_TOKEN'] = json.loads(req.content.decode('utf-8-sig'))['iamToken']
        time.sleep(2)
        os.environ['IAM_TOKEN'] = app.config['IAM_TOKEN']

    # print(current_app.config['IAM_TOKEN'])
    # os.system('set IAM_TOKEN = {}'.format(json.loads(r.content.decode('utf-8-sig'))['iamToken']))


def translate(text, source_lang, dest_lang):
    if 'IAM_TOKEN' not in current_app.config or not current_app.config['IAM_TOKEN']:
        return _('Ошибка: сервис перевода не сконфигурирован.')
    auth_head = {'Authorization': 'Bearer ' + current_app.config['IAM_TOKEN']}
    # print(current_app.config['IAM_TOKEN'])
    r = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                      json={"folder_id": "b1g7ssfgaa2lgvdvn9e3",
                            "texts": [text],
                            "targetLanguageCode": dest_lang,
                            "sourceLanguageCode": source_lang},
                      headers=auth_head)
    if r.status_code != 200:
        try:
            get_token(current_app._get_current_object())
            return translate(text, source_lang, dest_lang)
            # return json.loads(r.content.decode('utf-8-sig'))['languageCode']
        except:
            return _('Ошибка: Ошибка доступа к серверу перевода.')
        # translate(text, source_lang, dest_lang)
    # return json.loads(r.content.decode('utf-8-sig'))['translations'][0]['text']
    current_app.logger.info("translate '{}', from '{}', to '{}'".format(text, source_lang, dest_lang))
    return json.loads(r.content.decode('utf-8-sig'))['translations'][0]


def detect_lang(text):
    if 'IAM_TOKEN' not in current_app.config or not current_app.config['IAM_TOKEN']:
        language = ''
    auth_head = {'Authorization': 'Bearer ' + current_app.config['IAM_TOKEN']}
    lang_hints =['ru', 'en']
    r = requests.post('https://translate.api.cloud.yandex.net/translate/v2/detect',
                      json={"folder_id": "b1g7ssfgaa2lgvdvn9e3",
                            "text": text,
                            "languageCodeHints": lang_hints},
                            headers=auth_head)
    if r.status_code != 200:
        try:
            get_token(current_app._get_current_object())
            return detect_lang(text)
            # return json.loads(r.content.decode('utf-8-sig'))['languageCode']
        except:
            language = ''
            return language
    else:
        print('return  ' + json.loads(r.content.decode('utf-8-sig'))['languageCode'])
        print(type(json.loads(r.content.decode('utf-8-sig'))['languageCode']))
        # return json.loads(r.content.decode('utf-8-sig'))['languageCode']
        lang = json.loads(r.content.decode('utf-8-sig'))['languageCode']
        return str(lang)


# def get_token():
#     r = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
#                       json={"yandexPassportOauthToken":"AgAAAAAKSLWQAATuwVv6n06gDkY7uKfAU-Bf1H0"})
#     os.environ['IAM_TOKEN'] = json.loads(r.content.decode('utf-8-sig'))['iamToken']
#     time.sleep(3600)


# получить токен
# curl -d "{\"yandexPassportOauthToken\":\"AgAAAAAKSLWQAATuwVv6n06gDkY7uKfAU-Bf1H0\"}" "https://iam.api.cloud.yandex.net/iam/v1/tokens"
# {
#  "iamToken": "t1.9f7L7euelZqbi5ecycjLl4-bi5PHm5HPkuX090MMYQL67zdHIPDd9PcDO14C-u83RyDw.-GXojdk9C4bsoz8ZY4jvpZhN2098V6x01QOwnQkPYaZScD4XrklC9VCp1C2ueEsD2jsYSsGo5KBs7QtXZsbdDw",
#  "expiresAt": "2020-11-08T21:26:20.033021Z"
# }

# AgAAAAAKSLWQAATuwVv6n06gDkY7uKfAU-Bf1H0



def test_env(value):
    os.environ['TEST_ENV'] = str(value)
    some_result = 'result ' + current_app.config['TEST_ENV']
    return print(some_result)
