from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Length
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['password'], user['role'])
    return None

def get_db_connection():
    conn = sqlite3.connect('hgwbanners.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_remaining_time(end_date):
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    now = datetime.now()
    remaining_time = end_date_dt - now
    return remaining_time.days

@app.route('/')
def index():
    conn = get_db_connection()
    banners = conn.execute('SELECT * FROM hgwbanners').fetchall()
    conn.close()
    banners_with_remaining_time = []
    for banner in banners:
        banner_dict = dict(banner)
        remaining_time = calculate_remaining_time(banner['end_date'])
        if remaining_time > 0:
            banner_dict['remaining_time'] = remaining_time
            banners_with_remaining_time.append(banner_dict)
    return render_template('index.html', banners=banners_with_remaining_time)

@app.route('/api/banners', methods=['GET'])
def get_banners():
    conn = get_db_connection()
    banners = conn.execute('SELECT * FROM hgwbanners').fetchall()
    conn.close()
    banners_with_remaining_time = []
    for banner in banners:
        banner_dict = dict(banner)
        remaining_time = calculate_remaining_time(banner['end_date'])
        if remaining_time > 0:
            banner_dict['remaining_time'] = remaining_time
            banners_with_remaining_time.append(banner_dict)
    return jsonify(banners_with_remaining_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and user['password'] == password:
            user_obj = User(user['id'], user['username'], user['password'], user['role'])
            login_user(user_obj)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Form for adding a new banner
class BannerForm(FlaskForm):
    game_title = StringField('Game Title', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Banner')

@app.route('/add_banner', methods=['GET', 'POST'])
@login_required
def add_banner():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    form = BannerForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO hgwbanners (Game_title, Banner_type, Name, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (form.game_title.data, form.type.data, form.name.data, form.start_date.data, form.end_date.data))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_banner.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)