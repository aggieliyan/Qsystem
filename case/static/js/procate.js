	
	//����һ��չ������ͼ��
    function first_change_minadd(id){
    	var firstid=$('#a1_first'+id);
		var classname=firstid.attr("class");
		//�����չ����,���������
		if(classname=='procate-a1_minus'){
			firstid.attr("class","procate-a1_add");
			$("#contain-secthird"+id).attr("style","display:none")
		}else{
			//���������ģ������չ��
			firstid.attr("class","procate-a1_minus");
			$("#contain-secthird"+id).attr("style","display:block")		
		}
      }
  
    function sec_change_minadd(id){
    	var secid=$('#a1_second'+id);
		var classname=secid.attr("class");
		//�����չ����,���������
		if(classname=='procate-a1_add'){
			secid.attr("class","procate-a1_minus");
			$("#third"+id).attr("style","display:block")
		}else{
			//���������ģ������չ��
			secid.attr("class","procate-a1_add");
			$("#third"+id).attr("style","display:none")		
		}
      }
    
    function add_firprocate(){
    	alert($('#as').attr('name'));
        $('#myModal').attr("style","display:block")	
        
      }
