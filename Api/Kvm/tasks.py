#coding=utf-8

from celery import Celery,task
import os,salt.client
import subprocess
celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    )

@celery.task(name='tasks.create_vm_linux')
def create_vm_linux(mhostname,zhostname,mirror_name,secret_name):
    '''创建linux虚拟机'''
    local = salt.client.LocalClient()
    def find_pub(filepath):
        '''查找公钥'''
        file_list = []
        [file_list.append(i) for i in os.listdir(filepath) if i.endswith('.pub')]
        return file_list
    file_list = find_pub('/data/salt/kvm_manager')
    for i in file_list:
        local.cmd('{0}'.format(mhostname),"cp.get_file",['salt://kvm_manager/%s' % i,'/data/software/%s' % i])

    result = local.cmd('{0}'.format(mhostname),[
            'cp.get_file',
            'cp.get_file',
            'cp.get_file',
            'cmd.run',
        ],
        [
            ['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
            ['salt://kvm_manager/{0}.xml'.format(zhostname),'/etc/libvirt/qemu/{0}.xml'.format(zhostname)],
            ['salt://kvm_manager/createtemplate_test.sh', '/data/software/createtemplate_test.sh'],
            ['sh /data/software/createtemplate_test.sh {0} {1} {2}'.format(zhostname,mirror_name,secret_name)],
        ])
    return result

@celery.task(name='tasks.create_vm_xp')
def create_vm_xp(mhostname,zhostname,mirror_name):
    '''创建winxp虚拟机'''
    local = salt.client.LocalClient()
    result = local.cmd('{0}'.format(mhostname),[
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cmd.run',
		],
		[
			['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
			['salt://kvm_manager/{0}.xml'.format(zhostname),'/etc/libvirt/qemu/{0}.xml'.format(zhostname)],
			['salt://kvm_manager/createtemplate_xp_test.sh', '/data/software/createtemplate_xp_test.sh'],
			['sh /data/software/createtemplate_xp_test.sh {0} {1}'.format(zhostname,mirror_name)],
		])
    return result

@celery.task(name='tasks.create_vm_win')
def create_vm_win(mhostname,zhostname,mirror_name):
    '''创建win虚拟机'''
    local = salt.client.LocalClient()
    result = local.cmd('{0}'.format(mhostname),[
			'cp.get_file',
			'cp.get_file',
			'cp.get_file',
			'cmd.run',
		],
		[
			['salt://kvm_manager/secret2.xml','/data/software/secret2.xml'],
			['salt://kvm_manager/{0}.xml'.format(zhostname),'/etc/libvirt/qemu/{0}.xml'.format(zhostname)],
			['salt://kvm_manager/createtemplate_win_test.sh', '/data/software/createtemplate_win_test.sh'],
			['sh /data/software/createtemplate_win_test.sh {0} {1}'.format(zhostname,mirror_name)],
		])
    return result

@task(name='tasks.start_vm')
def start_vm(main_host, vir_name):
    '''启动虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),"virt.start",[vir_name])
    return a

@task(name='tasks.stop_vm')
def stop_vm(main_host, vir_name):
    '''关闭虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),"virt.stop",[vir_name])
    return a

@task(name='tasks.reboot_vm')
def reboot_vm(main_host, vir_name):
    '''重启虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),
                  [
                      "virt.stop",
                      "virt.start",
                  ],
                  [
                    [vir_name],
                    [vir_name]
                  ])
    return a

@task(name='tasks.vm_del')
def vm_del(main_host, hostname):
    '''删除虚拟机'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),
                [
                    "virt.stop",
                    "virt.undefine",
                    "cmd.run",
                ],
                [
                    [hostname],
                    [hostname],
                    ['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 rm vm_image/%s.img' % hostname]
                ])
    return a

@task(name='tasks.c_snapshot')
def c_snapshot(main_host,hostname):
    '''创建快照'''
    local = salt.client.LocalClient()
    import time
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    timeArray = time.strptime(now_time,"%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    a = local.cmd("{0}".format(main_host),"cmd.run",['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap create vm_image/{0}.img@{1}'.format(hostname,timeStamp)])
    return a

@task(name='tasks.re_snapshot')
def re_snapshot(main_host,hostname,snapshot_name):
    '''从快照还原'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),[
        'cmd.run',
        'cmd.run',
        'cmd.run',
        ],
        [
            ['virsh destroy {0}'.format(hostname)],
            ['rbd --keyring /etc/ceph/ceph.client.libvirt2.keyring --id libvirt2 snap rollback vm_image/{0}.img@{1}'.format(hostname,snapshot_name)],
            ['virsh start {0}'.format(hostname)],
        ])
    return a

@task(name='tasks.createkey')
def createkey(keyname):
    '''创建密钥对'''
    a = subprocess.call("ssh-keygen -f /root/.ssh/{0} -P '' && mv /root/.ssh/{0} /data/zPlatform/apps/kvm/app/keypairs/download/ && chmod 644 /data/zPlatform/apps/kvm/app/keypairs/download/{0} && mv /root/.ssh/{0}.pub /data/salt/kvm_manager".format(keyname),shell=True)
    return a

@task(name='tasks.delkey')
def delkey(keyname):
    '''删除密钥对'''
    a = subprocess.call('rm /data/salt/kvm_manager/{0} -rf && rm /data/zPlatform/apps/kvm/app/zxrCloud/keypairs/download/{0} -rf'.format(keyname),shell=True)
    return a

@task(name='tasks.mount_disk')
def mount_disk(main_host,image_name,vm_hostname,ip,dev_name,host_name):
    '''挂载云硬盘'''
    local = salt.client.LocalClient()
    a = local.cmd("%s" % main_host,
                  [
                      "cp.get_file",
                      "cp.get_file",
                      "cmd.run",
                  ],
                  [
                      ['salt://kvm_manager/mount_image.sh','/data/software/mount_image.sh'],
                      ['salt://kvm_manager/secret.xml','/data/software/secret.xml'],
                      ['sh /data/software/mount_image.sh %s %s %s %s %s' % (image_name,vm_hostname,ip,dev_name,host_name)]

                  ])
    return a

@task(name='tasks.umount_disk')
def umount_disk(main_host,vm_hostname,image_name,ip,dev_name):
    '''卸载云硬盘'''
    local = salt.client.LocalClient()
    a = local.cmd("{0}".format(main_host),"cmd.run", ['virsh detach-device --persistent {0} /etc/libvirt/qemu/disk_{1}-{2}-{3}.xml'.format(vm_hostname,image_name,ip,dev_name)])
    return a

@task(name='tasks.snap_disk')
def snap_disk(image_name,snap_name):
    '''创建ceph镜像快照'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap create kvms/{0}@{1}'.format(image_name,snap_name)]) #kvms01 为ceph mon 6789的端口
    return a

@task(name='tasks.del_snap')
def del_snap(image_name,snap_name):
    '''删除ceph镜像快照'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap rm kvms/{0}@{1}'.format(image_name,snap_name)])  #kvms01 为ceph mon 6789的端口
    return a

@task(name='tasks.rollback_snap')
def rollback_snap(image_name,snap_name):
    '''ceph快照回滚'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd snap rollback kvms/{0}@{1}'.format(image_name,snap_name)])
    return a

@task(name='tasks.del_image')
def del_image(image_name):
    '''删除ceph镜像'''
    local = salt.client.LocalClient()
    a = local.cmd("ceph02-10-10-111-2.iprun.com","cmd.run",['rbd rm -p kvms {0}'.format(image_name)])
    return a