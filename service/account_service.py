from datetime import datetime, timezone, timedelta
from turtledemo.penrose import inflatedart

from configs import app_config
from libs.feishu.auth import UserInfo
from libs.passport import PassportService
from libs.encrypt import decrypt,encrypt
from model.Account import Account


class AccountService:

    @staticmethod
    def load_user_from_token(payload:dict)->Account:
        account =Account()
        account.user_id=payload['user_id']
        account.access_token=AccountService.decrypt_token(payload['encrypt_token'])
        return account

    @staticmethod
    def sign_token(info: UserInfo,exp: timedelta = timedelta(days=30)):

        payload = {
            "user_id": info.open_id,
            "encrypt_token":AccountService.encrypt_token(info.access_token),
            "exp": datetime.now(timezone.utc).replace(tzinfo=None) + exp,
            "sub": "Console API Passport",
        }

        token = PassportService().issue(payload)
        return token

    @staticmethod
    def encrypt_token(token:str)->str:
        return encrypt(token,app_config.SCANNING_APP_SECRET)

    @staticmethod
    def decrypt_token(token:str)->str:
        return decrypt(token,app_config.SCANNING_APP_SECRET)