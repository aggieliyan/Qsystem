
 //新建部门
  $(document).ready(function(){

	$(".btn-section").click(function()
  {  
  
	alert('ok');
 
  });
 
  });
  
  //编辑
  $(document).ready(function(){

	$(".btn-edit").click(function()
  {  
  
	if($(".btn-edit").text()=="编辑"){

      $(".btn-edit").text("完成");
   }
 	else{
	$(".btn-edit").text("编辑");
	
	}	
 
  });
 
  });
 
//addsub
$(document).ready(function(){

$("#addsub").click(function()
  {  
   alert('ok');
   $("<p/>").appendto(".people").html("#section2");
	
         
  });
 
  });
  
  
  
  //minsub
  $(document).ready(function(){

	$("#minsub").click(function()
  {  
   //alert('ok');

   $(this).parent().remove();
   
 	
  lert('ok');
  });
 
  });
  
   //delsub
  $(document).ready(function(){

	$("#delsub").click(function()
  {  
    var obj = document.getElementById("section1");
 
    obj.remove(obj.selectedIndex)
	
	
   
  });
 
  });
  
  
  
