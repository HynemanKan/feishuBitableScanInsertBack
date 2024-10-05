from flask_restful import fields
from . import base_fields

component_fields = {
    "selfId": fields.String(attribute="self_id"),
    "name": fields.String,
    "supplierName": fields.String(attribute="supplier_name"),
    "supplierItemId": fields.String(attribute="supplier_item_id"),
    "qty": fields.Integer,
    "supplierDetailPageUrl": fields.String(attribute="supplier_detail_page_url"),
    "datasheetUrl": fields.String(attribute="datasheet_url"),
    "category": fields.List(fields.String),
    "description": fields.String,
    "brand": fields.String,
    "package": fields.String,
    "imgUrl": fields.String(attribute="img_url"),
}

scan_enrich_fields = {
    "component":fields.Nested(component_fields),
}
scan_enrich_fields.update(base_fields)