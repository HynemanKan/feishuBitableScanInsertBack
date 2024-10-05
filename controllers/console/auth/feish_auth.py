from flask import jsonify, g
from flask_restful import Resource, reqparse

from controllers.console import api
from libs.feishu.auth import get_user_access_token
from libs.response_builder import success
from service.account_service import AccountService


class FeishuAuth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ticket', type=str, required=True)
        args = parser.parse_args()
        token = g.get("tenant_access_token")
        userInfo = get_user_access_token(token, args.get("ticket"))
        jwt_token = AccountService.sign_token(userInfo)
        return  success({
            "token":jwt_token
        })


api.add_resource(FeishuAuth, '/auth/feishuLogin')