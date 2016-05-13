define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.ZcloudDataServerCtrl', [])
        .controller('ZcloudDataServerCtrl', function ($scope, $http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

            $scope.initPage = function(number) {
                $http.get('/api/v2/zcloud/' +number).success(function (data) {
                    if(data.status == 200){
                        Highcharts.chart('zcloud',{
                            options: {
                                chart: {
                                    zoomType: 'x'
                                },
                            },
                            title: {
                                text: 'zcloud数据库趋势图'
                            },
                            xAxis: {
                            categories: data.datetime,
                            min: [data.showmin],
                            },
                            yAxis: {
                                title: {
                                    text: '单位(k)'
                                },
                            },
                            legend: {
                                enabled: false
                            },
                            plotOptions: {
                                area: {
                                    fillColor: {
                                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                    ]
                                },
                                marker: {
                                    radius: 2
                                },
                                lineWidth: 1,
                                states: {
                                    hover: {
                                        lineWidth: 1
                                    }
                                },
                                threshold: null
                                    }
                            },

                            series: [{
                                type: 'area',
                                name: 'zcloud数据库',
                                data: data.rows
                         }]
                           });
                            }
                        });
                        }
            $scope.initPage(1);
            });
            });