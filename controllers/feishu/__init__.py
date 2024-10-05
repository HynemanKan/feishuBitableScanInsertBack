from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint("feishu", __name__, url_prefix="/api/v1/feishu")
api = ExternalApi(bp)

from . import (
    auth
)