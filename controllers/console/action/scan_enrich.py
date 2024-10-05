from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with

from controllers.console import api
from fields.scan_enrich_fields import scan_enrich_fields
from libs.login import login_required
from libs.response_builder import success
from service.scan_enrich_service import ScanEnrichService,SourceType


class ScanEnrich(Resource):

    @login_required
    @marshal_with(scan_enrich_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('scanContent', type=str, required=True)
        parser.add_argument('source', type=str, required=True)
        args = parser.parse_args()
        source = args.get('source')
        if SourceType.SZLCSC.value == source:
            source_type = SourceType.SZLCSC
        else:
            raise ValueError("Source type not supported")
        component =  ScanEnrichService.enrich(args['scanContent'],source_type)
        return success({
            "component":component.__dict__
        })



api.add_resource(ScanEnrich, '/action/scanEnrich')