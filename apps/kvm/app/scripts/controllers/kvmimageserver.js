define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.KvmImageServerCtrl', [])
        .controller('KvmImageServerCtrl', function ($scope, $http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $scope.initPage = function(number) {
                $http.get('/api/v2/mirrordata/' +number).success(function (data) {
                    if(data.status == 200){
                        Highcharts.chart('kvm',{
                            title: {
                                text: 'kvm镜像池空间大小趋势',
                                x: -20 //center
                                },

                            yAxis: {
                                title: {
                                    text: '单位(G)'
                                },
                                plotLines: [{
                                    value: 0,
                                    width: 1,
                                    color: '#808080'
                                }]
                            },
                            tooltip: {
                                valueSuffix: 'G'
                            },
                            legend: {
                                layout: 'vertical',
                                align: 'right',
                                verticalAlign: 'middle',
                                borderWidth: 0
                            },

                            xAxis: {
                                categories: data.datetime,
                            },

                            series: [{
                                    name: 'kvms',
                                    data: data.kvms
                                }, {
                                    name: 'vm_image',
                                    data: data.vm_image
                                }]
                      });
                            }
                        });
                        }
            $scope.initPage(1);
            });
            });
