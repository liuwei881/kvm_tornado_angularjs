define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.ServerService
   * @description
   * # PorjectService
   * Service in the kubernetesApp.
   */
  angular.module('kvmApp.services.SafetyService', [])
	.service('SafetyService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/safety/', {params: params});
        }

        function save(params) {
            if (params.SecretKeyId != undefined) {
                return $http.put('/api/v2/safety/' + params.SecretKeyId, {params: params})
            } else {
                return $http.post('/api/v2/safety/secretkey', {params: params})
            }
        }

        function Delete(params) {
            return $http.delete('/api/v2/safety/secretkey/' + params.SecretKeyId);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            fetch: fetch,
            save: save,
            Delete:Delete,
            post: post
        }
	});
});
