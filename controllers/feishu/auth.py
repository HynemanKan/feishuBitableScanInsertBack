import hashlib
import uuid
import time

from flask_restful import Resource, reqparse
from flask import g, current_app, jsonify

from libs.feishu.auth import get_js_api_ticket
from controllers.feishu import api

class FeishuAuthApi(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('current_url',required=True,location='args')
        args = parser.parse_args()
        app_id = current_app.config['FEISHU_APP_ID']
        token = g.get("tenant_access_token")
        ticket = get_js_api_ticket(token)
        timestamp = int(time.time())*1000
        nonce_str = str(uuid.uuid4())
        verify_str = "jsapi_ticket={}&noncestr={}&timestamp={}&url={}".format(
            ticket.ticket, nonce_str, timestamp, args.get('current_url')
        )
        signature = hashlib.sha1(verify_str.encode("utf-8")).hexdigest()
        return jsonify(
                {
                    "appId": app_id,
                    "signature": signature,
                    "nonceStr": nonce_str,
                    "timestamp": timestamp,
                }
            )


api.add_resource(FeishuAuthApi, '/base_config')
