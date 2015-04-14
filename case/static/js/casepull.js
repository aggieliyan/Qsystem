function ajaxClick(url){
		$.get(url, function(data, status){
			var json = eval ("(" + data + ")");
			$('#import_list tr').remove();
			for(var key in json['actionlist']){			
				$('#import_list').append('<tr><td class="text-left first-cell"><label class="import-list-item clearfix"><input type="checkbox" value="'+key+'" style="margin-right:10px;"><p>'+json['actionlist'][key]+'</p></label></td></tr>');
			}
			
			if (json['prelink']){
				$('.previous').removeClass('disabled');
				$('.previous a').attr("onclick", "ajaxClick('"+json['prelink']+"')");
			} else{
				$('.previous').addClass('disabled');
			}
			if (json['nextlink']){
				$('.next').removeClass('disabled');
				$('.next a').attr("onclick", "ajaxClick('"+json['nextlink']+"')");
			} else{
				$('.next').addClass('disabled');
			}			
		});	
	};
$(document).ready(function(){	
	$('#pullbutton').click(function(){
		var url = "/case/getcases/?page=1/";
		ajaxClick(url);
		});
	$('#go').click(function(){
		var num = $('#pagenum').val();
		var url = "/case/getcases/?page=" + num;
		ajaxClick(url);
	});
});