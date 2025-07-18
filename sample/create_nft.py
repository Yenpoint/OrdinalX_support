import argparse
import logging
from utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(params):
    logger.info('OrdinalX NFT API Sample: Create NFT (and send it by paymail')

    # 閑居変数の読み込みu
    load_environment()

    # セッションを張ってJWTトークンを取得する
    session, csrf_token = open_session()
    jwt_token = get_jwt_token(session)
    logger.debug(f'Acquired JWT token: {jwt_token}')

    # NFTを作成する
    fqdn = os.environ.get('ORDINALX_SERVER_FQDN')
    endpoint = '/api/v1/nft/create'
    url = 'https://' + fqdn + endpoint
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-CSRFTOKEN': csrf_token
    }

    # 宛先は省略できる（省略した場合は自分あてにNFTが作成される)
    if params.destination:
        payload = {
            'recipient_paymail': params.destination,
            'app': 'OrdinalX NFT API sample programs',
            'name': 'YenPoint logo'
        }
    else:
        payload = {
            'app': 'OrdinalX NFT API sample programs',
            'name': 'YenPoint logo'
        }
    files = {
        'file': open(params.file, 'rb')
    }
    response = session.post(url, headers=headers, data=payload, files=files)

    logger.debug(f'Request Header: {response.request.headers}')
    logger.debug(f'Request Body  : {response.request.body}')
    logger.debug(f'response: {response.text}')
    logger.info(f'API server responded with status {response.status_code}')

    # 送金が成功すると201が返ってくる
    if response.status_code == 201:
        logger.info(f'The NFT has been created successfully!')

        txid = response.json()['transaction_id']
        logger.info(f'Transaction ID: {txid}')
        logger.info(f'See https://whatsonchain.com/tx/{txid} for details')

        nft_origin = response.json()['nft_information']['nft_origin']
        logger.info(f'nft_origin (take a note): {nft_origin}')

    # それ以外の応答はエラーを表している
    else:
        logger.warning('Server responded with an error')
        logger.warning(f'Server response: {response.text}')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--destination', default=None, type=str, help='Destination paymail address')
    parser.add_argument('-f', '--file', default='yenpoint_logo.png', help='Path of NFT content file')
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    main(args)
