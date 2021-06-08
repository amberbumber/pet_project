from app import db
from app.api import bp
from app.models import User
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify, request, url_for, current_app


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user = User.query.get_or_404(id)
    data = User.to_collection_dict(user.followers, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user = User.query.get_or_404(id)
    data = User.to_collection_dict(user.followed, page, per_page, 'api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email')
    # создаем нового пользователя и заполняем его атрибуты
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    # формируем ответ
    current_app.logger.info('New user: login  ' + data['username'])
    response = jsonify(user.to_dict())
    response.code_status = 210     # код 210 используется, когда новый объект был успешно создан
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())