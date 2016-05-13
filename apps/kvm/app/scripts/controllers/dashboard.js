define(['angular'], function (angular) {
    'use strict';

    /**
     * @ngdoc function
     * @name kvmApp.controller:DashboardCtrl
     * @description
     * # DashboardCtrl
     * Controller of the kvmApp
     */
    angular.module('kvmApp.controllers.DashboardCtrl', [])
        .controller('DashboardCtrl', function ($scope, $http) {
            $scope.awesomeThings = [
                'HTML5 Boilerplate',
                'AngularJS',
                'Karma'
            ];

           $scope.initPage = function(number) {
                $http.get('/api/v2/getinfo/' +number).
                    success(function (data) {
                        $scope.username = data.username;
                        $scope.defaults = data.defaults;
                        $scope.projects = data.projects;
                        $scope.results = data.results;
                        });

                //admin用户报表
                $http.get('/api/v2/resource/' +number).success(function (data){
                    if(data.status == 200){
                        Highcharts.chart('adminshow',{
                            chart: {
                                type: 'column'
                            },

                            title: {
                                text: '项目资源统计'
                            },
                            xAxis: {
                                categories: data.ProName
                            },
                            yAxis: {
                                allowDecimals: false,
                                min: 0,
                                title: {
                                    text: '数量'
                                    }
                                },
                            tooltip: {
                                formatter: function () {
                                    return '<b>' + this.x + '</b><br/>' +
                                        this.series.name + ': ' + this.y + '<br/>' +
                                        'Total: ' + this.point.stackTotal;
                                    }
                                },
                            plotOptions: {
                                column: {
                                    stacking: 'normal'
                                    }
                                },
                            series: [{
                                name: '已分配CPU数量(单位:核)',
                                    data: data.allocate_cpu,
                                    stack: 'CPU'
                                    }, {
                                    name: '未分配CPU数量(单位:核)',
                                    data: data.undistributed_cpu,
                                    stack: 'CPU'
                                    }, {
                                    name: '已分配内存数(单位:G)',
                                    data: data.allocate_mem,
                                    stack: '内存'
                                    }, {
                                    name: '未分配内存数(单位:G)',
                                    data: data.undistributed_mem,
                                    stack: '内存'
                                }]
                                });
                            }
                        });

                //普通用户项目报表
                $http.get('/api/v2/resource/' +number).success(function (data){
                    if(data.status == 200){
                        Highcharts.chart('partshow',{
                        chart: {
                            plotBackgroundColor: null,
                            plotBorderWidth: null,
                            plotShadow: false
                        },

                        title: {
                            text: $scope.results
                        },

                        tooltip: {
                            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:f}</b><br/>'
                        },
                        plotOptions: {
                            pie: {
                                allowPointSelect: true,
                                cursor: 'pointer',
                                dataLabels: {
                                    enabled: false
                                },
                                showInLegend: true
                            }
                        },
                        series: [{
                            type: 'pie',
                            name: 'cpu',
                            data: [
                            {
                                name: '未分配cpu(单位:核)',
                                y:data.undistributed_cpu

                            },
                            {
                                name: '已分配cpu(单位:核)',
                                y:data.allocate_cpu
                            }],
                            center: [500, 150],
                            size: 200,
                            showInLegend: true,
                            dataLabels: {
                            enabled: false
                                }
                            },

                            {
                            type: 'pie',
                            name: '内存',
                            data: [
                            {
                                name: '未分配内存(单位:G)',
                                y:data.undistributed_mem,
                                color:"#50B432"
                            },
                            {
                                name:'已分配内存(单位:G)',
                                y:data.allocate_mem,
                                color:"#028DC7"
                            }],
                            center: [1000, 150],
                            size: 200,
                            showInLegend: true,
                            dataLabels: {
                            enabled: false
                                }
                            }]
                               });
                            }
                        });
                        }
            $scope.initPage(1);
            });
            });

