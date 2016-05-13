define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kvmApp.controller:ProjectServerCtrl
   * @description
   * # ProjectServerCtrl
   * Controller of the kvmApp
   */
  angular.module('kvmApp.controllers.ProjectServerCtrl', [])
    .controller('ProjectServerCtrl', function (ProjectService, $scope, $state, $uibModal,Syncservice) {
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
            ProjectService.fetch({page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
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
            var cpuList = JSON.parse(Syncservice.fetch('/api/v2/cpulist/'));
            var memList = JSON.parse(Syncservice.fetch('/api/v2/memlist/'));
            var directorList = JSON.parse(Syncservice.fetch('/api/v2/directorlist/'));
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
                        return {'title':'新建项目','cpuList':cpuList,'memList':memList,'directorList':directorList};
                    }
                }
            });
            modalInstance.save = function (item) {console.log(item);
                ProjectService.save(item).
                    success(function (data) {
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.edit = function (i) {
            var cpuList = JSON.parse(Syncservice.fetch('/api/v2/cpulist/'));
            var memList = JSON.parse(Syncservice.fetch('/api/v2/memlist/'));
            var directorList = JSON.parse(Syncservice.fetch('/api/v2/directorlist/'));
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
                        return {'title':'项目编辑','cpuList':cpuList,'memList':memList,'directorList':directorList};
                    }
                }
            });
           modalInstance.save = function (item) {
                ProjectService.save(item).
                    success(function (data) {
                    console.log(item);
                        modalInstance.close();
                        $scope.initPage();
                    });
            };
        };

        $scope.memberedit = function (ProjectId) {
            var directorDict = JSON.parse(Syncservice.fetch('/api/v2/directordict/'));
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'memberedit.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return ProjectService.showmember(ProjectId).then(function(succ){
                            return succ.data.rows;
                            });
                    },
                    title: function () {
                        return {'title':'项目成员编辑','directorDict':directorDict};
                    }
                }
            });
           modalInstance.savemember = function (item) {
                ProjectService.savemember(item).
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
            ProjectService
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
