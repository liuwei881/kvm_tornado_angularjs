#coding=utf-8

from lib.urlmap import urlmap
from lib.basehandler import RESTfulHandler
from tornado import web,gen
from Kvm.Entity.KvmModel import ParentkvmList,KvmList,MirrorList,\
    SecretKeyList,ZcloudSizeList,MirrorSizeList,SnapshotList,CloudDiskList,\
    CloudDiskSnapList,RollBackList,ProjectsList,pro_user_relation,auth_user
import json,salt.client
import random,time,uuid
from Kvm import tasks
from functions import curDatetime,randomMAC,createXml
from sqlalchemy import desc,or_,and_

#服务器资产统计
@urlmap(r'/assets\/?([0-9]*)')
class AssetsHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(ParentkvmList).get(ident)
                self.Result['rows'] = objServer.toDict()
                self.Result['total'] = 1
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            page = int(self.get_argument('page', 1))
            searchKey = self.get_argument('searchKey', None)
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            totalquery = self.db.query(ParentkvmList.ParentId)
            ParentkvmlistObj = self.db.query(ParentkvmList)
            if searchKey:
                totalquery = totalquery.filter(or_(ParentkvmList.ParentName.like('%%%s%%' % searchKey),ParentkvmList.OsVersion.like('%%%s%%' % searchKey)))
                ParentkvmlistObj = ParentkvmlistObj.filter(or_(ParentkvmList.ParentName.like('%%%s%%' % searchKey),ParentkvmList.OsVersion.like('%%%s%%' % searchKey)))

            self.Result['total'] = totalquery.count()
            serverTask = ParentkvmlistObj.order_by(desc(ParentkvmList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

    @web.asynchronous
    def put(self, ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(ParentkvmList).get(ident)
        if ident and objTask:
            objTask.ParentName= data['params'].get('ParentName', None)
            objTask.Ip= data['params'].get('Ip', None)
            objTask.Ip1 = data['params'].get('Ip1', None)
            objTask.Ip2 = data['params'].get('Ip2', None)
            objTask.ParentLocation = data['params'].get('ParentLocation', None)
            objTask.OsVersion = data['params'].get('OsVersion', None)
            objTask.MemoryInfo = data['params'].get('MemoryInfo', None)
            objTask.DiskInfo = data['params'].get('DiskInfo', None)
            objTask.ModelName = data['params'].get('ModelName', None)
            objTask.CpuCore = data['params'].get('CpuCore', None)
            objTask.Sorts = data['params'].get('Sorts', None)
            self.db.add(objTask)
            self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)

#虚拟机管理
@urlmap(r'/vms\/?([0-9]*)')
class VmsHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(KvmList).get(ident)
                self.Result['rows'] = objServer.toDict()
                self.Result['total'] = 1
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            username = self.get_current_user()
            page = int(self.get_argument('page', 1))
            searchKey = self.get_argument('searchKey', None)
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            if username == 'admin':
                totalquery = self.db.query(KvmList.KvmId)
                KvmlistObj = self.db.query(KvmList)
                if searchKey:
                    totalquery = totalquery.filter(or_(KvmList.CloudName.like('%%%s%%' % searchKey),KvmList.Ip.like('%%%s%%' % searchKey),KvmList.MainHost.like('%%%s%%' % searchKey)))
                    KvmlistObj = KvmlistObj.filter(or_(KvmList.CloudName.like('%%%s%%' % searchKey),KvmList.Ip.like('%%%s%%' % searchKey),KvmList.MainHost.like('%%%s%%' % searchKey)))
                self.Result['total'] = totalquery.count()
                serverTask = KvmlistObj.order_by(desc(KvmList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
                self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
                self.finish(self.Result)
            else:
                User = self.db.query(auth_user).filter(auth_user.UserName==username).first()
                Pro = self.db.query(pro_user_relation).filter(pro_user_relation.UserId==User.Id).all()
                pro_id = [ i.ProjectId for i in Pro ]
                project = self.db.query(ProjectsList).filter(ProjectsList.ProId.in_(pro_id)).all()
                project_name = [p.ProName for p in project]
                self.Result['defaults'] = project_name[0]
                self.Result['projects'] = project_name
                KvmlistObj = self.db.query(KvmList).filter(KvmList.ProjectsName.in_(project_name))
                if searchKey:
                    KvmlistObj = KvmlistObj.filter(or_(KvmList.CloudName.like('%%%s%%' % searchKey),KvmList.Ip.like('%%%s%%' % searchKey),KvmList.MainHost.like('%%%s%%' % searchKey)))
                self.Result['total'] = KvmlistObj.count()
                serverTask = KvmlistObj.order_by(desc(KvmList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
                self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
                self.finish(self.Result)

    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        local = salt.client.LocalClient()
        host_status = local.cmd("computer[1-6,11]*-112-*.iprun.com","grains.item", ["freemem"])     #freemem为自己定义
        h = random.choice(host_status.items())
        memory = int(h[1].values()[0].strip("G").split(".")[0])
        if memory <= 3:
            self.write(json.dumps({"status":200,"msg":u"内存不够，请重新创建"}))
        else:
            objTask = KvmList()
            objTask.VirDisk = data['params'].get('VirDisk', None)
            objTask.MirrorName = data['params'].get('MirrorName', None).get('name',None)
            objTask.CloudName = data['params'].get('CloudName', None)
            objTask.ProjectsName = data['params'].get('ProjectsName', None)
            objTask.Mac = randomMAC()
            objTask.HostName = time.strftime('%Y%m%d_%H-%M-%S', time.localtime())
            secret = self.db.query(SecretKeyList).filter(SecretKeyList.ProjectsName == objTask.ProjectsName)
            objTask.SecretName = ",".join([i.SecretkeyName for i in secret])
            objTask.MainHost = h[0]
            objTask.HostStatus = 1
            objTask.CreateTime = curDatetime()
            hostname=objTask.HostName
            cpu = str(objTask.VirDisk.split("_")[0][0])
            memory = str(int(objTask.VirDisk.split("_")[1][0]) * 1024 * 1024)
            pro = self.db.query(ProjectsList).filter(ProjectsList.ProName == objTask.ProjectsName).first()
            allocated_cpu_now = pro.Vcpu + int(cpu)
            allocated_memory_now = pro.Vmemory + int(objTask.VirDisk.split("_")[1][0])
            allocated_kvm_count = pro.Cconfig + 1
            mac = objTask.Mac
            monip = random.choice(['10.10.111.1','10.10.111.2','10.10.111.4'])
            port = str(random.randint(5910,6000))
            if allocated_cpu_now < pro.Ccpu and allocated_memory_now < pro.Cmemory:
                if objTask.MirrorName in ('centos6','centos6lnmp','ruby-base','data-zi','centos7','ubuntu'):
                    createXml("/data/salt/kvm_manager/centos6_template.xml",hostname,uuid.uuid1(),memory,cpu,monip,mac,port)
                    tasks.create_vm_linux.delay(objTask.MainHost,hostname,objTask.MirrorName,objTask.SecretName)
                    self.db.query(ProjectsList).filter(ProjectsList.ProName == objTask.ProjectsName).update({'Vcpu':allocated_cpu_now,
                                                                                                             'Vmemory':allocated_memory_now,
                                                                                                             'Cconfig':allocated_kvm_count})
                    with open("/data/software/vnc/vnc_tokens","a") as f:
                        f.writelines("{0}: {1}:{2}\n".format(objTask.HostName,objTask.MainHost,port))
                elif objTask.MirrorName == "winxp":
                    createXml("/data/salt/kvm_manager/winxp_template.xml",hostname,uuid.uuid1(),memory,cpu,monip,mac,port)
                    tasks.create_vm_xp.delay(objTask.MainHost,hostname,objTask.MirrorName)
                    self.db.query(ProjectsList).filter(ProjectsList.ProName == objTask.ProjectsName).update({'Vcpu':allocated_cpu_now,
                                                                                                             'Vmemory':allocated_memory_now,
                                                                                                             'Cconfig':allocated_kvm_count})
                    with open("/data/software/vnc/vnc_tokens","a") as f:
                        f.writelines("{0}: {1}:{2}\n".format(objTask.HostName,objTask.MainHost,port))
                else:
                    createXml("/data/salt/kvm_manager/centos6_template.xml",hostname,uuid.uuid1(),memory,cpu,monip,mac,port)
                    tasks.create_vm_win.delay(objTask.MainHost,hostname,objTask.MirrorName)
                    self.db.query(ProjectsList).filter(ProjectsList.ProName == objTask.ProjectsName).update({'Vcpu':allocated_cpu_now,
                                                                                                             'Vmemory':allocated_memory_now,
                                                                                                             'Cconfig':allocated_kvm_count})
                    with open("/data/software/vnc/vnc_tokens","a") as f:
                        f.writelines("{0}: {1}:{2}\n".format(objTask.HostName,objTask.MainHost,port))
                self.db.add(objTask)
                self.db.commit()
                self.Result['rows'] = 1
                self.Result['info'] = u'添加成功'
                self.finish(self.Result)
            else:
                self.write(json.dumps({"status":200,"msg":u"配额不足请联系管理员增加配额"}))

    @web.asynchronous
    def put(self, ident):
        data = json.loads(self.request.body)
        objTask = self.db.query(KvmList).get(ident)
        if ident and objTask:
            objTask.CloudName = data['params'].get('CloudName', None)
            self.db.add(objTask)
            self.db.commit()
        self.Result['rows'] = 1
        self.Result['info'] = u'修改成功'
        self.finish(self.Result)

    @web.asynchronous
    def delete(self, ident):
        vm = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        allocation_cpu = int(vm.VirDisk.split('_')[0][0])
        Allocation_mem = int(vm.VirDisk.split('_')[1][0])
        tasks.vm_del.delay(vm.MainHost,vm.HostName)
        pro = self.db.query(ProjectsList).filter(ProjectsList.ProName == vm.ProjectsName).first()
        now_cpu = pro.Vcpu - allocation_cpu
        now_mem = pro.Vmemory - Allocation_mem
        now_Cconfig = pro.Cconfig - 1
        if now_cpu <= 0:
            now_cpu = 0
        elif now_mem <= 0:
            now_mem = 0
        self.db.query(ProjectsList).filter(ProjectsList.ProName == vm.ProjectsName).update({'Vcpu':now_cpu,
                                                                                            'Vmemory':now_mem,
                                                                                            'Cconfig':now_Cconfig})
        self.db.query(KvmList).filter(KvmList.HostName==vm.HostName).delete()
        data = open("/data/software/vnc/vnc_tokens", 'r').readlines()
        for i in data:
            if i.startswith("{0}".format(vm.HostName)):
                delindex = data.index(i)
                with open("/data/software/vnc/vnc_tokens", 'w') as handle:
                    handle.writelines(data[:delindex])
                    handle.writelines(data[delindex+1:])
        self.db.commit()
        self.Result['info'] = u'删除虚拟机成功'
        self.finish(self.Result)

#启动虚拟机
@urlmap(r'/vms/start\/?([0-9]*)')
class StartHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        vm = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        main_host = vm.MainHost
        vir_name = vm.HostName
        tasks.start_vm.delay(main_host,vir_name)
        self.Result['info'] = u'启动虚拟机成功'
        self.finish(self.Result)

#停止虚拟机
@urlmap(r'/vms/stop\/?([0-9]*)')
class StopHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        vm = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        tasks.stop_vm.delay(vm.MainHost,vm.HostName)
        self.Result['info'] = u'停止虚拟机成功'
        self.finish(self.Result)

#重启虚拟机
@urlmap(r'/vms/restart\/?([0-9]*)')
class RestartHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        vm = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        tasks.reboot_vm.delay(vm.MainHost,vm.HostName)
        self.Result['info'] = u'重启虚拟机成功'
        self.finish(self.Result)

#创建快照
@urlmap(r'/snapshot/create\/?([0-9]*)')
class CreateSnapshotHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        pro = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        tasks.c_snapshot.delay(pro.MainHost,pro.HostName)
        time.sleep(1)
        local = salt.client.LocalClient()
        result = local.cmd("{0}".format(pro.MainHost), "cmd.run",['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap ls vm_image/{0}.img'.format(pro.HostName)])
        try:
            result_list = result.values()[0].split(' ')
            snapshot_name = result_list[-3]
            count_snap = self.db.query(SnapshotList).filter(and_(SnapshotList.KvmId==ident,SnapshotList.ParentHostname==pro.HostName))
            objTask = SnapshotList()
            objTask.KvmId = ident
            objTask.ParentHostname = pro.HostName
            objTask.SnapshotName = snapshot_name
            objTask.CreateTime = curDatetime()
            objTask.AutoCreate = 'no'
            if count_snap:
                objTask.SnapshotNum = count_snap.count() + 1
            else:
                objTask.SnapshotNum = 1
            self.db.add(objTask)
            self.db.commit()
            self.Result['info'] = u'创建快照成功'
            self.finish(self.Result)
        except Exception,e:
            print e
            self.Result['info'] = u'创建快照失败'
            self.finish(self.Result)

#查看快照
@urlmap(r'/showsnap\/?([0-9]*)')
class ShowSnapshotHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        if ident:
            try:
                objServer = self.db.query(SnapshotList).filter(SnapshotList.KvmId==ident).all()
                objs = [obj.toDict() for obj in objServer]
                self.Result['rows'] = objs
                self.finish(self.Result)
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            page = int(self.get_argument('page', 1))
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            SnapshotObj = self.db.query(SnapshotList)
            serverTask = SnapshotObj.order_by(desc(SnapshotList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

#从快照还原虚拟机
@urlmap(r'/rollbacksnap\/?([0-9]*)\/?([0-9]*)')
class RollBackSnapHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident,kident):
        roll = self.db.query(KvmList).filter(KvmList.KvmId==ident).first()
        hostname = roll.HostName
        main_host = roll.MainHost
        try:
            snap = self.db.query(SnapshotList).filter(and_(SnapshotList.KvmId==ident,SnapshotList.SnapshotNum==kident,SnapshotList.ParentHostname==hostname)).first()
            tasks.re_snapshot.delay(main_host,hostname,snap.SnapshotName)
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"还原异常"}))
            self.redirect("/#/vms")
            return
        self.write(json.dumps({"status":200,"msg":u"还原成功"}))
        self.redirect("/#/vms")
        return

#获取镜像，二级联动
@urlmap(r'/mirror/')
class MirrorHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        mirror = self.db.query(MirrorList).filter(MirrorList.Level==1)
        mirror_list = []
        for i in mirror:
            d = {}
            d["id"] = i.MirrorId
            d["name"] = i.MirrorName
            d["code"] = i.MirrorId
            d["child"] = []
            child = self.db.query(MirrorList).filter(MirrorList.Level==2,MirrorList.Parent==i.MirrorId)
            for c in child:
                d["child"].append({"id":c.MirrorId,"name":c.MirrorName,"child":[]})
                mirror_list.append(d)
        rows = []
        [rows.append(i) for i in mirror_list if i not in rows]
        data = json.dumps(rows,indent=2)
        self.finish(data)

#获取项目列表
@urlmap(r'/projectlist/')
class ProjectlistHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        project = self.db.query(ProjectsList)
        projectlist = [i.ProName for i in project]
        data = json.dumps(projectlist,indent=2)
        self.finish(data)

#查看密钥
@urlmap(r'/safety\/?([0-9]*)')
class SafetyHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(SecretKeyList).get(ident)
                self.Result['rows'] = objServer.toDict()
                self.Result['total'] = 1
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            page = int(self.get_argument('page', 1))
            searchKey = self.get_argument('searchKey', None)
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            totalquery = self.db.query(SecretKeyList.SecretKeyId)
            secretKeylistObj = self.db.query(SecretKeyList)
            if searchKey:
                totalquery = totalquery.filter(or_(SecretKeyList.SecretkeyName.like('%%%s%%' % searchKey),SecretKeyList.CreatePerson.like('%%%s%%' % searchKey)))
                secretKeylistObj = secretKeylistObj.filter(or_(SecretKeyList.SecretkeyName.like('%%%s%%' % searchKey),SecretKeyList.CreatePerson.like('%%%s%%' % searchKey)))

            self.Result['total'] = totalquery.count()
            serverTask = secretKeylistObj.order_by(desc(SecretKeyList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

#创建密钥
@urlmap(r'/safety/secretkey\/?([0-9]*)')
class CreateSecretkeyHandler(RESTfulHandler):
    @web.asynchronous
    def post(self, ident=0):
        data = json.loads(self.request.body)
        objTask = SecretKeyList()
        objTask.SecretkeyName= data['params'].get('SecretkeyName', None)
        tasks.createkey.delay(objTask.SecretkeyName)
        objTask.CreatePerson= self.get_current_user()
        objTask.ProjectsName = data['params'].get('ProjectsName', None)
        objTask.CreateTime = curDatetime()
        self.db.add(objTask)
        self.db.commit()
        self.Result['info'] = u'创建密钥成功'
        self.finish(self.Result)
    #删除密钥
    @web.asynchronous
    def delete(self, ident):
        objServer = self.db.query(SecretKeyList).get(ident)
        key_name = objServer.SecretkeyName
        self.db.query(SecretKeyList).filter(SecretKeyList.SecretkeyName==key_name).delete()
        self.db.commit()
        tasks.delkey.delay(key_name)
        self.Result['info'] = u'删除虚拟机成功'
        self.finish(self.Result)

#检查密钥的唯一性
@urlmap(r'/secretkeycheck\/?(.*)')
class SecretCheckAppHandler(RESTfulHandler):
    @web.asynchronous
    def post(self,ident):
        data = json.loads(self.request.body)
        proname = data['keyname']
        try:
            appname = self.db.query(SecretKeyList).filter(SecretKeyList.SecretkeyName==proname).first().SecretkeyName
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"密钥正常"}))
            self.finish()
        else:
            return

#云硬盘管理
@urlmap(r'/clouddisk\/?([0-9]*)')
class CloudDiskHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(CloudDiskList).get(ident)
                self.Result['rows'] = objServer.toDict()
                self.Result['total'] = 1
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            page = int(self.get_argument('page', 1))
            searchKey = self.get_argument('searchKey', None)
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            totalquery = self.db.query(CloudDiskList.CloudDiskId)
            clouddisklistObj = self.db.query(CloudDiskList)
            if searchKey:
                totalquery = totalquery.filter(or_(CloudDiskList.ImageName.like('%%%s%%' % searchKey)))
                clouddisklistObj = clouddisklistObj.filter(or_(CloudDiskList.ImageName.like('%%%s%%' % searchKey)))

            self.Result['total'] = totalquery.count()
            serverTask = clouddisklistObj.order_by(desc(CloudDiskList.CloudDiskId)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)
    #创建云硬盘镜像
    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        objTask = CloudDiskList()
        objTask.ImageName= data['params'].get('ImageName', None)
        if objTask.ImageName and len(objTask.ImageName) <= 30:
            try:
                self.db.query(CloudDiskList).filter(CloudDiskList.ImageName==objTask.ImageName).first().ImageName
            except Exception,e:
                objTask.CloudSize= int(data['params'].get('CloudSize', None)) * 1024
                local = salt.client.LocalClient()
                hostname_list = ['ceph01-10-10-111-1.iprun.com','ceph02-10-10-111-2.iprun.com','ceph04-10-10-111-4.iprun.com']
                hostname = random.choice(hostname_list)
                local.cmd("{0}".format(hostname),"cmd.run",["rbd create {0} --size {1} --pool kvms".format(objTask.ImageName,objTask.CloudSize)])
                self.db.add(objTask)
                self.db.commit()
                self.Result['info'] = u'创建云硬盘成功'
            else:
                self.write(json.dumps({"status":200,"msg":u"镜像重复"}))
        self.finish(self.Result)

    #删除云硬盘镜像
    @web.asynchronous
    def delete(self,ident):
        try:
            objServer = self.db.query(CloudDiskList).filter(CloudDiskList.CloudDiskId==ident).first()
            image_name = objServer.ImageName
            tasks.del_image.delay(image_name)
            self.db.query(CloudDiskList).filter(CloudDiskList.ImageName==image_name).delete()
            self.db.commit()
            self.Result['info'] = u'删除云硬盘镜像成功'
        except Exception,e:
            self.Result['info'] = u'删除失败,失败原因{0}'.format(e)
        self.finish(self.Result)

#云硬盘挂载
@urlmap(r'/clouddisk/mount\/?([0-9]*)')
class CloudMountHandler(RESTfulHandler):
    @web.asynchronous
    def post(self, ident=0):
        objServer = self.db.query(CloudDiskList).get(ident)
        image_name = objServer.ImageName
        try:
            data = json.loads(self.request.body)
            objTask = CloudDiskList()
            objTask.ImageName = data['params'].get('ImageName', None)
            objTask.MountLocation = data['params'].get('MountLocation', None)
            pro = self.db.query(KvmList).filter(KvmList.CloudName==objTask.MountLocation).first()
            vm_hostname = pro.HostName
            main_host = pro.MainHost
            ip = pro.Ip
            projects_name = pro.ProjectsName
            dict_disk = {1:'vdb',2:'vdc',3:'vdd',4:'vde',5:'vdf',6:'vdg',7:'vdh',8:'vdi'}
            p = self.db.query(CloudDiskList).filter(CloudDiskList.MountLocation==objTask.MountLocation)
            if objServer.MountLocation == None and len(list(p)) == 0:
                dev_name = dict_disk[1]
            else:
                dev_name = dict_disk[len(list(p)) + 1]
            host = ('10.10.111.1','10.10.111.2','10.10.111.4')
            host_name = random.choice(host)
            tasks.mount_disk.delay(main_host,image_name,vm_hostname,ip,dev_name,host_name)
            self.db.query(CloudDiskList).filter(CloudDiskList.ImageName==objTask.ImageName).update({
                'MountLocation':objTask.MountLocation,
                'IpInfo':ip,
                'ProjectsName':projects_name,
                'DevName':dev_name
            })
            self.db.commit()
            self.Result['info'] = u'挂载成功'
        except Exception,e:
            self.Result['info'] = u'挂载失败,失败原因{0}'.format(e)
        self.finish(self.Result)

#云硬盘卸载
@urlmap(r'/clouddisk/umount\/?([0-9]*)')
class CloudUmountHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        try:
            objServer = self.db.query(CloudDiskList).get(ident)
            image_name = objServer.ImageName
            cloud_name = objServer.MountLocation
            dev_name = objServer.DevName
            vm_hostname = self.db.query(KvmList).filter(KvmList.CloudName==cloud_name).first().HostName
            main_host = self.db.query(KvmList).filter(KvmList.CloudName==cloud_name).first().MainHost
            ip = self.db.query(KvmList).filter(KvmList.CloudName==cloud_name).first().Ip
            tasks.umount_disk.delay(main_host,vm_hostname,image_name,ip,dev_name)
            self.db.query(CloudDiskList).filter(and_(
                CloudDiskList.MountLocation==cloud_name,CloudDiskList.ImageName==image_name)).update({
                'MountLocation':'','IpInfo':'','DevName':'','ProjectsName':''})
            self.db.commit()
            self.Result['info'] = u'卸载成功'
        except Exception,e:
            self.Result['info'] = u'卸载失败,失败原因{0}'.format(e)
        self.finish(self.Result)

#创建云硬盘快照
@urlmap(r'/clouddisk/createsnap\/?([0-9]*)')
class CloudSnapHandler(RESTfulHandler):
    @web.asynchronous
    def post(self,ident=0):
        objServer = self.db.query(CloudDiskList).get(ident)
        image_name = objServer.ImageName
        try:
            data = json.loads(self.request.body)
            objTask = CloudDiskSnapList()
            objTask.SnapId = ident
            objTask.SnapName = data['params'].get('SnapName', None)
            objTask.ImageName = image_name
            objTask.SnapSize = objServer.CloudSize
            objTask.CreateTime = curDatetime()
            tasks.snap_disk.delay(image_name,objTask.SnapName)
            self.db.add(objTask)
            self.db.commit()
            self.Result['info'] = u'创建云硬盘快照成功'
        except Exception,e:
            self.Result['info'] = u'创建云硬盘快照失败,失败原因{0}'.format(e)
        self.finish(self.Result)

#查看云硬盘快照
@urlmap(r'/clouddisk/showsnap\/?([0-9]*)')
class CloudShowHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident):
        if ident:
            try:
                objServer = self.db.query(CloudDiskSnapList).filter(CloudDiskSnapList.SnapId==ident).all()
                objs = [obj.toDict() for obj in objServer]
                self.Result['rows'] = objs
                self.finish(self.Result)
            except Exception,e:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found,{0}'.format(e)
        else:
            page = int(self.get_argument('page', 1))
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            totalquery = self.db.query(CloudDiskSnapList.SnapId)
            clouddisksnaplistObj = self.db.query(CloudDiskSnapList)
            self.Result['total'] = totalquery.count()
            serverTask = clouddisksnaplistObj.order_by(desc(CloudDiskSnapList.SnapId)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)

#删除云硬盘快照
@urlmap(r'/clouddisk/delcloudsnap\/?([0-9]*)\/?([0-9]*)')
class DeleteCloudHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident,ikent):
        try:
            objServer = self.db.query(CloudDiskSnapList).filter(and_(
                    CloudDiskSnapList.SnapId==ident,
                    CloudDiskSnapList.CloudDiskSnapId==ikent)).first()
            image_name = objServer.ImageName
            snap_name = objServer.SnapName
            tasks.del_snap.delay(image_name,snap_name)
            self.db.query(CloudDiskSnapList).filter(and_(
                    CloudDiskSnapList.SnapId==ident,
                    CloudDiskSnapList.CloudDiskSnapId==ikent)).delete()
            self.db.commit()
            self.Result['info'] = u'删除云硬盘快照成功'
        except Exception,e:
            self.Result['info'] = u'删除快照失败,失败原因{0}'.format(e)
        self.redirect("/#/clouddisk")
        return

#从云硬盘快照恢复
@urlmap(r'/clouddisk/recloudsnap\/?([0-9]*)\/?([0-9]*)')
class RecoverCloudHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident,ikent):
        try:
            objServer = self.db.query(CloudDiskSnapList).filter(and_(
                    CloudDiskSnapList.SnapId==ident,
                    CloudDiskSnapList.CloudDiskSnapId==ikent)).first()
            image_name = objServer.ImageName
            snap_name = objServer.SnapName
            tasks.rollback_snap.delay(image_name,snap_name)
            self.Result['info'] = u'从云硬盘快照恢复成功'
        except Exception,e:
            self.Result['info'] = u'恢复失败,失败原因{0}'.format(e)
        self.redirect("/#/clouddisk")
        return

#获取虚拟机用途列表供云硬盘使用
@urlmap(r'/cloudnamelist/')
class CloudNamelistHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        cloudname = self.db.query(KvmList)
        cloudnamelist = [i.CloudName for i in cloudname]
        data = json.dumps(cloudnamelist,indent=2)
        self.finish(data)

#获取cpu数量
@urlmap(r'/cpulist/')
class CpuListHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        data = json.dumps(range(2,200),indent=2)
        self.finish(data)

#获取内存大小
@urlmap(r'/memlist/')
class MemListHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        data = json.dumps(range(1,201),indent=2)
        self.finish(data)

#获取负责人列表
@urlmap(r'/directorlist/')
class DirectorlistHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(auth_user)
        directorlist = [i.UserName for i in director]
        data = json.dumps(directorlist,indent=2)
        self.finish(data)

#获取项目成员字典
@urlmap(r'/directordict/')
class DirectordictHandler(RESTfulHandler):
    @web.asynchronous
    def get(self):
        director = self.db.query(auth_user)
        directordict = map(lambda obj: obj.toDict(), director)
        data = json.dumps(directordict,indent=2)
        self.finish(data)

#检查云硬盘的唯一性
@urlmap(r'/cloudcheck\/?(.*)')
class CloudCheckHandler(RESTfulHandler):
    @web.asynchronous
    def post(self,ident):
        data = json.loads(self.request.body)
        proname = data['imagename']
        try:
            cloudname = self.db.query(CloudDiskList).filter(CloudDiskList.ImageName==proname).first().ImageName
        except Exception,e:
            self.write(json.dumps({"status":200,"msg":u"云硬盘正常"}))
            self.finish()
        else:
            return

#项目管理
@urlmap(r'/project\/?([0-9]*)')
class ProjectHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(ProjectsList).get(ident)
                self.Result['rows'] = objServer.toDict()
                self.Result['total'] = 1
            except:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found'
        else:
            page = int(self.get_argument('page', 1))
            searchKey = self.get_argument('searchKey', None)
            pagesize = int(self.get_argument('pagesize', self._PageSize))
            totalquery = self.db.query(ProjectsList.ProId)
            projectslistObj = self.db.query(ProjectsList)
            if searchKey:
                totalquery = totalquery.filter(or_(ProjectsList.ProName.like('%%%s%%' % searchKey)))
                projectslistObj = projectslistObj.filter(or_(ProjectsList.ProName.like('%%%s%%' % searchKey)))

            self.Result['total'] = totalquery.count()
            serverTask = projectslistObj.order_by(desc(ProjectsList.CreateTime)).limit(pagesize).offset((page - 1) * pagesize).all()
            self.Result['rows'] = map(lambda obj: obj.toDict(), serverTask)
        self.finish(self.Result)
    @web.asynchronous
    def post(self,ident=0):
        data = json.loads(self.request.body)
        objTask = ProjectsList()
        objTask.ProName = data['params'].get('ProName', None)
        objTask.ProDesc = data['params'].get('ProDesc', '')
        objTask.Ccpu = data['params'].get('Ccpu', None)
        objTask.Vcpu = 0
        objTask.Cmemory = data['params'].get('Cmemory', None)
        objTask.Vmemory = 0
        objTask.Cconfig = 0
        objTask.Status = 1
        objTask.Admin = data['params'].get('Admin', None)
        objTask.AdminId = self.db.query(auth_user).filter(auth_user.UserName == objTask.Admin).first().Id
        objTask.CreateId = 1
        objTask.CreateTime = curDatetime()
        objTask.UpdateTime = curDatetime()
        self.db.add(objTask)
        self.db.commit()
        self.Result['info'] = u'创建项目成功'
        self.finish(self.Result)
    @web.asynchronous
    def put(self,ident=0):
        data = json.loads(self.request.body)
        objTask = self.db.query(ProjectsList).get(ident)
        if ident and objTask:
            objTask.ProDesc = data['params'].get('ProDesc', '')
            objTask.Ccpu = data['params'].get('Ccpu', None)
            objTask.Cmemory = data['params'].get('Cmemory', None)
            objTask.Admin = data['params'].get('Admin', None)
            objTask.AdminId = self.db.query(auth_user).filter(auth_user.UserName == objTask.Admin).first().Id
            objTask.UpdateTime = curDatetime()
            self.db.add(objTask)
            self.db.commit()
            self.Result['rows'] = 1
            self.Result['info'] = u'修改项目成功'
        else:
            self.Result['rows'] = 0
            self.Result['info'] = u'修改项目失败'
        self.finish(self.Result)

#编辑项目成员
@urlmap(r'/project/member\/?([0-9]*)')
class MemberHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        if ident:
            try:
                objServer = self.db.query(pro_user_relation).filter(pro_user_relation.ProjectId==ident).all()
                objServer2 = self.db.query(ProjectsList).get(ident)
                d = {}
                proname = objServer2.toDict().get("ProName",None)
                d['ProName'] = proname
                d['ProjectId'] = ident
                objs = [obj.toDict() for obj in objServer]
                if objs:
                    countlist = [i.get("UserId",None) for i in objs]
                    c = {}
                    for i in countlist:
                        c[i] = True
                    objs[0]["UserId"] = c
                    objs[0].update(d)
                else:
                    objs.append(d)
                self.Result['rows'] = objs[0]
                self.finish(self.Result)
            except Exception,e:
                self.Result['status'] = 404
                self.Result['info'] = 'No Row Found,{0}'.format(e)
        else:
            totalquery = self.db.query(pro_user_relation.ProjectId)
            memberlistObj = self.db.query(pro_user_relation)
            self.Result['total'] = totalquery.count()
            self.Result['rows'] = map(lambda obj: obj.toDict(), memberlistObj)
        self.finish(self.Result)

    @web.asynchronous
    def post(self, ident=0):
        self.db.query(pro_user_relation).filter(pro_user_relation.ProjectId==ident).delete()
        self.db.commit()
        data = json.loads(self.request.body)
        userdict = data['params'].get('UserId',None)
        if userdict:
            userid = [k for k,v in userdict.iteritems() if v]
            for i in userid:
                pro = pro_user_relation(UserId=int(i),
                                  ProjectId=data['params'].get('ProjectId',None),
                                  IsActive=1,
                                  IsAdmin=0)
                self.db.add(pro)
                self.db.commit()
        else:
            pass
        self.Result['rows'] = 1
        self.Result['info'] = u'修改项目成员成功'
        self.finish(self.Result)
#启动vnc
@urlmap(r'/vnc_start\/?([0-9]*)')
class VncStartHandler(RESTfulHandler):
    @web.asynchronous
    def get(self, ident):
        objServer = self.db.query(KvmList).get(ident)
        hostname = objServer.HostName
        html = "http://10.10.112.10:8000/vnc_auto.html?path=websockify/?token={0}".format(hostname)
        self.redirect(html,permanent=True)
        return

#zcloud图形趋势
@urlmap(r'/zcloud\/?([0-9]*)')
class ZcloudHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident=1):
        objServer = self.db.query(ZcloudSizeList).all()
        objs = [obj.toDict() for obj in objServer]
        self.Result['showmin'] = len(objs) - 10
        self.Result['datetime'] = [i.get("CreateTime",None) for i in objs]
        self.Result['rows'] = [int(i.get("ZcloudSize",None)) for i in objs]
        self.finish(self.Result)

#ceph镜像图形趋势
@urlmap(r'/mirrordata\/?([0-9]*)')
class MirrorDataHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident=1):
        objServer = self.db.query(MirrorSizeList).all()
        objs = [obj.toDict() for obj in objServer]
        self.Result['datetime'] = list(set([i.get("CreateTime",None) for i in objs]))
        self.Result['kvms'] = [int(j.MirrorSize) for j in self.db.query(MirrorSizeList).filter(MirrorSizeList.MirrorName=="kvms").all()]
        self.Result['vm_image'] = [int(j.MirrorSize) for j in self.db.query(MirrorSizeList).filter(MirrorSizeList.MirrorName=="vm_image").all()]
        self.finish(self.Result)

#资源统计图形显示
@urlmap(r'/resource\/?([0-9]*)')
class ResourceHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident=1):
        objServer = self.db.query(ProjectsList).all()
        objs = [obj.toDict() for obj in objServer]
        self.Result['ProName'] = [i.get("ProName",None) for i in objs]
        self.Result['allocate_cpu'] = [i.get("Vcpu",None) for i in objs]
        self.Result['undistributed_cpu'] = [i.get("Ccpu",None) - i.get("Vcpu",None) for i in objs]
        self.Result['allocate_mem'] = [i.get("Vmemory",None) for i in objs]
        self.Result['undistributed_mem'] = [i.get("Cmemory",None) - i.get("Vmemory",None) for i in objs]
        self.finish(self.Result)

#获取当前登录用户
@urlmap(r'/getusername/')
class GetUserNameHandler(RESTfulHandler):
    @web.asynchronous
    def get(self,ident=0):
        self.Result['username'] = self.get_current_user()
        self.finish(self.Result)

#切换项目