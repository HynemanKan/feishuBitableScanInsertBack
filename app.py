import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Config, Response, g, request
from werkzeug.exceptions import Unauthorized

from extensions import (
ext_login
)

from configs import app_config
from extensions.ext_login import login_manager
from libs.feishu.auth import get_tenant_access_token
from libs.passport import PassportService
from service.account_service import AccountService


class App(Flask):
    pass

def create_app_with_config()->Flask:
    app = App(__name__)
    app.config.from_mapping(app_config.model_dump())
    for key, value in app.config.items():
        if isinstance(value, str):
            os.environ[key] = value
        elif isinstance(value, int | float | bool):
            os.environ[key] = str(value)
        elif value is None:
            os.environ[key] = ""

    return app

def register_blueprints(app):
    from controllers.feishu import bp as feishu_bp
    from controllers.console import bp as console_bp
    app.register_blueprint(console_bp)
    app.register_blueprint(feishu_bp)


def create_app():
    app = create_app_with_config()
    #app.secret_key = app.config["SECRET_KEY"]
    log_handlers = None
    log_file = app.config.get("LOG_FILE")
    if log_file:
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)
        log_handlers = [
            RotatingFileHandler(
                filename=log_file,
                maxBytes=1024 * 1024 * 1024,
                backupCount=5,
            ),
            logging.StreamHandler(sys.stdout),
        ]

    logging.basicConfig(
        level=app.config.get("LOG_LEVEL"),
        format=app.config.get("LOG_FORMAT"),
        datefmt=app.config.get("LOG_DATEFORMAT"),
        handlers=log_handlers,
        force=True,
    )
    log_tz = app.config.get("LOG_TZ")
    if log_tz:
        from datetime import datetime

        import pytz

        timezone = pytz.timezone(log_tz)

        def time_converter(seconds):
            return datetime.utcfromtimestamp(seconds).astimezone(timezone).timetuple()

        for handler in logging.root.handlers:
            handler.formatter.converter = time_converter
    initialize_extensions(app)
    register_blueprints(app)
    return app

def initialize_extensions(app):
    ext_login.init_app(app)

@login_manager.request_loader
def load_user_from_request(request_from_flask_login):
    """Load user based on the request."""
    if request.blueprint in {"feishu"}:
        return None
    # Check if the user_id contains a dot, indicating the old format
    auth_header = request.headers.get("Authorization", "")
    if not auth_header:
        auth_token = request.args.get("_token")
        if not auth_token:
            raise Unauthorized("Invalid Authorization token.")
    else:
        if " " not in auth_header:
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")
        auth_scheme, auth_token = auth_header.split(None, 1)
        auth_scheme = auth_scheme.lower()
        if auth_scheme != "bearer":
            raise Unauthorized("Invalid Authorization header format. Expected 'Bearer <api-key>' format.")

    decoded = PassportService().verify(auth_token)
    account = AccountService.load_user_from_token(decoded)
    return account



@login_manager.unauthorized_handler
def unauthorized_handler():
    """Handle unauthorized requests."""
    return Response(
        json.dumps({"code": "unauthorized", "message": "Unauthorized."}),
        status=401,
        content_type="application/json",
    )

app=create_app()


@app.route("/health")
def health():
    return Response(
        json.dumps({"pid": os.getpid(), "status": "ok", "version": app.config["CURRENT_VERSION"]}),
        status=200,
        content_type="application/json",
    )


cache = {
    "tenant_access_token":""
}

@app.before_request
def before_request():
    g.tenant_access_token=cache["tenant_access_token"]

scheduler = BackgroundScheduler()

def refresh_token():
    logging.info("task feishu token refresh start")
    tenant_access_token = get_tenant_access_token(app.config["FEISHU_APP_ID"], app.config["FEISHU_APP_SECRET"])
    cache["tenant_access_token"] = tenant_access_token
    logging.info("task feishu token refresh finish")

refresh_token()

scheduler.add_job(refresh_token, 'interval', minutes=45)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)