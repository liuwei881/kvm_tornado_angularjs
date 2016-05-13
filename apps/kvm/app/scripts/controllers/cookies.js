define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:CookiesCtrl
     * @description
     * # CookiesCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.CookiesCtrl', ['ngCookies'])
        .controller('CookiesCtrl', function ($scope, $http, $cookieStore) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $scope.initPage = function(number) {
                $http.get('/api/v2/getinfo/' +number).
                    success(function (data) {
                        $scope.username = data.username;
                        $scope.defaults = data.defaults;
                        $scope.projects = data.projects;
                        $scope.results = data.results;
                        });

            };
            $scope.initPage(1);


        });
});
