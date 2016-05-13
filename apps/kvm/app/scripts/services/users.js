define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc service
     * @name kvmApp.Users
     * @description
     * # Users
     * Service in the kvmApp.
     */
    angular.module('kvmApp.services.Users', [])
        .service('Users', function ($http) {
            // AngularJS will instantiate a singleton by calling "new" on this function
            function fetch(params) {
                return $http.get('/api/v2/users', {params: params});
            }

            function save(params) {
                if (params.UsersId != undefined) {
                    return $http.put('/api/v2/users' + params.UserId, {params: params})
                } else {
                    return $http.post('/api/v2/users', {params: params})
                }
            }

            function Delete(id) {
                return $http.delete('/api/v2/users/' + id);
            }

            return {
                fetch: fetch,
                save: save,
                Delete: Delete
            }
        });
});
