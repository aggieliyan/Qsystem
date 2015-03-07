$(document).ready(function(){

    var casehtml = "<tr class=\"mtr\"><td><input class=\"casecheck\" type=\"checkbox\" checked='checked'>1</td>"+
			      		"<td class=\"editable\"></td>"+
			      		"<td class=\"editable\"></td>"+
			    		"<td class=\"editable\"></td>"+
			      		"<td>2</td>"+
			      		"<td></td>"+
			    		"<td class=\"editable\">-</td>"+
			      		"<td></td>"+
			      		"<td></td>"+
			      		"<td class=\"editable\">-</td>"+
			      		"<td>"+
			      			"<a class=\"icon-plus\" title=\"添加用例\"></a> "+
			      			"<a class=\"icon-download-alt\" title=\"引入用例\"></a> "+
			      			"<a class=\"icon-eye-open\" title=\"查看结果\"></a> "+
			      			"<a class=\"icon-trash\"></a>"+
			      		"</td>"+			
			    	"</tr>";

    var modulehtml = "<tr class=\"cmodule\">"+
	    		"<td colspan=\"11\">"+
	    			"<div>"+
	    				"<table >"+
	    					"<tbody>"+
	    						"<tr class=\"success\">"+
						    		"<td colspan=\"1\"><input class=\"modulecheck\" type=\"checkbox\" checked='checked'></td>"+
						    		"<td colspan=\"9\" class=\"editable\"></td>"+
						    		"<td >"+
						      			"<a class=\"icon-plus-sign\" title=\"添加模块\"></a> "+
						      		    "<a class=\"icon-plus\" title=\"添加用例\"></a> "+
						      		    "<a class=\"icon-trash\"></a> "+
						    		"</td>"+
	    						"</tr>"+
	    						casehtml +
	    					"</tbody>"+
	    				"</table>"+
	    			"</div>"+
	    		"</td>"+
	    	"</tr>"
    // click create case
    $("#newcase").click(function(){
        $(".mtr").last().after(casehtml);
    });

	$(".editable").live('dblclick', function(){
		var tdnode = $(this);
		var tdTest = tdnode.text();
		//before属性用来存点击时文本域的值
		tdnode.attr("before", tdTest);
   
		tdnode.empty();
		var tx = $("<textarea class='edittx'></textarea>");
		tx.attr("value", tdTest);
		tdnode.append(tx);
		tx.focus();
	});

	$(".edittx").live('blur', function(){
		var tx = $(this);
		var etext = tx.val();
		var tp = tx.parent();
		tx.remove();
		tp.attr("value", etext);
		tp.html(etext);
		//文本框的值与原来的值不同时，勾上checkbox
		if(tp.attr("before") !== etext){
			tp.siblings().eq(0).find("input").attr("checked", "checked");
		}

	});

	//插入模块后用例后，赋rank值

    //添加用例
    $(".icon-plus").live("click", function(){
        $(this).parent().parent().after(casehtml);
    });

    //添加模块
    $(".icon-plus-sign").live('click', function(){
        $(this).parents(".cmodule").after(modulehtml);
    });

    function checkall(master, slave){
        if(master.attr("checked")=="checked"){ 
        	slave.each(function(){
        		$(this).attr("checked","checked");
        	});
        }else{
         	slave.each(function(){
        		$(this).removeAttr("checked");
        	});
        }
    }

    //全选
    $("#caseall").click(function(){
    	var slave = $("#caselist").find("input");
    	checkall($(this), slave);
    });

    $(".modulecheck").live('click', function(){
    	var slave = $(this).parents(".cmodule").find("input");
    	checkall($(this), slave);
    });

    function update_rank(){

    	var celement = $(this);
    	var pelement = celement.prev();
    	if(pelement.length == 0 || pelement.attr("class") !== celement.attr("class")){
    		celement.attr("rank", "1");
    	}
    	else{
    		celement.attr("rank", parseInt(pelement.attr("rank"))+1);

    	}
    	celement.find("input").eq(0).attr("checked", "checked");
    	var classname = celement.attr("class")
    	var nx = celement.nextAll().filter("."+classname);
    	nx.each(function(){
    		var newrank = parseInt($(this).attr("rank"))+1;
    		$(this).attr("rank", newrank);
    		$(this).find("input").eq(0).attr("checked", "checked");
    	});

    }

    //模块拖拽
    $("#caselist tbody").dragsort({
    	dragSelector:".cmodule",
    	dragEnd:update_rank,
    });
    //用例拖拽
    $(".cmodule tbody").dragsort({
    	dragSelector:".mtr",
    	dragEnd:update_rank,
    });

    //删除
    $(".icon-trash").live('click', function(){

    	if(confirm("你确定要删除吗？")){
    		var node = $(this).parent().parent();
    		if(node.attr("class") == "mtr"){//删除用例
    			node.remove();
    		}else{//删除模块
    		  
    		    //找到该模块的前一个模块下的
    		    var currentm = node.parents(".cmodule")
	    		var prevmodule = currentm.prev().find('tbody');

	    		if(prevmodule.length){
	    			//克隆一份该模块下的用例
	        		var snode = node.siblings().clone(true);

	        		//将这些将被转移的用例checkbox都勾上因为父级模块变了
	        		snode.each(function(){
	        			$(this).find(".casecheck").attr("checked", "checked");
	        		});

                    //删掉该模块,将模块下用例复制到前一个模块下
	        		currentm.remove();
	        		prevmodule.append(snode);
    		    }else{
    		    	alert("抱歉~第一个模块不能删除。");
    		    }
            }
    	}
    });



});