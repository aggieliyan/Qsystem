function inputFileOnChange() {   
	if($('#file_upload1').val()){
		$('#path').attr("value", $('#path').val() + $('#file_upload1').val() + ";");
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
			content = "\r编号：" + $(obj).parent().children().eq(0).text().trim() + "\r" + "前置条件：" + $(obj).parent().children().eq(1).text() + "\r" + "输入/动作："+ $(obj).parent().children().eq(2).text() + "\r" + "期望输出："+ $(obj).parent().children().eq(3).text() + "\r";
			$('#description textarea').attr("value",content);
			$('#priority select').val('2');
			$('#assign_to select').val('');
			$('#file_upload1-queue').children().remove();  //清除之前弹框填写的数据
			$('#path').attr("value","");
			$('#cid').attr("value",$('.category_select_3').val());
			$('#create').removeAttr("disabled");			
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
				var path = '';
				for(var pa in issue['uploads']){
					path = path + issue['uploads'][pa] + ";&nbsp;&nbsp;&nbsp";
				 } //不显示路径了，因为只能增不能减，显示会重复提交
				$('#file_upload1-queue').children().remove();
				$('#file_upload1').before("");
				$('#file_upload1').before(path);
				$('#path').attr("value","");
				$('#my-file').attr("value",""); 
				$('#cid').attr("value", issue['cid']);
				$('#create').removeAttr("disabled");
				$('#fileBugForm').attr("action", "/case/newbug/"+wid+"/");
				$('#fileBugModal').modal('show');
				$(obj).next().attr("id", "bugId");		
			});
		}
	} else {
		$(obj).next().text('');
		wid && $.post('/case/closewi/'+wid+'/');
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
			$('#fileBugForm').submit();
			$('#create').attr('disabled',"true");
		}
	} else {
		return false;
	}
}
$('#fileBugModal').on('hidden', function(){ //为了保证标记的唯一性，所以要及时去掉无用的标记
	$('#bugId').removeAttr("id");
});
$('#refreshwi').click(function(){
	var buglist = {};
	for(var i=0; i<$('.wi').length; i++){
		if($('.wi a').eq(i).text()!=""){
			tid = $('.wi a').eq(i).parent().parent().attr("value");
			wid = $('.wi a').eq(i).text();
			buglist[tid] = wid;
		}
	}
	$.get('/case/getstatus/', buglist, function(data, status){
		uplist = eval('('+data+')');
		for (var wi in uplist){
			if(uplist[wi]==3){    //不同状态在页面做不同提示
				$('.'+wi).append('&nbsp<i class="icon-star" title="已解决"></i>');
			}
			else if(uplist[wi]==5){
				num = $('.'+wi).length;
				for(var i=num-1; i>=0; i--){					
					$('.'+wi).eq(i).parent().prev().children('span').attr("class","Pass");
					$('.'+wi).eq(i).parent().prev().children('span').text(" Pass");
					$('.'+wi).eq(i).parent().next().next().text("Redmine更新");
					$('.'+wi).eq(i).parent().next().next().next().text("#"+wi);
					$('.'+wi).eq(i).remove();						
				}
			}
			else if(uplist[wi]=="err"){
				$('.'+wi).append('&nbsp<i class="icon-exclamation-sign" title="WI不存在，请检查！"></i>');
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
		$('#create').removeAttr("disabled");
		var bug = eval("(" + data + ")");	
		if(bug['failed']){ 
			alert(bug['message']);
			return false;
		}
		buglink = '<a href=http://gj.ablesky.com/issues/'+bug+' target="_blank">'+bug+'</a>';
		$('#bugId a').remove();
		$('#bugId').append(buglink);
		tid = $('#bugId').parent().attr("value");
		$('#bugId a').attr("class",bug); 
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
    $('#file_upload1').uploadify({		
        'swf'  : '/static/jquery/uploadify.swf',
        'uploader'  : '/case/upload_script/',  
        'auto'      : true , 
        'removeCompleted':false,  
        'buttonText': '选择文件' , 
		'onUploadSuccess': function(file, data, response){
			var result = eval('(' + data + ')');
			$("#path").attr("value", $("#path").val()+result['old_name']+":"+result['save_name']+",");
		}
  });
});
