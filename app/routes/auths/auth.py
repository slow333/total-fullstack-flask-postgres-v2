from flask import (
    Blueprint, request, render_template as render, current_app,
    redirect, flash, url_for # type: ignore
    )
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from itsdangerous import TimedSerializer as Serializer # type: ignore
from flask_mail import Message # type: ignore
from flask_login import login_user, logout_user, login_required, current_user
from app import mail
from ... import db
from ...models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register_users():
    if request.method == 'GET':
        return render('apps/auth/register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(username=username).first()

        if user:
            flash(f'User {username} is already registered.')
            return render('apps/auth/register.html')
        if confirm_password != password:
            flash('Passwords do not match.')
            return render('apps/auth/register.html')
        else:
            user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('auth.login_users'))

@bp.route('/login', methods=['GET','POST'])
def login_users():
    if request.method == 'GET':
        return render('apps/auth/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'
        
        if error is None:
            login_user(user)
            flash(f'Welcome, {user.username}!')
            return redirect('/apps/')
        else:
            flash(error)
            return render('apps/auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/apps/')

@bp.route('/account', methods=['GET','POST'])
@login_required
def account():
    if request.method == 'GET':
        return render('apps/auth/account.html', user=current_user)
    
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        # username은 변경못하고, email만 변경 가능하게
        if current_user.email == email:
            flash(f'User {email} is already registered.')
            return render('apps/auth/account.html', user=current_user)

        current_user.email = email
        db.session.commit()
        flash('Your account has been updated.')
        return redirect(url_for('auth.account'))
@bp.route('/')
def index():
    return redirect('/apps/')
# 암호 변경 기능 --------------------------------
def get_reset_token(user_id, expiration=1800):
    s = Serializer(current_app.config.get('SECRET_KEY'), expiration)
    return s.dumps({'user_id': user_id}).decode('utf-8')

def verify_reset_token(token):
    s = Serializer(current_app.config.get('SECRET_KEY'))
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)

def send_email(user):
    token = get_reset_token(user.id)
    msg = Message('Reset Your Password', 
                  recipients=[user.email], 
                  sender=current_app.config.get('MAIL_USERNAME') or 'noreply@demo.com')
    msg.body = f'''
To reset your password, visit the following link:
{url_for('auth.reset_with_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)

@bp.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if request.method == 'GET':
        return render('apps/auth/reset_request.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash('No account found with that email address.')
            return render('apps/auth/reset_request.html')

        send_email(user)
        flash('A password reset link has been sent to your email address.')
        return redirect('/auth/login')

@bp.route('/reset_password/<token>', methods=['GET','POST'])
def reset_with_token(token):
    user = verify_reset_token(token)
    if user is None:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.reset_password'))
    if request.method == 'GET':
        return render('apps/auth/reset_with_token.html', token=token)
    elif request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match.')
            return render('apps/auth/reset_with_token.html', token=token)
        
        user.password = generate_password_hash(password)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
