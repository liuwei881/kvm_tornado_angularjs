/*jshint unused: vars */
define(['angular', 'controllers/main', 'controllers/about', 'directives/paging', 'controllers/login', 'controllers/header', 'controllers/sidebar', 'controllers/pagehead', 'controllers/footer', 'controllers/dashboard','services/httpinterceptor', 'controllers/users', 'services/users', 'controllers/modalinstance', 'services/syncservice','controllers/assetserver','services/assetservice','controllers/vmserver','services/vmservice','controllers/safetyserver','services/safetyservice','controllers/clouddiskserver','services/clouddiskservice','controllers/projectserver','services/projectservice','controllers/showsnapserver','services/showsnapservice','directives/kvmkeyname','directives/cloudimagename','controllers/zclouddataserver','controllers/kvmimageserver']/*deps*/, function (angular, MainCtrl, AboutCtrl, PagingDirective, LoginCtrl, HeaderCtrl, SidebarCtrl, PageHeadCtrl, FooterCtrl, DashboardCtrl, PhysicalCtrl, HttpInterceptorFactory, PhysicalService, UsersCtrl,UsersServices, ModalinstanceCtrl, Syncservice,AssetServerCtrl,AssetService,VmServerCtrl,VmService,SafetyServerCtrl,SafetyService,CloudDiskServerCtrl,CloudDiskService,ProjectServerCtrl,ProjectService,ShowSnapServerCtrl,ShowSnapService,KvmkeynameDirective,CloudImagenameDirective,ZcloudDataServerCtrl,KvmImageServerCtrl)/*invoke*/ {
    'use strict';

    /**
     * @ngdoc overview
     * @name kvmApp
     * @description
     * # kvmApp
     *
     * Main module of the application.
     */
    return angular
        .module('kvmApp', ['kvmApp.controllers.MainCtrl',
            'kvmApp.controllers.AboutCtrl',
            'kvmApp.directives.Paging',
            'kvmApp.controllers.LoginCtrl',
            'kvmApp.controllers.HeaderCtrl',
            'kvmApp.controllers.SidebarCtrl',
            'kvmApp.controllers.PageHeadCtrl',
            'kvmApp.controllers.FooterCtrl',
            'kvmApp.controllers.DashboardCtrl',
            'kvmApp.controllers.ZcloudDataServerCtrl',
            'kvmApp.controllers.KvmImageServerCtrl',
            'kvmApp.services.HttpInterceptor',
            'kvmApp.controllers.UsersCtrl',
            'kvmApp.services.Users',
            'kvmApp.controllers.ModalInstanceCtrl',
            'kvmApp.services.Syncservice',
            'kvmApp.controllers.AssetServerCtrl',
            'kvmApp.services.AssetService',
            'kvmApp.controllers.VmServerCtrl',
            'kvmApp.services.VmService',
            'kvmApp.controllers.SafetyServerCtrl',
            'kvmApp.services.SafetyService',
            'kvmApp.controllers.CloudDiskServerCtrl',
            'kvmApp.services.CloudDiskService',
            'kvmApp.controllers.ProjectServerCtrl',
            'kvmApp.services.ProjectService',
            'kvmApp.controllers.ShowSnapServerCtrl',
            'kvmApp.services.ShowSnapService',
            'kvmApp.directives.Kvmkeyname',
            'kvmApp.directives.CloudImagename',

/*angJSDeps*/
            'ngCookies',
            'ngSanitize',
            'ngAnimate',
            'ui.router'
        ])
        .config(function ($stateProvider, $urlRouterProvider, $httpProvider) {
            $httpProvider.interceptors.push('httpInterceptor');
            $stateProvider
                .state('dashboard', {
                    url: '/',
                    templateUrl: 'views/main.html',
                    nav: 'DashHome'
                })
                .state('dashboard.home', {
                    url: 'dashboard',
                    templateUrl: 'views/dashboard.html',
                    controller: 'DashboardCtrl',
                    nav: 'DashBoard',
                    needRequest: true
                })
                .state('dashboard.assets', {
                    url: 'assets',
                    templateUrl: 'views/assets.html',
                    controller: 'AssetServerCtrl',
                    nav: '资产管理',
                    needRequest: true
                })
                .state('dashboard.vm', {
                    url: 'vms',
                    templateUrl: 'views/vm.html',
                    controller: 'VmServerCtrl',
                    nav: '虚拟机管理',
                    needRequest: true
                })
                .state('dashboard.safety', {
                    url: 'safety',
                    templateUrl: 'views/safety.html',
                    controller: 'SafetyServerCtrl',
                    nav: '访问&安全',
                    needRequest: true
                })
                .state('dashboard.secretkey', {
                    url: 'secretkey',
                    templateUrl: 'views/secretkey.html',
                    controller: '',
                    nav: '',
                    needRequest: true
                })
                .state('dashboard.clouddisk', {
                    url: 'clouddisk',
                    templateUrl: 'views/clouddisk.html',
                    controller: 'CloudDiskServerCtrl',
                    nav: '云硬盘管理',
                    needRequest: true
                })
                .state('dashboard.user', {
                    url: 'users',
                    templateUrl: 'views/user.html',
                    controller: 'UserServerCtrl',
                    nav: '用户管理',
                    needRequest: true
                })
                .state('dashboard.project', {
                    url: 'projects',
                    templateUrl: 'views/project.html',
                    controller: 'ProjectServerCtrl',
                    nav: '项目管理',
                    needRequest: true
                })
                .state('dashboard.zclouddata', {
                    url: 'zclouddata',
                    templateUrl: 'views/zclouddata.html',
                    controller: 'ZcloudDataServerCtrl',
                    nav: 'zcloud数据库趋势',
                    needRequest: true
                })
                .state('dashboard.kvmimage', {
                    url: 'kvmimage',
                    templateUrl: 'views/kvmimage.html',
                    controller: 'KvmImageServerCtrl',
                    nav: 'kvm镜像趋势',
                    needRequest: true
                })

                .state('login',{
                    url: '/login',
                    templateUrl: 'views/login.html',
                    controller: 'LoginCtrl'
                })
                .state('logout',{
                    url: '/logout',
                    controller: function($cookies,$state){
                        $cookies.remove('user');
                        $state.go('login');
                    }
                })
            $urlRouterProvider.otherwise('/');
        })
        .run(function ($rootScope, $state, $stateParams, $cookies) {
            $rootScope.$state = $state;
            $rootScope.$stateParams = $stateParams;
            $rootScope.$on('$stateChangeStart', function (event, toState, fromState) {
                if (toState.url === '/login') {
                    $('body').addClass('login');
                } else {
                    $('body').removeClass('login');
                    if ($cookies.get('user') === undefined) {
                        event.preventDefault();
                        $state.go('login');
                    }
                }
            });
        });
    ;
});
