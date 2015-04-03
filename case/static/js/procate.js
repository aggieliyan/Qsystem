	
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
			$("#third"+id).attr("style","display:block")
		}else{
			//就是收缩的，点击后展开
			secid.attr("class","procate-a1_add");
			$("#third"+id).attr("style","display:none")		
		}
      }
    
    function add_firprocate(){
    	alert($('#as').attr('name'));
        $('#myModal').attr("style","display:block")	
        
      }
