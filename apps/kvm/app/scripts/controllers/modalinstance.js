define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:ModalInstanceCtrlCtrl
     * @description
     * # ModalInstanceCtrlCtrl
     * Controller of the kubernetesApp
     */
    angular.module('kvmApp.controllers.ModalInstanceCtrl', [])
        .controller('ModalInstanceCtrl', function ($scope, $uibModalInstance, item, title) {
            this.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];
            $scope.item = item;
            $scope.title = title;
            $scope.Save = function () {
                $uibModalInstance.save($scope.item);
            };

            $scope.Update = function () {
                $uibModalInstance.Update($scope.item);
            };

            $scope.Updateapp = function () {
                $uibModalInstance.Updateapp($scope.item);
            };

            $scope.Delete = function () {
                $uibModalInstance.Delete($scope.item);
            };

            $scope.Start = function () {
                $uibModalInstance.Start($scope.item);
            };

            $scope.Stop = function () {
                $uibModalInstance.Stop($scope.item);
            };

            $scope.Restart = function () {
                $uibModalInstance.Restart($scope.item);
            };

            $scope.CreateSnapshot = function () {
                $uibModalInstance.CreateSnapshot($scope.item);
            };

            $scope.mount = function () {
                $uibModalInstance.mount($scope.item);
            };

            $scope.umount = function () {
                $uibModalInstance.umount($scope.item);
            };

            $scope.createdisksnap = function () {
                $uibModalInstance.createdisksnap($scope.item);
            };

            $scope.savemember = function () {
                $uibModalInstance.savemember($scope.item);
            };

            $scope.showmember = function () {
                $uibModalInstance.showmember($scope.item);
            };

            $scope.cancel = function () {
                $uibModalInstance.dismiss('cancel');
            };
        });
});
