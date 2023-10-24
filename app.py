from config import IPA_SERVER, IPA_USER, IPA_PASSWD
from users import user_passwdexp_mod
from applog import logger
from python_freeipa import ClientMeta
import requests
from urllib3.exceptions import InsecureRequestWarning
import argparse
import inspect

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


if __name__ == '__main__':
    arg_list = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--passwdexp",
                        default='no',
                        help='Change user password expires to 31.12.2099')
    try:
        arg_list = parser.parse_args()
    except argparse.ArgumentError:
        logger.critical(f'Argument parsing error {argparse.ArgumentError}, unsuccessfully exiting app (((')
        exit(-1)
    else:
        try:
            if arg_list.passwdexp == 'yes':
                logger.info(f'App started for server {IPA_SERVER}')
                client = ClientMeta(IPA_SERVER, verify_ssl=False)
                if client:
                    logger.info(f'Connected to server {IPA_SERVER}')
                    user_passwdexp_mod(IPA_USER, IPA_PASSWD, client)
            else:
                logger.critical('Unrecognized mode, use --help to view available options')
        except Exception as err:
            logger.error(f'In function \'{inspect.stack()[0][3]}\' error: {str(err)}')
