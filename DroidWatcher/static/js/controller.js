/**
 * Created by suemi on 15/3/30.
 */
angular.module('Controllers',['angularFileUpload'])
    .service('Tool',function(){
        this.clone=function(obj){
            var o,i,j,k;
	        if(typeof(obj)!="object" || obj===null)return obj;
	        if(obj instanceof(Array))
	        {
	        	o=[];
	        	i=0;j=obj.length;
	        	for(;i<j;i++)
	        	{
	        		if(typeof(obj[i])=="object" && obj[i]!=null)
	        		{
	        			o[i]=arguments.callee(obj[i]);
	        		}
	        		else
	        		{
	        			o[i]=obj[i];
	        		}
	        	}
	        }
	        else
	        {
	        	o={};
	        	for(i in obj)
	        	{
	        		if(typeof(obj[i])=="object" && obj[i]!=null)
	        		{
	        			o[i]=arguments.callee(obj[i]);
	        		}
	        		else
	        		{
	        			o[i]=obj[i];
	        		}
	        	}
	        }

	        return o;
        };
        
        
    })
    .controller('apkSearchCtrl',function($scope,$rootScope,$http,$state){
        $scope.apkList=[];$scope.result=[];
        $scope.display=false;$scope.context="";
        $scope.start=0;
        $scope.search=function(){
            $http.post('/apk/search',{"keyword":$scope.keyword})
                .success(function(res){
                    console.log(res);
                    if(res.success){
                        $scope.result=res.data;
                        $scope.start=0;
                        $scope.apkList=$scope.result.slice(0,Math.min($scope.result.length,10))
                        $scope.display=false;
                    }
                    else{
                        $scope.context=res.msg;
                        $scope.display=true;
                    }
                }).error(function(){
                    $scope.context="出现未知错误，请稍后再试";
                    $scope.display=true;
                });
        };
        
        $scope.nextPage=function(){
            $scope.start+=10;
            if($scope.start>$scope.result.length) return;
            var end=Math.min($scope.start+10,$scope.result.length);
            $scope.apkList=$scope.result.slice($scope.start,end);
        };
        $scope.previousPage=function(){
            $scope.start-=10;
            if($scope.start<0) return;
            var end=Math.min($scope.start+10,$scope.result.length);
            $scope.apkList=$scope.result.slice($scope.start,end);
        };
        $scope.select=function(item){
            $http.post('/apk/select',item)
                .success(function(res){
                   if(res.success){
                       $rootScope.basic=res.data;
                       $state.go('report_basic');
                   }
                   else{
                       $scope.context=res.msg;
                       $scope.display=true;
                   }
                })
                .error(function(){
                       $scope.context="出现未知错误，请稍后再试";
                       $scope.display=true;
                });
        };

    })
    .controller('basicCtrl',function($scope,$rootScope,$http){
        //$('.information').css('display','none');
        $scope.display=true;
        var adaptor=function(src){
            //通过已有信息生成一些便于展示的附加属性
        	dst={};
        	for(var i in src){
        		if(typeof(src[i])=='string'){
        			dst[i]=src[i];
        		}
        	}
        	dst.rootTrusted=src.rootTrusted?'是':'否';
        	dst.selfSigned=src.selfSigned?'是':'否';
        	dst.verifySigned=src.verifySigned?'是':'否';
        	switch(src.type){
        	case 0: 
        		dst.type='训练样本';
        		break;
        	case 1:
        		dst.type='测试样本';
        		break;
        	case 2:
        		dst.type='记录样本';
        		break;
        	default:
        		dst.type='未知样本';
        	}
        	switch(src.level){
        	case 0: 
        		dst.level='正常';
        		break;
        	case 1:
        		dst.level='恶意';
        		break;
        	case 2:
        		dst.level='中危';
        		break;
        	case 3:
        		dst.level='高危';
        		break;
        	default:
        		dst.level='未知';
        	}
        	dst.hrefList=src.hrefList;
        	return dst;
        };
        if(!$rootScope.basic){
            $http.get('/report/basic').success(function(res){
                console.log(res);
                if(res.success){
                    $rootScope.basic=res.data;
                    $scope.apk=adaptor($rootScope.basic);
                }
                else{
                    $scope.context=res.msg;
                    $scope.display=false;
                }
            }).error(function(){
                $scope.context='请先转到搜索或提交页面选择应用';
                $scope.display=false;
            });
        }
        else{
            $scope.apk=adaptor($rootScope.basic);
        }
    })
    .controller('additionCtrl',function($scope,$rootScope,$http){
    	$scope.display=false;
        $scope.editor=new JSONEditor(document.getElementById('componentEditor'),{
        	mode:'view'
        });
    	var adaptor=function(src){
    		dst={};
    		org=$rootScope.basic;
    		if(org){
    			dst['应用名称']=org.name;
    			dst['风险级别']=function(level){
    				zz='';
    				switch(level){
    				case 0:
    					zz='正常';
    					break;
    				case 1:
    					zz='恶意';
    					break;
    				case 2:
    					zz='中危';
    					break;
    				case 3:
    					zz='高危';
    					break;
    				default:
    					zz='未知';
    				}
    				return zz;
    			}(org.level);
    			console.log(dst['风险级别']);
    		}

    		dst['活动总数']=src.activityList.length;
    		dst['提供者数量']=src.providerList.length;
    		dst['服务总数']=src.serviceList.length;
    		dst['广播接收者总数']=src.receiverList.length;
    		dst['申请权限总数']=src.permissionList.length;
    		dst['活动列表']=src.activityList;
    		dst['提供者列表']=src.providerList;
    		dst['服务列表']=src.serviceList;
    		dst['广播接收者列表']=src.receiverList;
    		dst['敏感API列表']=src.apiList;
    		dst['申请权限列表']=src.permissionList.map(function(x){
    			return {
    				'权限名称':x.name,
    				'权限级别':x.level,
    				'简要说明':x.desc,
    				'详细描述':x.detail
    			}
    		});
    		
    		return dst;
    	};
    	
        $http.get('/report/analysis').success(function(res){
        	console.log(res);
               if(res.success){
                   $scope.info=adaptor(res.data);
                   $scope.editor.set($scope.info);
                   $scope.display=false;
               }
               else{
                   $scope.context=res.msg;
                   $scope.display=true;
               }
           }).error(function(){
               $scope.context='请先转到搜索或提交页面选择应用';
               $scope.display=true;
           });   
    })
    .controller('apkUploadCtrl',function($scope,$rootScope,$http,$upload){
        $scope.xhr=null; $scope.apkType=3;$scope.level=4;
        
        Window.query=function(){
        	console.log('query');
        	$http.post('/apk/query',{
        		"md5":$scope.md5
        	}).success(function(res){
        		console.log(res);
        		$('#terminal').append(res);
        		
        	});
        	$scope.timer=setTimeout('Window.query()',5000);
        };
        $scope.start=function(){
            if(!$scope.files) return;
            if($scope.files.length<=0) return;
            var file=$scope.files[0];
            $scope.xhr=$upload.upload({
                url:'/apk/upload',
                file:file
                //fields:{'apkType':$scope.apkType}
            }).progress(function(evt){
                var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                $('#terminal').append('<p>文件已上传'+progressPercentage+'%</p>');
            }).success(function(res){
                if(res.success){
                	tmp={
                		"md5":res.data.md5,
                		"path":res.data.path,
                		"type":parseInt($scope.apkType),
                		"level":parseInt($scope.level)
                	};
                	$scope.md5=tmp.md5;
                	console.log(tmp);
                	$http.post('/apk/process',tmp).success(function(res){
                		clearTimeout($scope.timer);
                		$('#terminal').append('<p>处理完毕，请转至其他页面查看</p>');
                		$rootScope.basic=res.data;
                	}).error(function(){
                		clearTimeout($scope.timer);
                		$('#terminal').append('<p>发生未知错误，请稍后再试</p>')
                	});
                	Window.query();
                	
//                    var skt=io.connect('localhost:8000');
//                    skt.on('connect',function(){
//                        skt.emit('req:apk',{
//                            path:res.data,
//                            type:$scope.apkType,
//                            malware:$scope.malware
//                        });
//                    });
//                    skt.on('res:process',function(res){
//                        $('#terminal').append('<p>'+res.msg+'</p>');
//                    });
//                    skt.on('res:err',function(res){
//                        $('#terminal').append('<p>发生错误:'+res.msg+'</p>');
//                        skt.close();
//                    });
//                    skt.on('res:end',function(res){
//                        $('#terminal').append('<p>'+res.msg+'</p>');
//                        skt.close();
//                        $http.post('/apk/select',{"id":res.data})
//                            .success(function(res){
//                               if(res.success){
//                                    $rootScope.basic=res.data;
//                               }
//                               else{
//                                   $('#terminal').append('<p>发生错误:'+res.msg+'</p>');
//                               }
//                            })
//                            .error(function(){
//                                   $('#terminal').append("<p>发生未知错误，请稍后再试</p>");
//                            });
//                    });
                }
                else{
                    $('#terminal').append('<p>发生错误:'+res.msg+'</p>');
                }
            }).error(function(){
                $('#terminal').append('<p>发生未知错误，请稍后再试</p>');
            });
        };
        $scope.cancel=function(){
            if($scope.xhr) $scope.xhr.abort();
        };
        
    })
    .controller('reportEditCtrl',function($scope,$rootScope,$http,Tool,$state){
        $scope.editable=false;$scope.display=false;
        $('.alert').css('display','none');
        $scope.apk={};$scope.isCreate=false;
        $scope.editor=new JSONEditor(document.getElementById('jsoneditor'));
        if($rootScope.basic){
            $scope.apk=$rootScope.basic;
            $('.alert').css('display','block');
            $scope.editor.set($scope.apk);
        }
        else{
        	
        	$http.get('/report/basic').success(function(res){
                if(res.success){
                    $rootScope.basic=res.data;
                    $scope.apk=$rootScope.basic;
                    $scope.editor.set($scope.apk);
                }
                else{
                    alert('当前并未选择应用，自动转为新建模式');
                    $scope.editor.set({});
                    $scope.editor.setMode('code');
                    $scope.isCreate=true;
                }
            }).error(function(){
                alert('未知错误，请稍后重试');
            });
        	
            
        }
        $scope.create=function(){
        	$scope.editor.set({});
        	$scope.editor.setMode('code');
        	$scope.isCreate=true;
        };
        $scope.save=function(){
        	myMode=$scope.isCreate?'create':'modify';
            $http.post('/report/edit',{
                operation:myMode,
                data:$scope.editor.get()
            }).success(function(res){
                if(res.success){
                    $rootScope.basic=$scope.apk=res.data;
                    $scope.context="保存成功";
                    $scope.display=true;
                    $scope.isCreate=false;
                    $scope.editor.set($scope.apk);
                    $scope.editor.setMode('tree');
                }
                else{
                    $scope.context=res.msg;
                    $scope.display=true;
                }
            }).error(function(){
                $scope.context="出现未知错误，请稍后再试";
                $scope.display=true;
            });
        };
        $scope.cancel=function(){
        	if($scope.isCreate){
            	$scope.isCreate=false;
            	$scope.editor.setMode('tree');
            }
            $scope.editor.set($scope.apk);
        };
        $scope.rmdoc=function(){
            $http.post('/report/edit',{
                operation:"delete",
                data:null
            }).success(function(res){
                if(res.success){
                    $scope.apk=null;$rootScope.basic=null;
                    $scope.editor.set({});
                    $scope.context="删除成功";
                    $scope.display=true;
                }
                else{
                    $scope.context=res.msg;
                    $scope.display=true;
                }
            }).error(function(){
                $scope.context="出现未知错误，请稍后再试";
                $scope.display=true;
            });
        };
        
    })
    .controller('recordCtrl',function($scope,$rootScope,$http,$upload){
        $scope.files=[];
        
        $scope.context="提交的报告必须是json文件，请参照我们给出的说明完成您的报告\
            ,其中有些属性的值必须填写，详细说明可以参照示例中的注释信息";
        $scope.$watch('files',function(){
            if(!$scope.files) return;
            if($scope.files.length<=0) return;
            //console.log($scope.files[0]);
            $scope.upload($scope.files[0]);
        });
        
        $scope.upload=function(file){
            $upload.upload({
                    url:'/apk/record',
                    file:file
                }).success(function(res){
                    console.log(res);
                    if(res.success){
                        $rootScope.basic=res.data;
                        $scope.context=file.name+':上传成功';
                    }
                    else{
                        $scope.context=file.name+':'+res.msg;
                    }
                }).error(function(){
                    $scope.context=file.name+':出现未知错误，请稍后再试';
                });
        };
    })
    .controller('setCtrl',function($scope,$rootScope,$http){
    	$scope.display=false;
    	$scope.refresh=function(){
    		$http.get('/system/info').success(function(res){
    			console.log(res.msg);
    			if(res.success){
    				$scope.methods=res.data['method']['available'];
    				$scope.current=res.data['method']['current'];
    				$scope.database=res.data['database'];
    			}
    			else{
    				$scope.context=res.msg;
    				$scope.display=true;
    			}
    		}).error(function(){
    			$scope.context='出现未知错误，请稍后再试';
    			$scope.display=true;
    		});
    	};
    	$scope.train=function(){
    		$http.get('/system/train').success(function(res){
    			if(res.success){
    				$scope.context="训练任务已加入队列";
    				$scope.display=true;
    			}
    			else{
    				$scope.contxt=res.msg;
    				$scope.display=true;
    			}
			}).error(function(){
				$scope.context='出现未知错误，请稍后再试';
    			$scope.display=true;
			});
    	};
    	$scope.editMethod=function(){
//    		console.log($scope.current);
    		$http.post('/system/editMethod',{
    			'method':$scope.current
    		}).success(function(res){
    			if(res.success){
    				$scope.context="检测方法更改成功";
    				$scope.display=true;
    			}
    			else{
    				$scope.contxt=res.msg;
    				$scope.display=true;
    			}
    		}).error(function(){
    			$scope.context='出现未知错误，请稍后再试';
    			$scope.display=true;
    		});
    	};
    	$scope.refresh();
    });

