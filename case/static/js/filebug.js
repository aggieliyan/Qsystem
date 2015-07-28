function inputFileOnChange() {   
	if($('#my-file').val()){
		$('#path').attr("value", $('#path').val() + "C:\\bugPic\\" + $('#my-file').val() + ";");
	}
}; 
function fileBug(obj) {
	var result = $(obj).children().eq(1).val();
	var wid = $(obj).next().children().text();
	if(result!="Pass"){
		if(wid==""){
			$('#fileBugLabel').text("新建问题");
			$('#type select').val('');
			$('#status input').eq(0).attr("checked","checked");
			$('#environment select').val('');
			$('#subject input').attr("value","");
			$('#description textarea').attr("value","");
			$('#priority select').val('2');
			$('#assign_to select').val('');
			$('#path').attr("value","");    //清除之前弹框填写的数据
			$('#fileBugForm').attr("action", "/case/newbug/");
			$('#fileBugModal').modal('show');
			$(obj).next().attr("id", "bugId"); //做个标记，知道更新哪条用例的bug
		} else {
			$.get('/case/getwi/'+wid+'/', function(data, status){
				issue = eval('('+data+')');
				$('#fileBugLabel').text('#'+wid);
				$('#type select').val(issue['type']);
				issue['status']==4? $('#status input').eq(1).attr("checked","checked"):$('#status input').eq(0).attr("checked","checked");
				$('#environment select').val('');
				$('#subject input').attr("value",issue['subject']);
				$('#description textarea').attr("value", issue['description']);
				$('#priority select').val(issue['PRI']);
				$('#assign_to select').val(issue['assign_to']);
				// var path = '';
				// for(var pa in issue['uploads']){
				//	 path = path + "C:\\bugPic\\" + issue['uploads'][pa] + ";";
				// } //不显示路径了，因为只能增不能减，显示会重复提交
				//$('#path').attr("value",path);
				$('#fileBugForm').attr("action", "/case/newbug/"+wid+"/");
				$('#fileBugModal').modal('show');
				$(obj).next().attr("id", "bugId");		
			});
		}
	} else {
		wid && $.post('/case/closewi/'+wid+'/', function(data, status){
				
			});
		}	
}
function checkForm() {
	var flag = true;
	$('.item_cont').children().each(function(){
		if($(this).val()==''&&$(this).parent().parent().attr("id")!="attachment"){
			alert('请检查必填项都已填写');
			flag = false;
			return false;  //只是跳出了循环
		};		
	});
	if(flag){
		if($('#subject input').val().length>=140||$('#description textarea').val().length>=1000){
			alert('主题不能超过140字，描述不能超过1000字！');
			return false;
		} else {
			$('#fileBugForm').submit;
		}
	} else {
		return false;
	}
}
$('#fileBugModal').on('hidden', function(){ //为了保证标记的唯一性，所以要及时去掉无用的标记
	$('#bugId').removeAttr("id");
});
$('#refreshwi').click(function(){
	var buglist = '';
	for(var i=0; i<$('.wi').length; i++){
		if($('.wi a').eq(i).text()!=""){  
			buglist = buglist + '_' + $('.wi a').eq(i).text();
		}
	}
	$.get('/case/getstatus/'+buglist+'/', function(data, status){
		uplist = eval('('+data+')');
		for (var wi in uplist){
			if(uplist[wi]==3){    //不同状态在页面做不同提示
				$('#'+wi).append('&nbsp<i class="icon-star" title="已解决"></i>');
			}
			else if(uplist[wi]==5){
				$('#'+wi).remove();
			}
			else if(uplist[wi]=="err"){
				$('#'+wi).append('&nbsp<i class="icon-exclamation-sign" title="WI填写有误，请检查！"></i>');
			};
		};
	});
});
$(document).ready(function(){	
	$.get('/case/filebug/', function(data, status){
		var json = eval("(" + data + ")");
		for (var id in json){	
			$("#assign_to select").append("<option value=" + id +">" + json[id] + "</option>");
		};		
	});
	$('#fileBugForm').ajaxForm(function(data, status) {//提交完表单成功后做以下操作
		var bug = eval("(" + data + ")");	
		buglink = '<a href=http://gj.ablesky.com/issues/'+bug+' target="_blank">'+bug+'</a>';
		$('#bugId a').remove();
		$('#bugId').append(buglink);
		tid = $('#bugId').parent().attr("value");
		$('#bugId a').attr("id",bug); 
		var url = "/case/updateresult/";
        var para = {"tname":"wi", "tid":tid, "tcnt":bug};
        $.post(url, para, function(data){
            var rs = eval('('+data+')');
            if(rs.success){
                //alert("ok");
            }else{
                alert(rs.message);
            }
        }); 
		$('#fileBugModal').modal('hide'); 		
     });
});
