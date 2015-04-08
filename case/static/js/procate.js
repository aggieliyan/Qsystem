
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
    	
    function add_firprocate(){
        $('#myModal').modal('show');
    }

    function chk(){
        var title = document.test.procate_title.value.replace(/(^\s*)|(\s*$)/g,"");;
        if(!title){
            alert('产品模块名称不能为空！');
        }
        else if(title.length>30){
            alert('产品模块名称不能超过30个字符！');
        }
        else{
            $("#procate_btn").attr("disabled","true");
            document.test.submit();
        } 
      }
    
   function add_subprocate(id,level){
	   if( level== 3){
		  alert('三级产品模板不能添加子模块！');
		  return
	   }
       $('#procate_id').val(id);
       $('#procate_level').val(level);
       alert(('#procate_id').val());
	   $('#myModal').modal('show');
	      
   }
   
   
   
   
   
   