from flask import current_app
import requests
import os
import time
import json


def get_token(app):
    with app.app_context():
        req = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens',
                          json={"yandexPassportOauthToken":"AgAAAAAKSLWQAATuwVv6n06gDkY7uKfAU-Bf1H0"})



        # print('os.env---' + os.environ.get('IAM_TOKEN'))
        app.config['IAM_TOKEN'] = json.loads(req.content.decode('utf-8-sig'))['iamToken']
        time.sleep(2)
        os.environ['IAM_TOKEN'] = app.config['IAM_TOKEN']
        print('os.env---' + os.environ.get('IAM_TOKEN'))
        print('config---' + current_app.config['IAM_TOKEN'])

    # print(current_app.config['IAM_TOKEN'])
    # os.system('set IAM_TOKEN = {}'.format(json.loads(r.content.decode('utf-8-sig'))['iamToken']))


def test_env(value):
    os.environ['TEST_ENV'] = str(value)
    some_result = 'result ' + current_app.config['TEST_ENV']
    return print(some_result)



# print('os.env---' + os.environ.get('IAM_TOKEN'))
# print('config---' + current_app.config['IAM_TOKEN'])