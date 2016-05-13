# 项目简介

中细软运维项目平台

## 项目结构

*  Api

　　存放所有后端代码，按项目创建文件夹，例如Right文件夹对应到权限管理部分

　　每个模块中包含

    * tasks.py: 如果需要的话这个文件写celery任务代码
    * Handler: 该目录下存放对应的Url处理
    * Entity: 该目录下存放对应的数据表映射类

项目名称以首字母大写命名，相应文件夹也以这个方式命名

* apps

包含每应用的前端，使用 [generator-angular-require](https://github.com/hipeace86/generator-angular-require) 生成

每个应用都以全部小写命名

## 开发规范


### readme文档

每个项目文件夹下都要包含　`README.MD` 文件　用来记录相应功能描述及开发文档以方便后期整理

### mercurial分支

每项目必需有自己的分支，且分支都从 `common` 分支签出，确保不与其它分支（项目）有任何关系

`common` 分支有基础的登陆判断功能，会把Right功能引入；且其它应用也会用到权限部分

功能完成后需要把相应分支合并到 `master` 分支,并做好　`tag`

分支名称以项目名称的小写全称命名；例 Right 对应到 right　分支
