from flask import jsonify, request, send_file, url_for, current_app
from io import BytesIO
from app import db
from app.models import Project, User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import badRequest
from flask_login import current_user


@bp.route('/explore', methods=['GET', 'POST'])
def explore():
    pass


@bp.route('/projects/<int:id>')
def getProjectInfo(id):
    project = Project.query.get_or_404(id).first()

    if current_user.is_authenticated and current_user==project.author:
        response = jsonify(project.toDict(public=False))
        response.status_code = 200
        return response

    response = jsonify(project.toDict())
    response.status_code = 200
    return response



@bp.route('/projects/upload', methods=['POST'])
@token_auth.login_required
def upload(response):
    file = request.files['input_file']

    new_project = Project()
    new_project.owner = current_user.id
    new_project.title = request.form.get('project_title')
    if new_project.title == None:
        new_project.title = file.filename.split('.',1)[0]
    new_project.hashFilename(file.filename)
    new_project.file_data = file.read()

    db.session.add(new_project)
    db.session.commit()
    #response = jsonify(new_project.toDict(public=False))
    response.status_code = 201
    response.headers['Location'] = url_for('api.getProjectInfo', id=new_project.id)
    return response
    

@bp.route('/projects/download/<string:filename>')
@token_auth.login_required
def download(filename):
    project = Project.query.filter_by(filename=filename).first()
    return send_file(project.file_data, mimetype='application/pdf', attachment_filename=project.title+'.pdf', as_attachment=True)

@bp.route('/projects/search')
def search():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    payload = Project.query.whoosh_search(q).paginate(page, current_app.config['PROJECTS_PER_PAGE'], False) or []
    response = jsonify(payload)
    response.status_code = 200
    return response


# @bp.route('/projects/request_approval', methods=['PUT'])
# @token_auth.login_required
# def requestApproval():
#     pass

    
# @bp.route('/projects/accept_approval_request', methods=['POST'])
# @token_auth.login_required
# def acceptApprovalRequest():
#     pass


@bp.route('/projects/delete_project/<string:filename>', methods=['DELETE'])
@token_auth.login_required
def deleteProject(filename):
    pass