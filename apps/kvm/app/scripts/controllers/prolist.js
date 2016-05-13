define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:PageHeadCtrl
     * @description
     * # PageHeadCtrl
     * Controller of the kubernetesApp
     */
    angular.module('kvmApp.controllers.ProListCtrl', [])
        .controller('ProListCtrl', function ($scope) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
        });
});
