define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:UsersCtrl
     * @description
     * # UsersCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.UsersCtrl', ['ui.bootstrap', 'ui.bootstrap.tpls'])
        .controller('UsersCtrl', function (Users, $scope, $state, $modal) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $scope.total = 0;
            $scope.pageSize = 15;
            $scope.page = 1;
            if ($state.current.needRequest) {
                Users.fetch({page: $scope.page, pageSize: $scope.pageSize}).
                    success(function (data) {
                        $scope.total = data.total;
                        $scope.lstUsers = data.rows;
                    });
            }

            $scope.Create = function () {
                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'edit.html',
                    controller: 'ModalInstanceCtrl',
                    size: 'lg',
                    resolve: {
                        item: function () {
                            return {};
                        },
                        title: function () {
                            return '新建';
                        }
                    }
                });
                modalInstance.save = function (item) {
                    Users.save(item).
                        success(function (data) {
                            modalInstance.close();
                            console.log(data);
                            $scope.lstPhysical.push(item);
                        });
                };
            };

            $scope.detail = function (i) {
                $modal.open({
                    animation: true,
                    templateUrl: 'detail.html',
                    controller: 'ModalInstanceCtrl',
                    size: 'lg',
                    resolve: {
                        item: function () {
                            return $scope.lstUsers[i];
                        },
                        title: function () {
                            return '查看';
                        }
                    }
                });
            };

            $scope.edit = function (i) {
                var modalInstance = $modal.open({
                    animation: true,
                    templateUrl: 'edit.html',
                    controller: 'ModalInstanceCtrl',
                    size: 'lg',
                    resolve: {
                        item: function () {
                            return $scope.lstUsers[i];
                        },
                        title: function () {
                            return '编辑';
                        }
                    }
                });
                modalInstance.save = function (item) {
                    Users.save(item).
                        success(function (data) {
                            modalInstance.close();
                            console.log(data);
                            $scope.lstPhysical[i] = item;
                        });
                };
            };

            $scope.Search = function () {

            };

            $scope.pageAction = function (page) {
                Users
                    .fetch({page: page})
                    .success(function (data) {
                        $scope.total = data.total;
                        $scope.lstUsers = data.rows;
                    });
            };

        });
});
