from flask import Blueprint, request

infosCEMB_bp = Blueprint('infosCEMB', __name__)

@infosCEMB_bp.route("/infosCEMB", methods=["POST", "GET"])
def infosCEMB():
    cemb = request.json
    print(cemb)
    return {"success": True}