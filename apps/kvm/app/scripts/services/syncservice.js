define(['angular'], function (angular) {
  'use strict';

  /**
   * @ngdoc service
   * @name kvmApp.TaskService
   * @description
   * # TaskService
   * Service in the kvmApp.
   */
  angular.module('kvmApp.services.Syncservice', [])
	.service('Syncservice', function () {
        function fetch(url) {
            var request;
            if (window.XMLHttpRequest) {
                request = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                request = new ActiveXObject("Microsoft.XMLHTTP");
            } else {
                throw new Error("Your browser don't support XMLHttpRequest");
            }
            request.open('GET', url, false);
            request.send(null);

            if (request.status === 200) {
                return request.responseText;
            }
        }
        return {
            fetch: fetch
        }
	});
});
