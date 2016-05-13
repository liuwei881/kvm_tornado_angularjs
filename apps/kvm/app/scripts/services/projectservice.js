define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kvmApp.ServerService
   * @description
   * # PorjectService
   * Service in the kvmApp.
   */
  angular.module('kvmApp.services.ProjectService', [])
	.service('ProjectService', function ($http) {
	    // AngularJS will instantiate a singleton by calling "new" on this function
	    function fetch(params) {
            return $http.get('/api/v2/project', {params: params});
        }

        function save(params) {
            if (params.ProId != undefined) {
                return $http.put('/api/v2/project/' + params.ProId, {params: params})
            } else {
                return $http.post('/api/v2/project', {params: params})
            }
        }

        function Update(params) {
            return $http.post('/api/v2/update/' + params.ProjectId,{params: params});
        }

        function savemember(params) {
                return $http.post('/api/v2/project/member/' + params.ProjectId ,{params: params})
        }

        function showmember(ProjectId) {
            return $http.get('/api/v2/project/member/' + ProjectId);
        }

        function post(url, params) {
            return $http.post(url, {params: params})
        }

        return {
            fetch: fetch,
            save: save,
            Update: Update,
            savemember:savemember,
            showmember:showmember,
            post: post
        }
	});
});
