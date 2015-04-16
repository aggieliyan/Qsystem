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
		/* 取共几页 */
		$.get("/case/totalpage", function(data,status){
			var json = eval ("(" + data + ")");
			$('#totalpage').text(json['totalpage']);
		});	
		/* 画左边的类目树 */
		$.get("/case/getprocate", function(data, status){
			var json = eval ("(" + data + ")");
			$('.tree li').remove();
			/*显示一级类目*/
			for(var key in json['1']){
				$('.tree').append('<li><input type="checkbox" id='+key+'><label>'+json['1'][key]+'</label></li>');
			};
			var level_flag = true; 
			/*往对应的一级类目下插二级类目*/
			for(var key in json['2']){
				if(level_flag){
					$('.tree #'+json['2'][key][0]).parent().append('<ul><li><input type="checkbox" id='+key+'><label>'+json['2'][key][1]+'</label></li></ul>');
					level_flag = false;
				} else {
					$('.tree #'+json['2'][key][0]).parent().children().eq(2).append('<li><input type="checkbox" id='+key+'><label>'+json['2'][key][1]+'</label></li>');
				}				
			}
			level_flag = true;
			/*往对应的二级类目下插三级类目*/
			for(var key in json['3']){
				if(level_flag){
					$('.tree #'+json['3'][key][0]).parent().append('<ul><li><input type="checkbox" id='+key+'><label>'+json['3'][key][1]+'</label></li></ul>');
					level_flag = false;
				} else{
					$('.tree #'+json['3'][key][0]).parent().children().eq(2).append('<li><input type="checkbox" id='+key+'><label>'+json['3'][key][1]+'</label></li>');
				}				
			}
			/*执行checkTree显示为树状结构*/
			$("ul.tree").checkTree({});			
		});
	});
	/* 跳转到第几页 */
	$('#go').click(function(){
		var num = $('#pagenum').val();
		var url = "/case/getcases/?page=" + num;
		ajaxClick(url);
	});
	/*  点全选*/
	$("#select_all_btn").click(function(){
		var a = $("#import_list_wrapper tr td label input");
	    if($(this).attr("checked")=="checked"){ 
	      for(var i=0;i<a.length;i++){
	    	  a.eq(i).attr("checked","checked");
	      }
	    }else{
	      for(var i=0;i<a.length;i++){
	        a.eq(i).removeAttr("checked");
	      }
	    }

	  });
});