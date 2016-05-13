define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc service
     * @name kvmApp.httpInterceptor
     * @description
     * # httpInterceptor
     * Factory in the kvmApp.
     */
    angular.module('kvmApp.services.HttpInterceptor', [])
        .factory('httpInterceptor', function ($q, $rootScope, $cookies) {
            // Service logic
            // ...
            var meaningOfLife = 42;
            // Public API here
            return {
                someMethod: function () {
                    return meaningOfLife;
                },
                request: function (config) {
                    config.headers['X-Xsrftoken'] = $cookies.get('_xsrf');
                    return config;
                },
                response: function (response) {
                    return response || $q.when(response);
                },
                responseError: function (rejection) {
                    if (rejection.status === 401) {
                        $rootScope.$state.go('login');
                    }
                    return $q.reject(rejection);
                }
            };
        });
});
