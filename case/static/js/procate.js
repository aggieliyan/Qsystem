
	//处理一级展开收缩图标
    function first_change_minadd(id){
    	var firstid=$('#a1_first'+id);
		var classname=firstid.attr("class");
		//如果是展开的,点击后收缩
		if(classname=='procate-a1_minus'){
			firstid.attr("class","procate-a1_add");
			$("#contain-secthird"+id).attr("style","display:none")
		}else{
			//就是收缩的，点击后展开
			firstid.attr("class","procate-a1_minus");
			$("#contain-secthird"+id).attr("style","display:block")		
		}
      }
  
    function sec_change_minadd(id){
    	var secid=$('#a1_second'+id);
		var classname=secid.attr("class");
		//如果是展开的,点击后收缩
		if(classname=='procate-a1_add'){
			secid.attr("class","procate-a1_minus");
			$(".procate-third"+id).attr("style","display:block")
		}else{
			//就是收缩的，点击后展开
			secid.attr("class","procate-a1_add");
			$(".procate-third"+id).attr("style","display:none")		
		}
      }
    
    //一级产品模块弹窗
    function add_firprocate(){
	       $('#project_id').val("");
	       $('#procate_title').val("");
        $('#myModal').modal('show');
    }

    function check_projectid(obj){
    	var proid = obj.value.replace(/(^\s*)|(\s*$)/g,"");
    	if(proid.length!=0 && (proid <= 0 || proid >999999999 || proid!=parseInt(proid))){
    		window.checkvar = 0;
    	}
    	else{
    		window.checkvar = 1;
    	}
    }
 
   function check_protitle(obj){
	var title = obj.value.replace(/(^\s*)|(\s*$)/g,"");
	if(!title || title.length>30){
         window.checkvar = 0;
     }
	else{
		window.checkvar = 1;
	}
   }
   
    //添加验证输入框
    function chk(){
        var proid = document.test.project_id.value.replace(/(^\s*)|(\s*$)/g,"");
        //先判断填写项是否符合规格
        if(window.checkvar == 0){
            alert('编号为正整数且不超过9位数；模块名称不能为空且不超过30个字符！');
        }else if(proid.length == 0){
        	$("#project_id").val(proid);
        	document.test.submit();
        }else{
            //再判断项目编号之前是否填写过
            url = "/case/has_proid";
            para = {"proid":proid};
            var has_pro = "";
            $.get(url, para, function(data){
                has_pro = eval('('+data+')');
                if(has_pro != "no"){
                	getname = has_pro.split("has")[0];
                	alert("项目编号已被模块名称为“"+getname+"”关联！");	
                } 	
                else{
                	$("#procate_btn").attr("disabled","true");
                    document.test.submit();	
                }
            });
        } 
      }

    //编辑验证输入框
    function chk1(){
        var proid = document.test1.project_id1.value.replace(/(^\s*)|(\s*$)/g,"");
        var procate_id = document.test1.procate_id1.value;
        //先判断填写项是否符合规格
        if(window.checkvar == 0){
            alert('编号为正整数且不超过10位数；模块名称不能为空且不超过30个字符！');
        }else if(proid.length == 0){
        	$("#project_id").val(proid);
        	document.test1.submit();
        }else{
            //再判断项目编号之前是否填写过
            url = "/case/has_proid";
            para = {"proid":proid};
            $.get(url, para, function(data){
                has_pro = eval('('+data+')');
                getid = has_pro.split("has")[1];
                if(has_pro != "no" && procate_id != getid){
                	getname = has_pro.split("has")[0];
                	alert("项目编号已被模块名称为“"+getname+"”关联！");	
                } 	
                else{
                	$("#procate_btn1").attr("disabled","true");
                    document.test1.submit();	
                }
            });
        }     
      }
    
   //添加产品模块
   function add_procate(id,level){
	   if( level==3){
		  alert('三级产品模板不能添加子模块！');
		  return
	   }
	   else{
	       $('#procate_id').val(id);
	       $('#procate_level').val(level);
	       $('#project_id').val("");
	       $('#procate_title').val("");
		   $('#myModal').modal('show'); 
	   } 
   }
   
  //编辑产品模块
  function edit_procate(id,name){
	   url = "/case/get_proid"
	   para = {"procate_id":id}
	   $.get(url, para, function(data){
	       var proid = eval('('+data+')');
	       $('#project_id1').val(proid);
	     });
       $('#procate_id1').val(id);
	   $('#procate_title1').val(name);
	   $('#myModal1').modal('show');
  }  

//删除产品模块
 function del_procate(id){
     url = "/case/delprocate_confirm"
     para = {"procate_id":id}
     $.get(url, para, function(data){
         var according = eval('('+data+')');
         if(according == "has_son"){
            $('#lab_del').text('该模块有子模块，不能被删除！');    	
            $('#myModal_del_no').modal('show'); 
         }
         else if(according == "has_case"){
            $('#lab_del').text('该模块下包含用例，不能被删除！');    	
            $('#myModal_del_no').modal('show'); 
         }
         else{
           $('#procate_id_del').val(id);
           $('#myModal_del').modal('show'); 
         }
     })      
 }
   
 function setup(){
     $("#procate_btn_del").attr("disabled","true"); 
 }
 
//  $(document).ready(function(){
// 	 $(".on_myproject").each(function(){
// 		 val = $(this).text();
// 		 if(val.length > 20){
// 			 newval = val.substring(0,20)+"...";
// 			 $(this).text(newval);
// 		 }	 
//      }); 
// });
   
 
 
 