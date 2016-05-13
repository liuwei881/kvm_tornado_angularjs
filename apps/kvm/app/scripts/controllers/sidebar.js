define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kubernetesApp.controller:SidebarCtrl
     * @description
     * # SidebarCtrl
     * Controller of the kubernetesApp
     */
    angular.module('kvmApp.controllers.SidebarCtrl', [])
        .controller('SidebarCtrl', function ($scope, $http) {

            $scope.$on('$includeContentLoaded', function () {
                Layout.initSidebar();
            });

            $scope.pageSidebarClosed= false;

            $scope.initPage = function(number) {
            $http.get('/api/v2/getinfo/' +number).
                    success(function (username) {
                        $scope.username = username.username;
                        });
                    };
            $scope.initPage(1);
        });
});
