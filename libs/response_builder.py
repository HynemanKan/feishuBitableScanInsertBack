from flask import jsonify


def success(data:dict):
    data.update({
        "code": "success", "message": "success."
    })
    return data