define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kvmApp.controller:ProjectServerCtrl
   * @description
   * # ProjectServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('kvmApp.controllers.ShowSnapServerCtrl', [])
    .controller('ShowSnapServerCtrl', function (ShowSnapService, $scope, $state, $uibModal,Syncservice) {
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
            ShowSnapService.fetch({page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }

        $scope.Create = function () {
            var allImage = JSON.parse(Syncservice.fetch('/api/v2/mirror/'));
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
                        return {'title':'新建','imageList':allImage,'projectlist':allproject};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                VmService.save(item).
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
                VmService.save(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Start = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'start.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'启动虚拟机'};
                    }
                }
            });
           modalInstance.Start = function (item) {
                VmService.Start(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Stop = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'stop.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'关闭虚拟机'};
                    }
                }
            });
           modalInstance.Stop = function (item) {
                VmService.Stop(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.Reboot = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'reboot.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'重启虚拟机'};
                    }
                }
            });
           modalInstance.Reboot = function (item) {
                VmService.Reboot(item).
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
                        return {'title':'删除虚拟机'};
                    }
                }
            });
           modalInstance.Delete = function (item) {
                VmService.Delete(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.CreateSnapshot = function (i) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'createsnapshot.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'创建快照'};
                    }
                }
            });
           modalInstance.CreateSnapshot = function (item) {
                VmService.CreateSnapshot(item).
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
            VmService
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
