from dataclasses import fields

from flask import request
from flask_restful import Resource, reqparse, marshal_with

from controllers.console import api
from fields.data_fields import bitable_fields, bitable_tables_fields, bitable_table_fields_fields
from libs.feishu.bitable.records import select_record, insert_record, update_record
from libs.login import login_required, current_user
from libs.response_builder import success
from service.bitable_service import BitableService
from service.drive_file_service import DriveFileService


class BitableFileListApi(Resource):
    @login_required
    @marshal_with(bitable_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pageToken', type=str, location='args')
        args = parser.parse_args()
        if 'pageToken' not in args or args['pageToken'] is None:
            page_token = ""
        else:
            page_token = args['page_token']
        user_access_token = current_user.access_token
        res = DriveFileService.list_bitable_files_in_root(user_access_token,page_token)
        return success({"data":res})

class BitableTableListApi(Resource):
    @login_required
    @marshal_with(bitable_tables_fields)
    def get(self, app_id:str):
        parser = reqparse.RequestParser()
        parser.add_argument('pageToken', type=str, location='args')
        args = parser.parse_args()
        if 'pageToken' not in args or args['pageToken'] is None:
            page_token = ""
        else:
            page_token = args['page_token']
        user_access_token = current_user.access_token
        res = BitableService.get_tables(user_access_token,app_id,page_token)
        return success({"data":res})

class BitableTableFieldListApi(Resource):
    @login_required
    @marshal_with(bitable_table_fields_fields)
    def get(self, app_id:str, table_id:str):
        user_access_token = current_user.access_token
        res = BitableService.get_table_fields(user_access_token,app_id,table_id)
        return success({"data": res})

class BitableTableRecordSearchOneApi(Resource):
    @login_required
    def post(self, app_id:str, table_id:str):
        user_access_token = current_user.access_token
        parser = reqparse.RequestParser()
        parser.add_argument('fieldsNeed', type=str,action='append', location='json')
        parser.add_argument('filterStr', type=str, location='json')
        args = parser.parse_args()
        data = select_record(user_access_token,app_id,table_id,args['fieldsNeed'],args['filterStr'])
        if len(data["items"])==0:
            return success({"data":{
                "fields":{},
                "record_id":""
            }})
        else:
            return success({
                "data":data["items"][0]
            })

class BitableTableRecordInsertApi(Resource):
    @login_required
    def post(self, app_id: str, table_id: str):
        user_access_token = current_user.access_token
        body = request.json
        record = body['fields']
        insert_record(user_access_token, app_id, table_id, record)
        return success({})

class BitableTableRecordUpdateApi(Resource):
    @login_required
    def put(self, app_id: str, table_id: str, record_id: str):
        user_access_token = current_user.access_token
        body = request.json
        record = body['fields']
        update_record(user_access_token, app_id, table_id, record_id, record)
        return success({})

api.add_resource(BitableFileListApi, '/feishu/bitables')
api.add_resource(BitableTableListApi, '/feishu/bitables/<app_id>/tables')
api.add_resource(BitableTableFieldListApi, '/feishu/bitables/<app_id>/tables/<table_id>/fields')
api.add_resource(BitableTableRecordSearchOneApi,'/feishu/bitables/<app_id>/tables/<table_id>/records/searchOne')
api.add_resource(BitableTableRecordInsertApi,'/feishu/bitables/<app_id>/tables/<table_id>/records')
api.add_resource(BitableTableRecordUpdateApi,"/feishu/bitables/<app_id>/tables/<table_id>/records/<record_id>")