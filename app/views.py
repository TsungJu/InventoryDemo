from datetime import datetime

from flask import Flask, render_template, request

from . import app
import mysql.connector
import json

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

def get_widgets():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM widgets")

    # this will extract row headers
    row_headers=[x[0] for x in cursor.description]

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json_data

def web_select_specific(condition):
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor=mydb.cursor()

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

    return json_data

def web_select_overall():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

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

    return results

def get_unique(table):
    unique_name = {i[0] for i in table}
    unique_description = {i[1] for i in table}
    return sorted(unique_name),sorted(unique_description)

@app.route("/select_widgets_select_opt",methods=['GET','POST'])
def select_widgets_select_opt():
    if request.method == 'POST':
        python_widgets = web_select_specific(request.form)
        return render_template("show_widgets.html",widgets=python_widgets)
    else:
        table = web_select_overall()
        uniques = get_unique(table)
        return render_template("select_widgets_select_opt.html",uniques=uniques)

@app.route("/select_widgets",methods=['GET','POST'])
def select_widgets():
    if request.method == 'POST':
        python_widgets = web_select_specific(request.form)
        return render_template("show_widgets.html",widgets=python_widgets)
    else:
        return render_template("select_widgets.html")

@app.route('/widgets')
def show_widgets():
    widgets=get_widgets()
    return render_template("show_widgets.html",widgets=widgets)

@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        password="p@ssw0rd1",
        database="inventory"
    )
    cursor=mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
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
    mydb.commit()
    cursor.close()

    return 'init database'
