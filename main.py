from flask import Flask, redirect, url_for, session, request, jsonify,render_template
from authlib.integrations.flask_client import OAuth
import os
import requests
import setting
import mysql.connector
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect( **setting.my_sql_setting )

cursor = conn.cursor()
if conn.is_connected():
    print("Connection successful!")
else:
    print("Connection failed!")

cursor.execute("USE login_db;")
cursor.execute("SELECT * FROM login;")
cursor.fetchall()

# 配置 OAuth
oauth = OAuth(app)
oauth.register(**setting.google_os_setting) #*:list,tuple ; ** dict
oauth.register(**setting.github_os_setting)

@app.route('/')
def index():
    return render_template("login_page.html") #首頁

@app.route('/index')
def index2():
    return render_template('test.html')#登入頁面

#選擇登入方式
@app.route("/login/<provider>")
def login(provider):
    if provider not in oauth._clients:
        return 'provider not found',404
    redirect_uri = "http://127.0.0.1:8080/auth/callback/"+str(provider)#url_for('auth_callback',provider=provider,_external = True)
    print(redirect_uri)
    return oauth.create_client(provider).authorize_redirect(redirect_uri)


@app.route("/auth/callback/<provider>")
def auth_callback(provider):
    try:
        if provider not in oauth._clients:
            return 'provider not found',404
        
        token = oauth.create_client(provider).authorize_access_token()

        if provider =="google":
            userinfo_response = oauth.google.get('https://openidconnect.googleapis.com/v1/userinfo') #get用網址
        elif provider =="github":
            print("hah")
            userinfo_response = oauth.github.get('https://api.github.com/user') #get用網址
        
        user_info = userinfo_response.json()
        session['user'] = user_info

        try:
            cursor.execute("INSERT INTO login (name, email) VALUES (%s, %s)", (user_info['name'], user_info['email']))
            conn.commit()
            cursor.execute("SELECT * FROM login WHERE email = %s", (user_info['email'],))
            result = cursor.fetchall()
            for row in result:
                print(row)
        except mysql.connector.Error as err:
            print(f"Error: {err}")        
        
        return render_template("login_success.html",user = user_info) #顯示登入成功

    except Exception as e:
        return f'an error occured:{str(e)}',400
    
@app.route('/dump')
def dump():
    query = "SELECT * FROM login"
    df = pd.read_sql(query, conn)
    df.to_csv('export.csv', index=False)
    return 'dump successfully'

@app.route('/dump/json')
def dump_json():
    cursor.execute("SELECT * FROM login")
    data=cursor.fetchall()
    for e in data:
        json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), default=str)
    return 'nice'
        

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0',debug=True)
