define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc function
   * @name kvmApp.controller:ProjectServerCtrl
   * @description
   * # ProjectServerCtrl
   * Controller of the kubernetesApp
   */
  angular.module('kvmApp.controllers.RollBackSnapServerCtrl', [])
    .controller('RollBackSnapServerCtrl', function (RollBackSnapService, $scope, $state, $uibModal,Syncservice) {
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
            RollBackSnapService.fetch({page: $scope.page, pageSize: $scope.pageSize, searchKey:searchKey}).
                success(function (data) {
                    $scope.searchKey = searchKey;
                    $scope.total = data.total;
                    $scope.rows = data.rows;
                });
        };

        if ($state.current.needRequest) {
            $scope.initPage();
        }


        $scope.RollBackSnap = function (KvmId,SnapshotNum) {
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'rollback.html',
                controller: 'ModalInstanceCtrl',
                size: 'lg',
                resolve: {
                    item: function () {
                        return $scope.rows[i];
                    },
                    title: function () {
                        return {'title':'查看快照'};
                    }
                }
            });
           modalInstance.RollBackSnap = function (item) {
                RollBackSnapService.RollBackSnap(KvmId,SnapshotNum).
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
            RollBackSnapService
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
