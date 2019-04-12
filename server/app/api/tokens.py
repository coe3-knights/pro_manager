from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def getToken():
    token = g.current_user.getToken()
    db.session.commit()
    return jsonify({'Bearer': g.current_user.username, 'token': token})

@bp.route('/tokens', methods=['DELETE'])
@basic_auth.login_required
def revokeToken():
    g.current_user.revokeToken()
    db.session.commit()
    return '' + 204
