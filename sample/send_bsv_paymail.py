import argparse
import logging
from utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(params):
    logger.info('OrdinalX NFT API Sample: Send BSV by Paymail')

    # 閑居変数の読み込み
    load_environment()

    # セッションを張ってJWTトークンを取得する
    session, csrf_token = open_session()
    jwt_token = get_jwt_token(session)
    logger.debug(f'Acquired JWT token: {jwt_token}')

    # BSVを送金する
    fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
    endpoint = '/api/v1/bsv/paymail/send'
    url = 'https://' + fqdn + endpoint
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-CSRFTOKEN': csrf_token
    }
    request = {
        'recipient_paymail': params.destination,
        'amount_satoshis': params.amount
    }
    response = session.post(url, headers=headers, json=request)

    logger.debug(f'Request Header: {response.request.headers}')
    logger.debug(f'Request Body  : {response.request.body}')
    logger.debug(f'response: {response.text}')
    logger.info(f'API server responded with status {response.status_code}')

    # 送金が成功すると200が返ってくる
    if response.status_code == 200:
        logger.info(f'BSV amount of {params.amount} satoshis has been sent to {params.destination} successfully!')
        txid = response.json()['txid']
        logger.info(f'Transaction ID: {txid}')
        logger.info(f'See https://whatsonchain.com/tx/{txid} for details')
    # 200以外の応答はエラーを表している
    else:
        logger.warning('Server responded with an error')
        logger.warnning(f'Server response: {response.text}')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--destination', default='jo7ueb@handcash.io', help='Destination paymail address')
    parser.add_argument('-a', '--amount', default=22, help='Amount of BSV to send in Satoshi')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    main(args)
