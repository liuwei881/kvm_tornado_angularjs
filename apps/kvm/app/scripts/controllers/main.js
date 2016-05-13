define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:MainCtrl
     * @description
     * # MainCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.MainCtrl', [])
        .controller('MainCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});
