from flask import Blueprint

from libs.external_api import ExternalApi

bp = Blueprint("console", __name__, url_prefix="/api/v1/console/")
api = ExternalApi(bp)

from .auth import (
    feish_auth
)

from .action import (
    scan_enrich
)

from .datas import (
    bitable
)