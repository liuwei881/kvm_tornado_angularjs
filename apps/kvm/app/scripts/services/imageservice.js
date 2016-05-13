define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kvmApp.ImageService
   * @description
   * # ImageService
   * Service in the kvmApp.
   */
  angular.module('kvmApp.services.ImageService', [])
	.service('ImageService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/image', {params: params});
        }

        function save(params) {
            if (params.ImageId != undefined) {
                return $http.put('/api/v2/image/' + params.ImageId, {params: params})
            } else {
                return $http.post('/api/v2/image', {params: params})
            }
        }

        function saveApp(params) {
            if (params.AppName === undefined) {
                return $http.post('/api/v2/app/')
            } else {
                return $http.post('/api/v2/app', {params: params})
            }
        }

        function Delete(params) {
            return $http.delete('/api/v2/image/' + params.ImageId);
        }

        function Start(params) {
            return $http.start('/api/v2/image/' + params.ImageId);
        }

        function Stop(params) {
            return $http.stop('/api/v2/image/' + params.ImageId);
        }


        return {
            fetch: fetch,
            save: save,
            Delete: Delete,
            saveApp: saveApp,
            Start: Start,
            Stop: Stop
        }
	});
});
