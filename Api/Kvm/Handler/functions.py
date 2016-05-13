#coding=utf-8

import time,random,xml.dom.minidom

def curDatetime():
    '''生成时间格式'''
    return time.strftime('%Y-%m-%d %X', time.localtime())

def getStatusId(ident):
    '''虚拟机状态'''
    statusDIct = {1:'pending',2:'online',3:'down'}
    if ident and ident in statusDIct.keys():
        return statusDIct[ident]
    else:
        return ident

def randomMAC():
    mac = [0x52, 0x56,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def createXml(filename,hostname,uuid,memory,cpu,monip,mac,port):
    '''修改kvm模板文件'''
    oldxmlfile=open(filename)
    oldxml=oldxmlfile.read()
    oldxmlfile.close()
    doc = xml.dom.minidom.parseString(oldxml)
    doc.getElementsByTagName("name")[0].childNodes[0].data = hostname
    doc.getElementsByTagName("uuid")[0].childNodes[0].data = uuid
    doc.getElementsByTagName("memory")[0].childNodes[0].data = memory
    doc.getElementsByTagName("currentMemory")[0].childNodes[0].data = memory
    doc.getElementsByTagName("vcpu")[0].childNodes[0].data = cpu
    itemip = doc.getElementsByTagName("host")
    itemip[0].setAttribute("name",monip)
    itemmac = doc.getElementsByTagName("mac")
    itemmac[0].setAttribute("address",mac)
    itemport = doc.getElementsByTagName("graphics")
    itemport[0].setAttribute("port",port)
    newxml=doc.toprettyxml(newl='')
    xmlfile=open("/data/salt/kvm_manager/{0}.xml".format(hostname),"w")
    xmlfile.write(newxml)
    xmlfile.close()
