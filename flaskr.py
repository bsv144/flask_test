import paramiko
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from zabbix_api import ZabbixAPI 
from flask_simpleldap import LDAP
import ldap

app = Flask(__name__)

app.config.from_pyfile('config.ini', silent=True)

ldap = LDAP(app)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        # This is where you'd query your database to get the user info.
        g.user = {}
        # Create a global with the LDAP groups the user is a member of.
        g.ldap_groups = ldap.get_user_groups(user=session['user_id'])

@app.route('/login', methods=['GET','POST'])
def login(): pass

@app.route('/')
def index():
    return render_template('index.html')

#Вывод страницы для заведения нового магазина
@app.route('/newshop')
def newshop():
    return render_template('adminlte_newshop.html') 

#Обработка формы для для заведения нового магазина
@app.route('/fnewshop')
def fnewshop():
    #TODO валидация данных с формы. Если ошибка возвращаем
    #исходную страницу с сообщением о необходимости правильном заполнении формы
    ##Создаём ключи и конфигурацию openvpn
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
    	client.connect(hostname=app.config['SSH_OPENVPN'], username=app.config['SSH_OPENVPN_USER'], password=app.config['SSH_OPENVPN_PASSWORD'])
    except:
    	#raise e
    	data = "Error connect to openvpn server sys.exc_info()[0]"
    stdin, stdout, stderr = client.exec_command('/etc/openvpn/makeovpnclient.sh snb net/mask'.format(snb=SHOPNUMBER,net=NET,mask=MASK))
    #TODO checkout stderr for correct  script output
    data = stdout.read() + stderr.read()
    client.close()
    ##TODO Создаём учётку в AD
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
    	client.connect(hostname=app.config['SSH_WINADMIN'], username=app.config['SSH_WINADMIN_USER'], password=app.config['SSH_WINADMIN_PASSWORD'])
    except:
    	#raise e
    	data = "Error connect to openvpn server sys.exc_info()[0]"
    stdin, stdout, stderr = client.exec_command('new-aduser')
    
    

    ##TODO Создаём номер на FreePBX
    ##TODO make email
    ##TODO make mikrotik config
    sn = request.args.get('inShopNumber')
    flash('Номер магазина: ' + data.decode("utf-8"))
    return redirect(url_for('newshop')) 


@app.route('/zabbix')
def zabbix():
    #pass
    #Получаем список групп хостов с zabbix
    zapi = ZabbixAPI(server=app.config['ZABBIX_SERVER'])
    zapi.login(app.config['ZABBIX_USER'], app.config['ZABBIX_PASSWORD'])
    hostgroups = zapi.hostgroup.get({"output":["name","groupid"], "real_hosts":True})
    return render_template('zabbix.html', hostgroups=hostgroups)


	
if __name__ == '__main__':
    app.run()