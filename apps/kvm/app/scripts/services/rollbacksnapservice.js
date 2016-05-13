define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.ServerService
   * @description
   * # PorjectService
   * Service in the kubernetesApp.
   */
  angular.module('kvmApp.services.RollBackSnapService', [])
	.service('RollBackSnapService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function

        function RollBackSnap(KvmId,SnapshotNum) {
            return $http.get('/api/v2/rollbacksnap/' + KvmId + SnapshotNum);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            RollBackSnap:RollBackSnap,
            post: post
        }
	});
});
