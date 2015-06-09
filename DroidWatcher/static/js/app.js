/**
 * Created by suemi on 15/3/30.
 */
angular.module('DroidWatcher',['ui.router','Controllers'])
    .config(function($stateProvider,$urlRouterProvider,$interpolateProvider){
        $urlRouterProvider.when('','/');
        $urlRouterProvider.otherwise('/404');
        $stateProvider
            .state('dashboard',{
                url:'/',
                templateUrl:'/static/html/dashboard.html'
            })
            .state('apk_search',{
                url:'/apk/search',
                templateUrl:'/static/html/apk/search.html',
                controller:'apkSearchCtrl'
            })
            .state('apk_upload',{
                url:'/apk/upload',
                templateUrl:'/static/html/apk/upload.html',
                controller:'apkUploadCtrl'
            })
            .state('report_basic',{
                    url:'/report/basic',
                    templateUrl:'/static/html/report/basic.html',
                    controller:'basicCtrl'
                })
            .state('report_analysis',{
                url:'/report/analysis',
                templateUrl:'/static/html/report/analysis.html',
                controller:'additionCtrl'
            })
            .state('report_edit',{
                url:'/report/edit',
                templateUrl:'/static/html/report/edit.html',
                controller:'reportEditCtrl'
            })
            .state('apk_record',{
                url:'/apk/record',
                templateUrl:'/static/html/apk/record.html',
                controller:'recordCtrl'
            })
            .state('exception',{
                url:'/404',
                templateUrl:'/static/html/404.html'
            })
            .state('setting',{
            	url:'/system/setting',
            	templateUrl:'/static/html/system/setting.html',
            	controller:'setCtrl'
            });
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');

    })
    .controller('rootCtrl',function($scope,$rootScope){
        $rootScope.msgList=[];
//        var skt=new io.Socket();
//        skt.connect();
//	        var skt=io.connect();
//	        skt.on('connect',function(){
//	        	console.log('haha');
//	        });
//	        skt.on('connect',function(){
//	            console.log('ss');
//	        });
//	        skt.emit('apk','aa');
    });

