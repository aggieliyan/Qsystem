/* 为了点击类目将模块信息传给右边下拉菜单，使用全局变量 */
var m_menu = new Array();
/* 用例列表内容和翻页链接*/
function ajaxClick(url){
	$.get(url, function(data, status){
		var json = eval ("(" + data + ")");
		$('#import_list tr').remove();
		for(var key in json['actionlist']){			
			$('#import_list').append('<tr><td class="text-left first-cell"><label class="import-list-item clearfix"><input onclick="change(this)" type="checkbox" value="'+key+'" style="margin-right:10px;"><p>'+json['actionlist'][key]+'</p></label></td></tr>');
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
		if (json['golink']){
			$('#go').attr("value", json['golink']);
		}
	});			
};
/* 点击选择用例 */
function change(obj){
	if ($(obj).attr("checked")=="checked"){
		$(obj).attr("checked", "checked");
	}else{
		$(obj).removeAttr("checked");
	}	
}
/* 勾选分类赋值给模块下拉列表 */
function menu_val(){
	$('.cc-textbox option').remove();
	$('.cc-textbox').append('<option value="">请选择模块</option>');
	for (var key in m_menu){
		if ($('.tree #'+key).attr("checked")=="checked"){
			for (var i in m_menu[key][0]){
					$('.cc-textbox').append('<option value='+m_menu[key][0][i]+'>'+m_menu[key][1][i]+'</option>');				
			}			
		};
	};
}
/* 搜索用例 */
function search_case(){
	var a = $('.tree ul li ul li input');
    for(var i=0;i<a.length;i++){
    	if(a.eq(i).attr("checked")=="checked"){
    		if(i==0){
    			$('#cate_ids').val(a.eq(i).attr("id"));
    		}else{
    			$('#cate_ids').val($('#cate_ids').val()+","+a.eq(i).attr("id"));
    		}
    	};
      }
    url = "/case/getcases/?page=1&mid="+$('.cc-textbox').val()+"&cids="+$('#cate_ids').val()+"&skey="+$('#search_text').val();
    ajaxClick(url);
}

$(document).ready(function(){	
	$('#pullbutton').click(function(){
		var url = "/case/getcases/?page=1/";
		ajaxClick(url);
		/* 取共几页 */
		$.get("/case/totalpage/", function(data,status){
			var json = eval ("(" + data + ")");
			$('#totalpage').text(json['totalpage']);
		});	
		/* 画左边的类目树 */
		$.get("/case/getprocate/", function(data, status){
			var json = eval ("(" + data + ")");
			$('.tree li').remove();
			/*显示一级类目*/
			for(var key in json['1']){
				$('.tree').append('<li><input type="checkbox" id='+key+'><label>'+json['1'][key][0]+'</label></li>');
			};
			/*往对应类目下插入子类目*/
			other = [json['2'], json['3']];
			var m_names = new Array();
			var m_ids = new Array();
			for(var i in other){
				for(var key in other[i]){
					/* 只循环第三级（末级）类目下关联的模块 ，默认其它非末级类目下没有模块*/
					if (i==1){	
						m_names = [];
						m_ids = [];
						for(var k in other[i][key][2]){	
							m_names[k]=other[i][key][2][k];
							m_ids[k]=k;
							}
						m_menu[key] = [m_ids, m_names];
					};
				/* 这时候还没执行checkTree(),所以是小于3，或是等于2 */
					if($('.tree #'+other[i][key][0]).parent().children().length<3){
						$('.tree #'+other[i][key][0]).parent().append('<ul><li><input type="checkbox" id='+key+'><label>'+other[i][key][1]+'</label></li></ul>');
					} else {
						$('.tree #'+other[i][key][0]).parent().children().eq(2).append('<li><input type="checkbox" id='+key+'><label>'+other[i][key][1]+'</label></li>');
					}				
				}				
			}
			/*执行checkTree显示为树状结构*/
			$("ul.tree").checkTree({});
			$("ul.tree .checkbox").attr("onclick", "menu_val()");
		});		
	});
	/* 跳转到第几页 */
	$('#go').click(function(){
		var num = $('#pagenum').val();
		var url = $(this).attr("value") + num;
		ajaxClick(url);
	});
	/* 点全选 */
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