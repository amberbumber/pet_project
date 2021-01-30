from app import  db
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.main.forms import  EditProfileForm, PostForm, EmptyForm, SearchForm, MessageForm
from app.translate import translate, detect_lang
from flask_login import current_user, login_required
from app.models import User, Post, Message, Notification
from datetime import datetime
from flask_babel import _, get_locale
from app.main import bp
import time
from threading import Thread


# запись последнего времени активности пользователя
@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())


# @app.route
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        # try:
        language = detect_lang(form.post.data)
        # except:
        #     language = ''
        # language = guess_language(form.post.data)
        # if language == 'UNKNOWN' or len(language) > 5:
        #     language = ''
        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Ваш пост успешно опубликован!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_post().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title=_('Домашняя страница'),  form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)
    # user = {'username': 'Anna'}
    # posts = [
    #     {
    #         'author': {'username': 'Зинаида'},
    #         'body': 'Вот это красота!!'
    #     },
    #     {
    #         'author': {'username': 'Ипполит'},
    #         'body': 'Я готовил рыбу'
    #     },
    # ]


# функция просмотра всех постов
@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title=_('Explore'), posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/test')
def test():
    return render_template('testpage.html')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}
    # ]
    form = EmptyForm()
    return render_template('user.html', title=str(user.username), form=form, user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    form=EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Изменения успешно сохранены'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, title=_('Редактировать профиль'))


@bp.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('Пользователь %(username)s не найден', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('Вы не можете подписаться на самого себя'))
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(_('Вы подписались на пользователя %(username)s!', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(_('Пользователь %(username)s не найден', username=username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash(_('Вы не можете отписаться от самого себя'))
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(_('Вы успешно отписались от пользователя %(username)s', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))



@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    # return jsonify({'text': translate(request.form['text'],
    #                                   request.form['source_lang'],
    #                                   request.form['dest_lang'])})

    # get_token()
    return jsonify(translate(request.form['text'],
                             request.form['source_lang'],
                             request.form['dest_lang']))


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user, body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Ваше сообщение было отправлено пользователю {}'.format(recipient)))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Отправить сообщение'), form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    # messages = Message.query.order_by(Message.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    messages = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('messages.html', title=_('Сообщения'), messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(Notification.timestamp >= since).order_by(
        Notification.timestamp.asc())
    print([{
        'user': n.user_id,
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])


@bp.route('/read_message')
@login_required
def read_message():
    message_id = request.args.get('id', 0, type=int)
    message = Message.query.filter_by(id=message_id).first_or_404()
    if message.recipient_id != current_user.id:
        return jsonify({'access': 'denied'})
    message.is_new = False
    db.session.commit()
    return jsonify({
        'message_id': message.id,
        'message_is_new': message.is_new})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page-1) \
        if page > 1 else None
    return render_template('search.html', title=_('Поиск'), posts=posts, next_url=next_url, prev_url=prev_url)


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('Экспорт сейчас в процессе. Дождитесь завершения текущего экспорта и попробуйте снова.'))
    else:
        current_user.launch_task('export_posts', _('Выгружаем посты...'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))
