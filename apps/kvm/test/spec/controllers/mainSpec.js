/*jshint unused: vars */
define(['angular', 'angular-mocks', 'app'], function(angular, mocks, app) {
  'use strict';

  describe('Controller: MainCtrl', function () {

    // load the controller's module
    beforeEach(module('kvmApp.controllers.MainCtrl'));

    var MainCtrl;
    var scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function ($controller, $rootScope) {
      scope = $rootScope.$new();
      MainCtrl = $controller('MainCtrl', {
        $scope: scope
        // place here mocked dependencies
      });
    }));

    it('should attach a list of awesomeThings to the scope', function () {
        expect(MainCtrl._AuthorCompany_.length).toBe(6);
    });
  });
});
