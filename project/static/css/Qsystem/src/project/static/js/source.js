

$(document).ready(function(){

	// $("#newdept").hide();
     $(".def1").hide();
     $(".def2").hide();
     $(".def3").hide();
     $(".addsub").hide();
	 $(".minsub").hide();
	 $(".delsub").hide();
  // $(".s2").hide();
  // $(".s3").hide();
   	
	   
   //新建部门
   $(".btn-section").click(function()
  {  
  
 
	
  });
 
  
  
  //编辑
  

	$(".btn-edit").click(function()
  {  
  
	if($(".btn-edit").text()=="编辑"){
	  $(".btn-edit").text("完成");
      $(".addsub").show()
	  $(".minsub").show()
	  $(".delsub").show()
     
	  $("#sec1").removeAttr("onfocus");
	  $("#sec2").removeAttr("onfocus");
	  $("#sec3").removeAttr("onfocus");
	
   }
 	else{
	$(".btn-edit").text("编辑");
    $(".addsub").hide();
	$(".minsub").hide();
	$(".delsub").hide();

	$("#sec1").attr("onfocus","this.blur()");
	$("#sec2").attr("onfocus","this.blur()");
	$("#sec3").attr("onfocus","this.blur()");
	window.location.reload();
	}	

    });
	
 
   //add
	$("#add1a").click(function() {  
   

    $("div:eq(6)").clone(true).show().appendTo(".people");  
		
			
        }); 
	
	$("#add2a").click(function() {  
       
        $("div:eq(7)").clone(true).show().appendTo($(this).parent());  
			
        }); 
	
	$("#add3a").click(function() {  
            alert("不能添加第四级");  
        });
	
	
	$("#add1").click(function() {  
   

      $("div:eq(6)").clone(true).show().appendTo(".people");  
		
			
        }); 
	
	$(".ad2").click(function() {  
       
        $("div:eq(7)").clone(true).show().appendTo($(this).parent());  
			
        }); 
	 $(".ad3").click(function() {  
            alert("不能添加第四级");  
        });
  
	//删除类目
    $("#min1").click(function() {  
            alert('不能删除一级类目');  
        });		
			
		 
    $("#min2").click(function(){ 
		 
		var checkval=$(this).parent().has("#sec2").find("option:selected").val();//获取选择的iption value值
		
		 var child=$(this).parent().has(".s3");
		
	     if(child.length>0){
		  alert('该类目有子类，不能直接删除');
		  }
		  
		/* else if(checkval=="请选择"){
		   
		  $(this).parent().remove();
		  
		   }*/
		   	
        });  
   
		
	$("#min3").click(function() {  
	    
		 var checkval=$(this).parent().has("#sec3").find("option:selected").val();//获取选择的iption value值
	     if(checkval=="请选择"){
		 $(this).parent().remove();
		  }		
        }); 
	
	//删除用户
	$("#del1").click(function() {    
		
		var checkval=$(this).parent().has("#sec1").find("option:selected").val();//获取选择的option value值
		if(checkval=="请选择"){
		alert("当前没有用户");
		}
		else {
		$(this).parent().has("#sec1").find("OPTION:selected").remove();
		}
   
		 });
	
	$("#del2").click(function() {    
		var checkval=$(this).parent().has("#sec2").find("option:selected").val();//获取选择的option value值
		if(checkval=="请选择"){
		alert("当前没有用户");
		}
		/*
		else {
		$(this).parent().has("#sec2").find("OPTION:selected").remove();
		}
   */
		 });
	
	 $("#del3").click(function() {   
		var checkval=$(this).parent().has("#sec3").find("option:selected").val();//获取选择的option value值
		if(checkval=="请选择"){
		alert("当前没有用户");
		}
		/*
		else {
		$(this).parent().has("#sec3").find("OPTION:selected").remove();
		}
   */
		 });
				
});

  
