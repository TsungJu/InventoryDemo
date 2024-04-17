from datetime import datetime
import os
import json
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
import datetime,time
import bcrypt
from . import app
import psycopg2
import plotly.express as px
import pandas as pd
import requests
#app.secret_key = 'eb6ecd808fcc342793df99a753ed7292'
#app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please input account and password login.'

class User(UserMixin):
    def __init__(self):
        self._is_admin = False

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = value
    
    @is_admin.deleter
    def is_admin(self):
        del self._is_admin

#users={'leolee':{'password':'passw0rd'}}

@login_manager.user_loader
def user_loader(enter_user):
    if enter_user == None:
        return
    #if enter_user not in users:
    #    return
    user = User()
    user.id = enter_user

    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT account_role FROM accounts where account_name='"+enter_user+"'")
    account_role = cursor.fetchone()
    cursor.close()
    conn.close()
    try:
        user.is_admin = account_role[0] == "admin"
    except TypeError:
        return

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

    conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
    cursor = conn.cursor()
    cursor.execute("SELECT account_password FROM accounts where account_name='"+flask_request_user+"'")
    account_password = cursor.fetchone()
    cursor.close()
    conn.close()
    try:
        user.is_authenticated = bcrypt.checkpw(request.form['password'].encode('utf-8'), account_password[0].tobytes())
    except TypeError:
        return
    print(user.is_admin)
    #user.is_authenticated = request.form['password']==user[flask_request_user]['password']

    return user

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("home.html")

        #access_token = create_access_token(identity=email)
        #user.update_one({"email":email},{'$set':{"last_login":datetime.datetime.now()}})
    if request.method == 'POST':
        user_id = request.form['user_id']
        conn = None
        try:
            conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
            cursor = conn.cursor()
            sql = """ SELECT account_password
                    FROM accounts
                    where account_name=%s """
            cursor.execute("SELECT account_password FROM accounts where account_name='"+user_id+"'")
            # cursor.execute(sql,str(user_id))
            admin_password=cursor.fetchone()
            print(admin_password)
            # cursor.close()
            # conn.close()
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), admin_password[0].tobytes()):
                user = User()
                user.id = user_id
                login_user(user)
                flash(f'{user_id}! Welcome to join us !')
                cursor.execute("UPDATE accounts SET last_login=\'"+str(datetime.datetime.now())+"\' where account_name='"+user_id+"'")
                conn.commit()
                cursor.close()
                return redirect(url_for('home',_external=True,_scheme=app.config['SCHEME'],login=current_user.is_authenticated))
            else:
                flash('Login Failed...')
                return render_template('home.html')
        except TypeError:
            flash('Login Failed...')
            return render_template('home.html')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                print("Close db connect!")
                conn.close()

def get_accounts():
    conn = None
    try:
        conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
        cursor = conn.cursor()
        sql = """ SELECT *
                FROM accounts """
        cursor.execute(sql)

        # this will extract row headers
        row_headers=[x[0] for x in cursor.description]

        results = cursor.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(row_headers,result)))

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    finally:
        if conn is not None:
            print("Close db connect!")
            conn.close()

    return json_data

@app.route('/manage',methods=['GET','POST'])
@login_required
def manage():
    if request.method == 'GET':
        accounts=get_accounts()
        return render_template('manage.html',accounts=accounts, login=current_user.is_authenticated)

    if request.method == 'POST':
        account_name = request.form['user_id']
        account_password = bcrypt.hashpw((request.form["password"]).encode('utf-8'), bcrypt.gensalt())
        created_on = datetime.datetime.now()
        print(created_on)
        email = request.form['email']
        role = request.form['role']
        user_info = tuple((account_name,account_password,role,email,created_on,created_on))
        user_info_insert = list()
        user_info_insert.append(user_info)
        insert_account_sql='''
                        INSERT INTO accounts (account_name,account_password,account_role,email,created_on,last_login)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        '''
        conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
        cursor = conn.cursor()
        cursor.executemany(insert_account_sql,user_info_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home',_external=True,_scheme=app.config['SCHEME'],login=current_user.is_authenticated))
    
@app.route('/logout')
def logout():
    current_login_user = current_user.get_id()
    logout_user()
    flash(f'{current_login_user}! Welcome to comeback!')
    return render_template("home.html")

@app.route("/")
@app.route("/home")
def home():
    if login:
        return render_template("home.html", login = current_user.is_authenticated)
    else:
        return render_template("home.html")

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

@app.route("/prods",methods=['GET'])
@login_required
def prods():
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

    return jsonify(products=json_data), 200
    
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
    return render_template("products.html", products=products, products_fig=products_fig, login=current_user.is_authenticated)
    #return redirect(url_for('products',products=products,products_fig=products_fig,_external=True,_scheme=app.config['SCHEME']))

@app.route('/factory')
@login_required
def factory():
    return render_template("factory.html", login=current_user.is_authenticated)
    #return redirect(url_for('factory',_external=True,_scheme=app.config['SCHEME']))

@app.route('/sales')
@login_required
def sales():
    return render_template("sales.html", login=current_user.is_authenticated)
    #return redirect(url_for('sales',_external=True,_scheme=app.config['SCHEME']))

@app.route('/upload',methods=['GET'])
@login_required
def upload():
    """
    if request.method == 'POST':
        f = request.files['file']
        response = requests.post("http://"+app.config['API_SERVER']+"/api/guest/upload",files = {"file": (f.filename, f.stream, f.mimetype)})
        print(json.loads(response.text))
        return render_template("upload.html",filelist=json.loads(response.text))
    else:
        response = requests.get("http://"+app.config['API_SERVER']+"/api/guest/uploaded")
        return render_template("upload.html",filelist=json.loads(response.text))
    """
    return render_template("upload.html",apiServer=app.config['API_SERVER'], current_login_user = current_user.get_id(), login=current_user.is_authenticated)
    #return redirect(url_for('upload',apiServer=app.config['API_SERVER'],current_login_user = current_user.get_id(),_external=True,_scheme=app.config['SCHEME']))

@app.route('/product_create',methods=['GET','POST'])
@login_required
def product_create():
    if request.method == 'POST':
        conn = psycopg2.connect(app.config['DATABASE_URL'], sslmode=app.config['SSL_MODE'])
        cursor = conn.cursor()
        cursor.execute("select max(product_id) from products")
        max_product_id=cursor.fetchone()[0]
        if max_product_id == None:
            max_product_id = 1
        product_id = max_product_id + 1
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_price = request.form['product_price']
        product_amount = request.form['product_amount']
        product_info = tuple((product_id,product_name,product_description,product_price,product_amount))
        product_info_insert = list()
        product_info_insert.append(product_info)
        insert_product_sql='''
                            INSERT INTO products
                            (product_id,product_name,product_description,product_price,product_amount)
                            VALUES (%s,%s,%s,%s,%s)
                            '''
        cursor.executemany(insert_product_sql,product_info_insert)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("products",_external=True,_scheme=app.config['SCHEME'],login=current_user.is_authenticated))
