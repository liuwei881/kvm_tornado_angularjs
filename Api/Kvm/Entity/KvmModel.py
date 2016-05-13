#coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from lib.Route import BaseModel
from Kvm.Handler.functions import getStatusId

class ParentkvmList(BaseModel):
    """
    服务器信息列表
    """
    __tablename__ = 'bk_parent_list'

    ParentId = Column('fi_id', Integer, primary_key=True)
    ParentName = Column('fs_parentname', String(50))
    Ip = Column('fs_ip',String(15))
    Ip1 = Column('fs_ip1',String(15))
    Ip2 = Column('fs_ip2',String(15))
    ParentLocation = Column('fs_location',String(50))
    OsVersion = Column('fs_osversion',String(20))
    MemoryInfo = Column('fs_memory',String(20))
    DiskInfo = Column('fs_diskinfo',String(20))
    ModelName = Column('fs_modelname',String(20))
    CpuCore = Column('fs_cpucore',String(20))
    Sorts = Column('fs_sorts',String(20))
    SaltInfo = Column('fs_saltstatus',String(20))
    CreateTime = Column('ft_create_time', DateTime)
    """:param CreateTime: 创建时间"""

    def toDict(self):
        return {
            'ParentId': self.ParentId,
            'ParentName':self.ParentName,
            'Ip':self.Ip,
            'Ip1':self.Ip1,
            'Ip2':self.Ip2,
            'ParentLocation':self.ParentLocation,
            'OsVersion':self.OsVersion,
            'MemoryInfo':self.MemoryInfo,
            'DiskInfo':self.DiskInfo,
            'ModelName':self.ModelName,
            'CpuCore':self.CpuCore,
            'Sorts':self.Sorts,
            'SaltInfo':self.SaltInfo,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }

class KvmList(BaseModel):
    """
    镜像显示列表
    """
    __tablename__ = 'bk_kvm_list'

    KvmId = Column('fi_id', Integer, primary_key=True)
    CloudName = Column('fs_cloudname', String(40))
    HostName = Column('fs_hostname', String(20))
    Ip = Column('fs_ip', String(15))
    VirDisk = Column('fs_virdisk', String(20))
    MainHost = Column('fs_mainhost', String(50))
    Mac = Column('fs_mac', String(50))
    HostStatus = Column('fi_hoststatus', Integer)
    ProjectsName =Column('fs_projectsname', String(50))
    MirrorName = Column('fs_mirrorname', String(50))
    SecretName = Column('fs_secretname', String(50))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'KvmId': self.KvmId,
            'CloudName':self.CloudName,
            'HostName':self.HostName,
            'Ip':self.Ip,
            'VirDisk': self.VirDisk,
            'MainHost':self.MainHost,
            'Mac':self.Mac,
            'HostStatus':getStatusId(self.HostStatus),
            'ProjectsName':self.ProjectsName,
            'MirrorName':self.MirrorName,
            'SecretName': self.SecretName,
            'StatusNum':self.HostStatus,
            'CreateTime':self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }

class MirrorList(BaseModel):
    """
    三级联动镜像
    """
    __tablename__ = 'bk_mirrorname_list'
    MirrorId = Column('fi_id', Integer, primary_key=True)
    MirrorName = Column('fs_mirror_name', String(50))
    Level = Column('fi_level', Integer)
    Parent = Column('fi_parent', Integer)

    def toDict(self):
        return {
            'MirrorId': self.MirrorId,
            'MirrorName':self.MirrorName,
            'Level':self.Level,
            'Parent':self.Parent
        }

class SecretKeyList(BaseModel):
    """
    秘钥显示列表
    """
    __tablename__ = "bk_secretkey_list"
    SecretKeyId = Column('fi_id', Integer,primary_key=True)
    SecretkeyName = Column('fs_secretkey_name', String(20))
    CreatePerson = Column('fs_create_person', String(20))
    ProjectsName = Column('fs_projects_name', String(30))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'SecretKeyId': self.SecretKeyId,
            'SecretkeyName':self.SecretkeyName,
            'CreatePerson':self.CreatePerson,
            'ProjectsName':self.ProjectsName,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }


class ZcloudSizeList(BaseModel):
    """
    zcloud size
    """
    __tablename__ = "bk_zcloudsize_list"
    ZcloudSizeId = Column('fi_id', Integer,primary_key=True)
    ZcloudSize = Column('fs_size', String(20))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'ZcloudSizeId': self.ZcloudSizeId,
            'ZcloudSize':self.ZcloudSize,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d') if self.CreateTime else ''
        }


class MirrorSizeList(BaseModel):
    """
    镜像显示列表
    """
    __tablename__ = "bk_mirrorsize_list"
    MirrorId = Column('fi_id', Integer,primary_key=True)
    MirrorName = Column('fs_mirror_name', String(30))
    MirrorSize = Column('fs_mirror_size', String(20))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'MirrorId': self.MirrorId,
            'MirrorName':self.MirrorName,
            'MirrorSize':self.MirrorSize,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d') if self.CreateTime else ''
        }

class SnapshotList(BaseModel):
    """
    快照显示列表
    """
    __tablename__ = "bk_snapshot_list"
    SnapshotId = Column('fi_id', Integer,primary_key=True)
    KvmId = Column('fi_kvm_id',Integer)
    ParentHostname = Column('fs_parent_hostname', String(50))
    SnapshotName = Column('fs_snapshot_name', String(50))
    SnapshotNum = Column('fs_snapshot_num', Integer)
    AutoCreate = Column('fs_auto_create', String(50))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'SnapshotId': self.SnapshotId,
            'KvmId':self.KvmId,
            'ParentHostname':self.ParentHostname,
            'SnapshotName':self.SnapshotName,
            'SnapshotNum':self.SnapshotNum,
            'AutoCreate':self.AutoCreate,
            'CreateTime': self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }


class CloudDiskList(BaseModel):
    """
    云硬盘显示列表
    """
    __tablename__ = "bk_clouddisk_list"
    CloudDiskId = Column('fi_id', Integer,primary_key=True)
    ImageName = Column('fs_image_name',String(20))
    CloudSize = Column('fs_cloud_size', String(50))
    MountLocation = Column('fs_mount_location', String(50))
    IpInfo = Column('fs_ip', String(15))
    DevName = Column('fs_dev_name', String(10))
    ProjectsName = Column('ft_projects_name', String(50))

    def toDict(self):
        return {
            'CloudDiskId': self.CloudDiskId,
            'ImageName':self.ImageName,
            'CloudSize':self.CloudSize,
            'MountLocation':self.MountLocation,
            'IpInfo':self.IpInfo,
            'DevName':self.DevName,
            'ProjectsName': self.ProjectsName
        }


class CloudDiskSnapList(BaseModel):
    """
    云硬盘快照显示列表
    """
    __tablename__ = "bk_clouddisksnap_list"
    CloudDiskSnapId = Column('fi_id', Integer,primary_key=True)
    SnapId = Column('fs_snap_id',Integer)
    ImageName = Column('fs_image_name', String(20))
    SnapName = Column('fs_snap_name', String(50))
    SnapSize = Column('fs_snap_size', String(50))
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'CloudDiskSnapId': self.CloudDiskSnapId,
            'SnapId':self.SnapId,
            'ImageName':self.ImageName,
            'SnapName':self.SnapName,
            'SnapSize':self.SnapSize,
            'CreateTime':self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }


class RollBackList(BaseModel):
    """
    云硬盘快照回滚显示列表
    """
    __tablename__ = "bk_rollback_list"
    RollId = Column('fi_id', Integer,primary_key=True)
    SnapName = Column('fs_snap_name', String(50))
    CreateNum = Column('fi_create_num', Integer)
    CreateTime = Column('ft_create_time', DateTime)

    def toDict(self):
        return {
            'RollId': self.RollId,
            'SnapName':self.SnapName,
            'CreateNum':self.CreateNum,
            'CreateTime':self.self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else ''
        }


class ProjectsList(BaseModel):
    """
    项目显示列表
    """
    __tablename__ = "bk_pro_projects"
    ProId = Column('fi_id', Integer,primary_key=True)
    ProName = Column('fs_pro_name', String(100))
    ProDesc = Column('fs_pro_desc', String(254))
    Ccpu = Column('fi_c_cpu', Integer) #总cpu个数
    Vcpu = Column('fi_v_cpu', Integer) #已分配cpu个数
    Cmemory = Column('fi_c_memory', Integer) #总内存数
    Vmemory = Column('fi_v_memory', Integer) #已分配内存
    Cconfig = Column('fi_c_config', Integer) #虚拟机数量
    Status = Column('fi_status', Integer) #状态
    AdminId = Column('fi_admin_id', Integer) #负责人id
    Admin = Column('fs_admin',String(100)) #负责人
    CreateId = Column('fi_create_id', Integer) #创建人id
    CreateTime = Column('ft_create_time', DateTime)
    UpdateTime = Column('ft_update_time', DateTime)

    def toDict(self):
        return {
            'ProId': self.ProId,
            'ProName':self.ProName,
            'ProDesc':self.ProDesc,
            'Ccpu': self.Ccpu,
            'Vcpu':self.Vcpu,
            'Cmemory':self.Cmemory,
            'Vmemory': self.Vmemory,
            'Cconfig': self.Cconfig,
            'Status':self.Status,
            'AdminId':self.AdminId,
            'Admin':self.Admin,
            'CreateId':self.CreateId,
            'CreateTime':self.CreateTime.strftime('%Y-%m-%d %H:%M:%S') if self.CreateTime else '',
            'UpdateTime':self.UpdateTime.strftime('%Y-%m-%d %H:%M:%S') if self.UpdateTime else ''
        }

class auth_user(BaseModel):
    """用户表临时使用"""
    __tablename__ = "bk_auth_user"
    Id = Column('fi_id', Integer,primary_key=True)
    UserName = Column('fs_username', String(100))
    def toDict(self):
        return {
            'Id': self.Id,
            'UserName':self.UserName
        }

class pro_user_relation(BaseModel):
    """
    用户关系项目表
    """
    __tablename__ = "bk_pro_user_relation"
    Id = Column('fi_id', Integer,primary_key=True)
    UserId = Column('fs_user_id', Integer)
    ProjectId = Column('fi_project_id', Integer)
    IsActive = Column('fi_is_active', Integer)
    IsAdmin = Column('ft_is_admin', Integer)
    def toDict(self):
        return {
            'Id': self.Id,
            'UserId':self.UserId,
            'ProjectId':self.ProjectId,
            'IsActive':self.IsActive,
            'IsAdmin':self.IsAdmin
        }





