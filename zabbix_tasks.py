from zabbix_api import ZabbixAPI
from zabbix_api import Already_Exists
#import zabbix_api
import re
import sys

'''
Скрипт добавляет хосты (WS, SRV, VideoRecorder, Mikrotik) при открытии магазина

входные параметры скрипта:
    shopNumber - номер магазина
    shopNet - подсеть магазина (192.168.168.0)
    zabbixServer - сервер заббикса (http://192.168.3.8/zabbix)
    zabbixUser - Пользователь для авторизации на сервере
    zabbixPassword - Пароль для авторизации на сервере

'''

def addHostsToZabbix(shopNumber,shopNet,zabbixServer,zabbixUser,zabbixPassword):
    zapi = ZabbixAPI(server = zabbixServer)
    #TODO обработка исключения при недоступности сервера zabbix
    zapi.login(zabbixUser, zabbixPassword)

    #
    #создаём host для сервера
    #
    hostName = "shop%s_srv" % shopNumber
    visibleName = "Магазин %s Срв" % shopNumber
    groups = ['Shops', 'Shop servers', 'SetRetail']
    templates = ['Template OS Windows Shops','Template Shops Servers','Template_Set10-Windows-APP-Retail']
    ip = shopNet.replace('.0',".245")

    #Получаем groupid для groups
    groupsInfo = zapi.hostgroup.get({"filter":{"name":groups}})
    groupsid = [{"groupid":int(group.get('groupid'))} for group in groupsInfo]

    #Получаем gtempalteid для templates
    templatesInfo = zapi.template.get({"filter":{"name":templates}})
    templatesid = [{"templateid":int(template.get('templateid'))} for template in templatesInfo]
    try:
        zapi.host.create({"host":hostName,"name":visibleName,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"groups":groupsid,"templates":templatesid})
        print("Хост", hostName, "создан")
    except Already_Exists:
        print("Хост", hostName, "уже существует")
               

    #
    #создаём host для рабочей станции
    #
    hostName = "shop%s_ws" % shopNumber
    visibleName = "Магазин %s Рс" % shopNumber
    groups = ['Shops', 'Shop workstation', 'Domino']
    templates = ['Template Shops']
    ip = shopNet.replace('.0',".244")

    #Получаем groupid для groups
    groupsInfo = zapi.hostgroup.get({"filter":{"name":groups}})
    groupsid = [{"groupid":int(group.get('groupid'))} for group in groupsInfo]

    #Получаем gtempalteid для templates
    templatesInfo = zapi.template.get({"filter":{"name":templates}})
    templatesid = [{"templateid":int(template.get('templateid'))} for template in templatesInfo]
    try:
        zapi.host.create({"host":hostName,"name":visibleName,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"groups":groupsid,"templates":templatesid})
        print("Хост", hostName, "создан")
    except Already_Exists:
        print("Хост", hostName, "уже существует")
    #
    #создаём host для регистратора
    #
    hostName = "VR%s" % shopNumber
    visibleName = hostName
    groups = ['VideoRecorders']
    templates = ['Template_VideoRecorders']
    ip = shopNet.replace('.0',".240")

    #Получаем groupid для groups
    groupsInfo = zapi.hostgroup.get({"filter":{"name":groups}})
    groupsid = [{"groupid":int(group.get('groupid'))} for group in groupsInfo]

    #Получаем gtempalteid для templates
    templatesInfo = zapi.template.get({"filter":{"name":templates}})
    templatesid = [{"templateid":int(template.get('templateid'))} for template in templatesInfo]

    try:
        zapi.host.create({"host":hostName,"name":visibleName,"interfaces":[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":"10050"}],"groups":groupsid,"templates":templatesid})
        print("Хост", hostName, "создан")
    except Already_Exists:
        print("Хост", hostName, "уже существует")
