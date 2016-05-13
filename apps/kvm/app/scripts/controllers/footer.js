define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:FooterCtrl
     * @description
     * # FooterCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.FooterCtrl', [])
        .controller('FooterCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.$on('$includeContentLoaded', function () {
                Layout.initFooter(); // init footer
            });
        });
});
