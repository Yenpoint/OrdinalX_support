import os
import logging
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_environment():
    load_dotenv()

def open_session():
    fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
    url = 'https://' + fqdn

    session = requests.Session()
    try:
        response = session.get(url + '/auth/login/')
        response.raise_for_status()

        cookies = session.cookies
        if cookies:
            for i, (name, value) in enumerate(cookies.items()):
                logger.debug(f'Cookie #{i}\t{name}: {value}')
        else:
            raise RuntimeError('サーバーがクッキーを返しませんでした')

        csrf_token = response.cookies.get('csrftoken')
        if csrf_token:
            logger.debug(f'CSRF token: {csrf_token}')
            return session, csrf_token
        else:
            raise RuntimeError('サーバーがCSRFトークンを返しませんでした')

    except Exception as e:
        logger.critical(f'セッション開始時にエラーが発生: {e}')
        raise

def login(session, csrf_token):
    # ログイン情報を環境変数からとってくる
    credential = {'username': os.environ.get('ORDINALX_USERNAME'),
                  'password': os.environ.get('ORDINALX_PASSWORD')}
    logger.debug(f'Login with credentials: {credential}')

    # セッション認証でログインする
    fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
    endpoint = '/api/v1/auth/login'
    url = 'https://' + fqdn + endpoint
    headers = {'X-CSRFTOKEN': csrf_token}
    response = session.post(url, json=credential, headers=headers)

    logger.debug(f'Request Header: {response.request.headers}')
    logger.debug(f'Request Body  : {response.request.body}')
    logger.debug(f'Response      : {response.text}')

    response.raise_for_status()
    return session.cookies.get('csrftoken', csrf_token)

def logout(session):
    fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
    endpoint = '/api/v1/auth/logout'
    url = 'https://' + fqdn + endpoint
    response = session.get(url)
    logger.debug(f'Logout response: {response.status_code}')