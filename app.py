from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import click

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://snowy:Snowy_77@localhost/tims"
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

provinces = [
  '北京市',
  '天津市',
  '河北省',
  '山西省',
  '内蒙古自治区',
  '辽宁省',
  '吉林省',
  '黑龙江省',
  '上海市',
  '江苏省',
  '浙江省',
  '安徽省',
  '福建省',
  '江西省',
  '山东省',
  '河南省',
  '湖北省',
  '湖南省',
  '广东省',
  '广西壮族自治区',
  '海南省',
  '重庆市',
  '四川省',
  '贵州省',
  '云南省',
  '西藏自治区',
  '陕西省',
  '甘肃省',
  '青海省',
  '宁夏回族自治区',
  '新疆维吾尔自治区',
  '台湾省',
  '香港特别行政区',
  '澳门特别行政区'
];

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class TunnelInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(14), nullable=False, index=True)
    name = db.Column(db.String(20), nullable=False, index=True)
    length = db.Column(db.Integer)
    province = db.Column(db.String(10))
    lane = db.Column(db.Integer)
    year = db.Column(db.Integer)
    highway = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'name': self.name,
            'length': self.length,
            'province': self.province,
            'lane': self.lane,
            'year': self.year,
            'highway': self.highway
        }

class MaintainInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tunnel_name = db.Column(db.String(20), nullable=False, index=True)
    check_program = db.Column(db.String(20), nullable=False)
    check_time = db.Column(db.DateTime, nullable=False, index=True)
    check_name = db.Column(db.String(20))
    enter_man = db.Column(db.String(20))
    conclusion = db.Column(db.String(100))

@app.cli.command()
def forge():
    db.create_all()

    maintain_info = [
    {'number': 'G69U000610000', 'name': '秦岭终南山隧道', 'length': 22110, 'province': '陕西省', 
     'lane': 2, 'year': 2007, 'highway': '银百高速'},
    {'number': 'G85U000610000', 'name': '秦岭天台山隧道', 'length': 15560, 'province': '陕西省', 
     'lane': 3, 'year': 2021, 'highway': '银昆高速'},
    {'number': 'G85U000610000', 'name': '米仓山隧道', 'length': 13833, 'province': '陕西省', 
     'lane': 2, 'year': 2018, 'highway': '银昆高速'},
    {'number': 'G42U000510000', 'name': '二郎山隧道', 'length': 13469, 'province': '四川省', 
     'lane': 2, 'year': 2017, 'highway': '雅叶高速'},
    {'number': 'G42U000510000', 'name': '狮子坪隧道', 'length': 13156, 'province': '四川省', 
     'lane': 2, 'year': 2020, 'highway': '蓉昌高速'},
    {'number': 'G04U000140000', 'name': '虹梯关隧道', 'length': 13122, 'province': '山西省', 
     'lane': 2, 'year': 2013, 'highway': '安长高速'}
    ]

    for info in maintain_info:
        item = TunnelInfo(number=info['number'], name=info['name'], length=info['length'],
                          province=info['province'], lane=info['lane'], year=info['year'],
                          highway=info['highway'])
        db.session.add(item)

    db.session.commit()
    click.echo('Done.')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def signup(username, password):
    db.create_all() #Creates all tables

    user = User.query.filter_by(username=username).first()

    if user is not None:
        click.echo('Duplicate username!')
    else:
        click.echo('Creating user...')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo('Done.')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    return {'data': [info.to_dict() for info in TunnelInfo.query]}

@app.route('/tunnel/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        number = request.form['number']
        name = request.form['name']
        length = request.form['length']
        province = request.form['province']
        lane = request.form['lane']
        year = request.form['year']
        highway = request.form['highway']

        tunnel = TunnelInfo(number=number, name=name, length=length, province=province, 
                            lane=lane, year=year, highway=highway)
        db.session.add(tunnel)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add.html', provinces=provinces)

@app.route('/tunnel/edit/<int:tunnel_id>', methods=['GET', 'POST'])
def edit(tunnel_id):
    tunnel = TunnelInfo.query.get_or_404(tunnel_id)

    if request.method == 'POST':
        number = request.form['number']
        name = request.form['name']
        length = request.form['length']
        province = request.form['province']
        lane = request.form['lane']
        year = request.form['year']
        highway = request.form['highway']

        tunnel.number = number
        tunnel.name = name
        tunnel.length = length
        tunnel.province = province
        tunnel.lane = lane
        tunnel.year = year
        tunnel.highway = highway
        db.session.commit()
        return redirect(url_for('index')) 

    return render_template('edit.html', provinces=provinces, tunnel=tunnel)

@app.route('/tunnel/delete/<int:tunnel_id>', methods=['POST'])
def delete(tunnel_id):
    tunnel = TunnelInfo.query.get_or_404(tunnel_id)
    db.session.delete(tunnel)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.validate_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('用户名重复或密码错误')
        return redirect(url_for('login'))

    return render_template('login.html')