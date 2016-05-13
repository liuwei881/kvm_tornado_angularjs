define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kvmApp.controller:ProjectServerCtrl
   * @description
   * # ProjectServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('kvmApp.controllers.CloudDiskServerCtrl', [])
    .controller('CloudDiskServerCtrl', function (CloudDiskService, $scope, $state, $uibModal,Syncservice) {
      this.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];

        $scope.total = 0;
        $scope.pageSize = 15;
        $scope.page = 1;
        $scope.searchKey = '';
        $scope.initPage = function(searchKey){
            CloudDiskService.fetch({page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                    $scope.defaults = data.defaults;
                    $scope.projects = data.projects;
                    $scope.username = data.username;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
            var allproject = JSON.parse(Syncservice.fetch('/api/v2/projectlist/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'add.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return {};
                    },
                    title: function () {
                        return {'title':'新建云硬盘','projectlist':allproject};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                CloudDiskService.save(item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.edit = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'edit.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'编辑'};
                    }
                }
            });
           modalInstance.save = function (item) {
                CloudDiskService.save(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.mount = function (i) {
            var allHost = JSON.parse(Syncservice.fetch('/api/v2/cloudnamelist/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'mount.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'挂载云硬盘','cloudnamelist':allHost};
                    }
                }
            });
           modalInstance.mount = function (item) {
                CloudDiskService.mount(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.umount = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'umount.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'卸载云硬盘'};
                    }
                }
            });
           modalInstance.umount = function (item) {
                CloudDiskService.umount(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.createdisksnap = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'createdisksnap.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'创建云硬盘快照'};
                    }
                }
            });
           modalInstance.createdisksnap = function (item) {
                CloudDiskService.createdisksnap(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.showdisksnap = function (SnapId) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'showdisksnap.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return CloudDiskService.showdisksnap(SnapId).then(function(succ){
                            return succ.data.rows;
                            });
                    },
                    title: function () {
                        return {'title':'查看云硬盘快照'};
                    }
                }
            });
           modalInstance.showdisksnap = function (item) {
                CloudDiskService.showdisksnap(SnapId).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Delete = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'delete.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'删除云硬盘'};
                    }
                }
            });
           modalInstance.Delete = function (item) {
                CloudDiskService.Delete(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Search = function (searchKey) {
            $scope.initPage(searchKey);
        };

        $scope.pageAction = function (page) {
            CloudDiskService
                .fetch({page: page})
                .success(function (data) {
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        $scope.sendReq = function(id, val){
         ProjectService.post('/api/v2/update/rc/' + id, {"rc": val}).then(function(result){
            result.data;
         });
        };

    }).filter('cut', function () {
        return function (value, wordwise, max, tail) {
            if (!value) return '';

            max = parseInt(max, 10);
            if (!max) return value;
            if (value.length <= max) return value;

            value = value.substr(0, max);
            if (wordwise) {
                var lastspace = value.lastIndexOf(' ');
                if (lastspace != -1) {
                    value = value.substr(0, lastspace);
                }
            }
            return value + (tail || '...');
        };
    });;
});
