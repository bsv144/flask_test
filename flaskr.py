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
    	client.connect(hostname=app.config['FNEWSHOP_SSH_HOST'], username=app.config['FNEWSHOP_SSH_USER'], password=app.config['FNEWSHOP_SSH_PASSWORD'])
    except:
    	#raise e
    	data = "Error connect to openvpn server sys.exc_info()[0]"
    stdin, stdout, stderr = client.exec_command('ls -l')
    #TODO checkout stderr for correct  script output
    data = stdout.read() + stderr.read()
    client.close()
    ##TODO Создаём учётку в AD
    con = ldap.initialize('ldap://localhost:389', bytes_mode=False)
    con.simple_bind_s('login', 'secret_password')
	# The dn of our new entry/object
	dn="cn=replica,dc=example,dc=com" 
	# A dict to help build the "body" of the object
	attrs = {}
	attrs['objectclass'] = ['top','organizationalRole','simpleSecurityObject']
	attrs['cn'] = 'replica'
	attrs['userPassword'] = 'aDifferentSecret'
	attrs['description'] = 'User object for replication using slurpd'
	# Convert our dict to nice syntax for the add-function using modlist-module
	ldif = modlist.addModlist(attrs)
	# Do the actual synchronous add-operation to the ldapserver
	l.add_s(dn,ldif)
	# Its nice to the server to disconnect and free resources when done
	l.unbind_s()

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