import argparse
import logging
from utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(params):
    logger.info('OrdinalX NFT API Sample: Burn NFT')

    # 閑居変数の読み込み
    load_environment()

    # セッションを張ってログインする
    session, csrf_token = open_session()
    csrf_token = login(session, csrf_token)

    try:
        # NFTを燃やす
        fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
        endpoint = '/api/v1/nft/burn'
        url = 'https://' + fqdn + endpoint
        headers = {
            'X-CSRFTOKEN': csrf_token,
            'Referer': 'https://' + fqdn,
        }
        request = {
            'nft_origin': params.origin
        }
        response = session.post(url, headers=headers, json=request)

        logger.debug(f'Request Header: {response.request.headers}')
        logger.debug(f'Request Body  : {response.request.body}')
        logger.debug(f'response: {response.text}')
        logger.info(f'API server responded with status {response.status_code}')

        # 送信が成功すると201が返ってくる
        if response.status_code == 201:
            logger.info(f'NFT(origin: {params.origin}) has been burnt successfully!')
            txid = response.json()['transaction_id']
            logger.info(f'Transaction ID: {txid}')
            logger.info(f'See https://whatsonchain.com/tx/{txid} for details')
        # それ以外の応答はエラーを表している
        else:
            logger.warning('Server responded with an error')
            logger.warning(f'Server response: {response.text}')

    finally:
        logout(session)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--origin', required=True, help='NFT origin to burn')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    main(args)
