
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
        $('#myModal').modal('show');
    }

    //添加验证输入框
    function chk(){
        var title = document.test.procate_title.value.replace(/(^\s*)|(\s*$)/g,"");;
        if(!title){
            alert('产品模块名称不能为空！');
        }
        else if(title.length>30){
            alert('产品模块名称不能超过30个字符！');
        }
        else{
            document.test.submit();
        } 
      }
   
    //编辑验证输入框
    function chk1(){
        var title = document.test1.procate_title1.value.replace(/(^\s*)|(\s*$)/g,"");;
        if(!title){
            alert('产品模块名称不能为空！');
        }
        else if(title.length>30){
            alert('产品模块名称不能超过30个字符！');
        }
        else{
            document.test1.submit();
        } 
      }
    
   //添加产品模块
   function add_procate(id,level){
	   if( level==3){
		  alert('三级产品模板不能添加子模块！');
		  return
	   }
	   else if(level==1 || level==2){
	       $('#procate_id').val(id);
	       $('#procate_level').val(level);
		   $('#myModal').modal('show'); 
	   }
	   else{
		   $('#myModal').modal('show');    
	   }
  
   }
   
  //编辑产品模块
  function edit_procate(id,name){
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
 //点击时将父级id写入cookie
 // var cate1 = $.cookie("c1");
 // var cate2 = $.cookie("c2");
 // var cate3 = $.cookie("c3");
 //    //alert("tabcookievalue="+tabcookievalue); v 
 //    $(".procate-a2").click(function(){
 //      $.cookie("mytab", $(this).index());
 //    });
   
   

   