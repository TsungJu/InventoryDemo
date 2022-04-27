from datetime import datetime
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
import datetime
import bcrypt
from . import app
import psycopg2
import plotly.express as px
import pandas as pd
#app.secret_key = 'eb6ecd808fcc342793df99a753ed7292'
#app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please input account and password login.'

class User(UserMixin):
    pass

#users={'leolee':{'password':'passw0rd'}}

@login_manager.user_loader
def user_loader(enter_user):
    #if enter_user == None:
    #    return
    #if enter_user not in users:
    #    return
    user = User()
    user.id = enter_user
    return user

@login_manager.request_loader
def request_loader(request):
    flask_request_user = request.form.get('user_id')
    
    if flask_request_user == None:
        return
    #if flask_request_user not in users:
    #    return

    user = User()
    user.id = flask_request_user

    user.is_authenticated = bcrypt.checkpw(request.form['password'].encode('utf-8'), user[flask_request_user]['password'])
        
    #user.is_authenticated = request.form['password']==user[flask_request_user]['password']

    return user

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

        #access_token = create_access_token(identity=email)
        #user.update_one({"email":email},{'$set':{"last_login":datetime.datetime.now()}})
    
    user_id = request.form['user_id']
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT admin_password FROM admins where admin_name='"+user_id+"'")
    admin_password=cursor.fetchone()
    cursor.close()
    conn.close()
    if bcrypt.checkpw(request.form['password'].encode('utf-8'), admin_password[0].tobytes()):
        user = User()
        user.id = user_id
        login_user(user)
        flash(f'{user_id}! Welcome to join us !')
        return redirect(url_for('home',_external=True,_scheme=app.config['SCHEME']))
    
    flash('Login Failed...')
    return render_template('login.html')

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')

    if request.method == 'POST':
        admin_name = request.form['user_id']
        admin_password = bcrypt.hashpw((request.form["password"]).encode('utf-8'), bcrypt.gensalt())
        created_on = datetime.datetime.now()
        email = request.form['email']
        user_info = tuple((admin_name,admin_password,email,created_on,created_on))
        user_info_insert = list()
        user_info_insert.append(user_info)
        insert_admin_sql='''INSERT INTO admins (admin_name,admin_password,email,created_on,last_login) VALUES (%s,%s,%s,%s,%s)'''
        conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
        cursor = conn.cursor()
        cursor.executemany(insert_admin_sql,user_info_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home',_external=True,_scheme=app.config['SCHEME']))
    
    return render_template('admin.html')

@app.route('/logout')
def logout():
    current_login_user = current_user.get_id()
    logout_user()
    flash(f'{current_login_user}! Welcome to comeback!')
    return render_template("login.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

def get_widgets():
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM widgets")

    # this will extract row headers
    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    conn.close()

    return json_data

def web_select_specific(condition):
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    condition_query = []

    for key, value in condition.items():
        if value:
            condition_query.append(f"{key}={value}")
    
    if condition_query:
        condition_query = "WHERE " + ' AND '.join(condition_query)
    else:
        condition_query = ''

    mysql_select_query = f"""SELECT * FROM widgets {condition_query};"""
    print(mysql_select_query)

    cursor.execute(mysql_select_query)

    # this will extract row headers
    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    conn.close()

    return json_data

def web_select_overall():
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM widgets")

    '''message=[]
    while True:
        temp = cursor.fetchmany(10)

        if temp:
            message.extend(temp)
        else:
            break
    '''
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return results

def get_unique(table):
    unique_name = {i[0] for i in table}
    unique_description = {i[1] for i in table}
    return sorted(unique_name),sorted(unique_description)

def get_products():
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")

    # this will extract row headers
    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()
    conn.close()

    df_data = pd.DataFrame(results,columns =['product_id', 'product_name', 'product_description','product_price','product_amount'])
    fig = px.histogram(df_data, x='product_name', y='product_amount')

    #print(fig.to_html())

    return json_data,fig.to_html()
    
@app.route("/select_widgets_select_opt",methods=['GET','POST'])
@login_required
def select_widgets_select_opt():
    if request.method == 'POST':
        python_widgets = web_select_specific(request.form)
        return render_template("show_widgets.html",widgets=python_widgets)
    else:
        table = web_select_overall()
        uniques = get_unique(table)
        return render_template("select_widgets_select_opt.html",login=current_user.is_authenticated,uniques=uniques)

@app.route("/select_widgets",methods=['GET','POST'])
@login_required
def select_widgets():
    if request.method == 'POST':
        python_widgets = web_select_specific(request.form)
        return render_template("show_widgets.html",widgets=python_widgets)
    else:
        return render_template("select_widgets.html",login=current_user.is_authenticated)

@app.route('/widgets')
@login_required
def show_widgets():
    widgets=get_widgets()
    return render_template("show_widgets.html",widgets=widgets)

@app.route('/products')
@login_required
def products():
    products,products_fig=get_products()
    return render_template("products.html",products=products,products_fig=products_fig)

@app.route('/product_create',methods=['GET','POST'])
@login_required
def product_create():
    if request.method == 'POST':
        conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
        cursor = conn.cursor()
        cursor.execute("select max(product_id) from products")
        max_product_id=cursor.fetchone()[0]
        product_id = max_product_id + 1
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_price = request.form['product_price']
        product_amount = request.form['product_amount']
        product_info = tuple((product_id,product_name,product_description,product_price,product_amount))
        product_info_insert = list()
        product_info_insert.append(product_info)
        insert_product_sql='''INSERT INTO products (product_id,product_name,product_description,product_price,product_amount) VALUES (%s,%s,%s,%s,%s)'''
        cursor.executemany(insert_product_sql,product_info_insert)
        conn.commit()
        cursor.close()
        conn.close()

    products,products_fig=get_products()
    return render_template("products.html",products=products,products_fig=products_fig)

@app.route('/initdb')
def db_init():
    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255));")
    #Insert multiple rows
    insert_multiple_rows_sql="INSERT INTO widgets (name,description) VALUES (%s,%s)"
    val = [
        ('Peter', 'Lowstreet 4'),
        ('Amy', 'Apple st 652'),
        ('Hannah', 'Mountain 21'),
        ('Michael', 'Valley 345'),
        ('Sandy', 'Ocean blvd 2'),
        ('Betty', 'Green Grass 1'),
        ('Richard', 'Sky st 331'),
        ('Susan', 'One way 98'),
        ('Vicky', 'Yellow Garden 2'),
        ('Ben', 'Park Lane 38'),
        ('William', 'Central st 954'),
        ('Chuck', 'Main Road 989'),
        ('Viola', 'Sideway 1633')
    ]
    cursor.executemany(insert_multiple_rows_sql,val)
    conn.commit()
    cursor.close()
    conn.close()

    return 'init database'
