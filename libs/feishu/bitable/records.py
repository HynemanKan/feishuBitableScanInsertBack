import json

import requests

from libs.feishu import feishu_response_load


def insert_record(access_token:str,app_token:str,table_id:str,fields:dict):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    response = requests.post(
        url,
        json={
            "fields": fields,
        },
        headers={"Authorization": f"Bearer {access_token}"})
    feishu_response_load(response)

def select_record(access_token:str,app_token:str,table_id:str,field_need:list[str],filter_json:str):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
    response = requests.post(
        url,
        json={
            "field_names": field_need,
            "filter":json.loads(filter_json),
            "automatic_fields": False,
        },
        headers={"Authorization": f"Bearer {access_token}"})
    data = feishu_response_load(response)
    return data["data"]

def update_record(access_token:str,app_token:str,table_id:str,record_id:str,fields:dict):
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
    response = requests.put(
        url,
        json={
            "fields": fields,
        },
        headers={"Authorization": f"Bearer {access_token}"})
    feishu_response_load(response)
