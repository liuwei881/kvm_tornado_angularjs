define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:HeaderCtrl
     * @description
     * # HeaderCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.HeaderCtrl', [])
        .controller('HeaderCtrl', function ($scope,$cookies,$state) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initHeader();
            });
            $scope.Login = function() {
                alert($cookies.user);
                $cookies.remove('user');
                $state.go('login');
            };

        });
});
