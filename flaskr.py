import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from zabbix_api import ZabbixAPI 

app = Flask(__name__)

DATABASE = 'db\\flask_test.db'

app.config.from_pyfile('config.ini', silent=True)


# def connect_db():
    # print DATABASE
    # return sqlite3.connect(app.config['DATABASE'])

# def init_db():
    # with app.app_context():
        # print ('Test')
        # ##print app.config['DATABASE']
        # with closing(connect_db()) as db:
            # with app.open_resource('D:\\Web\\flask_test\\db\\schema.sql', mode='r') as f:
                # db.cursor().executescript(f.read())
            # db.commit()

# @app.before_request
# def before_request():
    # g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
    # db = getattr(g, 'db', None)
    # if db is not None:
        # db.close()


@app.route('/')
def index():
    return render_template('adminlte_main.html')

#Вывод страницы для заведения нового магазина
@app.route('/newshop')
def newshop():
    return render_template('adminlte_newshop.html') 

#Обработка формы для для заведения нового магазина
@app.route('/fnewshop')
def fnewshop():
    sn = request.args.get('inShopNumber')
    flash('Номер магазина: ' + sn)
    return redirect(url_for('newshop')) 


@app.route('/zabbix')
def zabbix():
    #pass
    #Получаем список групп хостов с zabbix
    zapi = ZabbixAPI(server="http://192.168.3.9/zabbix/")
    zapi.login("Admin", "zabbix")
    hostgroups = zapi.hostgroup.get({"output":["name","groupid"], "real_hosts":True})
    return render_template('zabbix.html', hostgroups=hostgroups)


	
if __name__ == '__main__':
    app.run()

##import sys
##sys.path.append("D:\\Web\\flask_test")
