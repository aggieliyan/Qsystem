$(document).ready(function(){
		// 实现下拉、收起，并动态生成表格，异步展示数据
		var id=0;
		$(".flip").click(function(){
		    if ($(".panel").length != id){
				id++;
			}
			$(this).toggleClass("drapdown");
			pid = $(this).attr("value");
			var panel = $(this).parent().parent().next(".panel");
			if(panel.length == 0){
				$(this).parent().parent().after("<tr class='panel'><td colspan=5 id='"+id+"'></td></tr>");
				var url = "/sflip/" + pid;
				$.get(url, function(data, status){
					var datalist = eval ("(" + data + ")");
					var num = datalist.length;
					for(var i=0;i<num;i++){
						$("#"+id).append("<div><div style='float:left;width:500px;'><p>"+datalist[i].item+":"+"</p><p>"+datalist[i].num+"</p></div><div style='float:right;width:600px;'><div style='width:60%;'><canvas id='canvas"+id+datalist[i].sql+"' height='2' width='3'></canvas></div></div></div>");
						if(i<num-1){
							$("#"+id).append("<div><p style=\"color:#7B7B7B\">-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------</p></div>");
						}
					}				
				});				
				setTimeout(500);
				show_graph(pid,id);			
			}
			else{
				panel.toggle();
				}
			});
		// 全选和取消全选
		$("#chk_all").click(function(){
			if(typeof($("#chk_all").attr("checked"))=="undefined")
				$("input[name='chk_list']").removeAttr("checked");
			else
				$("input[name='chk_list']").attr("checked",$(this).attr("checked"));
		});
		// 批量操作，批量添加模块
		$("#bulk_add").click(function(){
			var arrChk=$("input[name='chk_list']:checked");
			var value = '';
			$(arrChk).each(function(){
				value=this.value + "," + value;
			});
			if (value) {
				$("#bulk_sid").val(value);
				$("#addmodule").modal('show')
			}			
			else{
				alert("请勾选项目后再进行批量操作！");
			}				
		});		
	});

	function s_operate(id){
        $('#bulk_sid').val(id);
        $('#addmodule').modal('show');
      }