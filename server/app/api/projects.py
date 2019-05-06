from flask import jsonify, request, send_file
from io import BytesIO
from app import db
from app.models import Project
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import badRequest

@bp.route('/explore', methods=['GET', 'POST'])
def explore():
    pass


@bp.route('/projects/upload', methods=['POST'])
@token_auth.login_required
def upload():
    pass


@bp.route('/projects/download/<string:filename>')
@token_auth.login_required
def download(filename):
    project = Project.query.filter_by(filename).first_or_404()
    return send_file(project.file_data, mimetype='application/pdf', attachment_filename=project.title+'.pdf', as_attachment=True)

# Remove this method from here and redefine in the user-specific modules.
# It should return all the uploads done or supervised by a user
#
# @bp.route('/<string:username>/dashboard')
# @bp.route('/<string:username>/projects/uploads')
# @token_auth.login_required
# def userUploads(pass):
#     pass

@bp.route('/projects/request_approval', methods=['PUT'])
@token_auth.login_required
def requestApproval():
    pass

    
@bp.route('/projects/accept_approval_request', methods=['POST'])
@token_auth.login_required
def acceptApprovalRequest():
    pass


@bp.route('/projects/delete_project/<string:filename>', methods=['DELETE'])
@token_auth.login_required
def deleteProject(filename):
    pass