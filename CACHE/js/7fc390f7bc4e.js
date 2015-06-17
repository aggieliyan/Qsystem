$(".reply-btn").bind("click",function(){var i=$(this).attr('id');var rpid="#rp"+i;$(rpid).attr("style","display:block");});$(".cancle-reply").click(function(){var i=$(this).attr('id');var rpid="#rp"+i;$(rpid).attr("style","display:none");});function feedbacktext(){var text=document.feedbackForm.content.value;if(text=="请输入您想要反馈的问题，最多不要超过300字哟！"){$(".feedback").attr("style","width:700px; margin-top:20px; margin-bottom:20px; background:#ffe4e1");try{alert("反馈内容不能为空！")}
finally{return false;}}
else if(text.length>300){$(".feedback").attr("style","width:700px; margin-top:20px; margin-bottom:20px; background:#ffe4e1");try{alert("反馈内容不能超过300字")}
finally{return false;}}
else{$("#sendfeedbacbtn").attr("disabled","");document.feedbackForm.submit();}}
function commenttext(id){var text=$("#"+id.replace("_","")).val();if(!text){$(".feedback-reply").attr("style","width:600px; margin-top:20px; margin-bottom:20px; background:#ffe4e1");try{alert("回复内容不能为空！")}
finally{return false;}}
else if(text.length>300){$(".feedback-reply").attr("style","width:600px; margin-top:20px; margin-bottom:20px; background:#ffe4e1");try{alert("回复内容不能超过300字")}
finally{return false;}}
else{$("#"+id).attr("disabled","");$("#form"+id.split("_")[1]).submit();}}