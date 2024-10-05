import json

import requests

from libs.feishu import feishu_response_load
from libs.feishu.errors import FeishuError


def get_tenant_access_token(app_id:str,app_secret:str)->str:
    res =requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                  json={"app_id":app_id, "app_secret":app_secret})
    data = feishu_response_load(res)
    return data['tenant_access_token']

class JsApiTicket:
    ticket:str
    expire_in:str

def get_js_api_ticket(access_token:str)->JsApiTicket:
    res = requests.post("https://open.feishu.cn/open-apis/jssdk/ticket/get",
                        json={},headers={"Authorization":"Bearer "+access_token})
    data = feishu_response_load(res)
    ticket = JsApiTicket()
    ticket.ticket = data['data']['ticket']
    ticket.expire_in = data['data']['expire_in']
    return ticket

class UserInfo:
    access_token:str
    token_type:str
    expires_in:str
    name:str
    en_name:str
    avatar_url:str
    open_id:str
    union_id:str
    email:str
    user_id:str
    refresh_expires_in:int
    refresh_token:str
    sid:str

def get_user_access_token(access_token:str,user_ticket:str)->UserInfo:
    response = requests.post("https://open.feishu.cn/open-apis/authen/v1/access_token",
                  json={
                      'grant_type':'authorization_code',
                      'code':user_ticket
                  },headers={"Authorization":"Bearer "+access_token})
    data = feishu_response_load(response)
    userInfo = UserInfo()
    userInfo.access_token = data['data']['access_token']
    userInfo.token_type = data['data']['token_type']
    userInfo.expire_in = data['data']['expires_in']
    userInfo.name = data['data']['name']
    userInfo.en_name = data['data']['en_name']
    userInfo.avatar_url = data['data']['avatar_url']
    userInfo.open_id = data['data']['open_id']
    userInfo.union_id = data['data']['union_id']
    userInfo.email = data['data']['email']
    userInfo.user_id = data['data']['user_id']
    userInfo.refresh_expire_in = data['data']['refresh_expires_in']
    userInfo.refresh_token = data['data']['refresh_token']
    userInfo.sid = data['data']['sid']
    return userInfo