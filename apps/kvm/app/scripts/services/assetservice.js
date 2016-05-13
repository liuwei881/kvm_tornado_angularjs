define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kubernetesApp.ServerService
   * @description
   * # PorjectService
   * Service in the kubernetesApp.
   */
  angular.module('kvmApp.services.AssetService', [])
	.service('AssetService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/assets', {params: params});
        }

        function save(params) {
            if (params.ParentId != undefined) {
                return $http.put('/api/v2/assets/' + params.ParentId, {params: params})
            } else {
                return $http.post('/api/v2/assets', {params: params})
            }
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            fetch: fetch,
            save: save,
            post: post
        }
	});
});
