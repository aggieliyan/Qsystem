
 //�½�����
  $(document).ready(function(){

	$(".btn-section").click(function()
  {  
  
	alert('ok');
 
  });
 
  });
  
  //�༭
  $(document).ready(function(){

	$(".btn-edit").click(function()
  {  
  
	if($(".btn-edit").text()=="�༭"){

      $(".btn-edit").text("���");
   }
 	else{
	$(".btn-edit").text("�༭");
	
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
  
  
  
