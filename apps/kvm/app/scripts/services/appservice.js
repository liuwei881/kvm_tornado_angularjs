define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kvmApp.ImageService
   * @description
   * # ImageService
   * Service in the kvmApp.
   */
  angular.module('kvmApp.services.AppService', [])
	.service('AppService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/app', {params: params});
        }

        function save(params) {
            if (params.AppId != undefined) {
                return $http.put('/api/v2/app/' + params.AppId, {params: params})
            } else {
                return $http.post('/api/v2/app', {params: params})
            }
        }

        function Updateapp(params) {
            return $http.post('/api/v2/updateapp/' + + params.AppId,{params: params});
        }

        function Delete(params) {
            return $http.delete('/api/v2/app/' + params.AppId);
        }

        function Start(params) {
            return $http.get('/api/v2/start/' + params.AppId);
        }

        function Stop(params) {
            return $http.get('/api/v2/stop/' + params.AppId);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            fetch: fetch,
            save: save,
            Updateapp:Updateapp,
            Delete: Delete,
            Start: Start,
            Stop: Stop,
            post:post
        }
	});
});
