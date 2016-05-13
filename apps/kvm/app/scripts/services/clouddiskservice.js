define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.ServerService
   * @description
   * # PorjectService
   * Service in the kubernetesApp.
   */
  angular.module('kvmApp.services.CloudDiskService', [])
	.service('CloudDiskService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/clouddisk', {params: params});
        }

        function save(params) {
            if (params.CloudDiskId != undefined) {
                return $http.put('/api/v2/clouddisk/' + params.CloudDiskId, {params: params})
            } else {
                return $http.post('/api/v2/clouddisk', {params: params})
            }
        }

        function mount(params) {
            return $http.post('/api/v2/clouddisk/mount/' + params.CloudDiskId,{params: params});
        }

        function umount(params) {
            return $http.get('/api/v2/clouddisk/umount/' + params.CloudDiskId);
        }

        function createdisksnap(params) {
            return $http.post('/api/v2/clouddisk/createsnap/' + params.CloudDiskId,{params: params});
        }

        function showdisksnap(SnapId) {
            return $http.get('/api/v2/clouddisk/showsnap/' + SnapId);
        }

        function Delete(params) {
            return $http.delete('/api/v2/clouddisk/' + params.CloudDiskId);
        }
        return {
            fetch: fetch,
            save: save,
            mount:mount,
            umount:umount,
            createdisksnap:createdisksnap,
            showdisksnap:showdisksnap,
            Delete:Delete
        }
	});
});
