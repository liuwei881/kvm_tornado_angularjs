define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.ServerService
   * @description
   * # PorjectService
   * Service in the kubernetesApp.
   */
  angular.module('kvmApp.services.VmService', [])
	.service('VmService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/vms', {params: params});
        }

        function save(params) {
            if (params.KvmId != undefined) {
                return $http.put('/api/v2/vms/' + params.KvmId, {params: params})
            } else {
                return $http.post('/api/v2/vms', {params: params})
            }
        }

        function Start(params) {
            return $http.get('/api/v2/vms/start/' + params.KvmId);
        }

        function Stop(params) {
            return $http.get('/api/v2/vms/stop/' + params.KvmId);
        }

        function Restart(params) {
            return $http.get('/api/v2/vms/restart/' + params.KvmId);
        }

        function Delete(params) {
            return $http.delete('/api/v2/vms/' + params.KvmId);
        }

        function CreateSnapshot(params) {
            return $http.get('/api/v2/snapshot/create/' + params.KvmId);
        }

        function ShowSnap(KvmId) {
            return $http.get('/api/v2/showsnap/' + KvmId);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            fetch: fetch,
            save: save,
            Start:Start,
            Stop:Stop,
            Restart:Restart,
            Delete:Delete,
            CreateSnapshot:CreateSnapshot,
            ShowSnap:ShowSnap,
            post: post
        }
	});
});
