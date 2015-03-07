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

    // click + 
    $(".icon-plus").live("click", function(){
        $(this).parent().parent().after(casehtml);
    });

    $(".icon-plus-sign").live('click', function(){
        $(this).parents(".cmodule").after(modulehtml);
    });

    //全选
    $("#caseall").click(function(){
    	var a = $(".casecheck")
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

    $("#caselist tbody").dragsort({
    	dragSelector:".cmodule",
    	dragEnd:function(){
    		console.log("ok");
    	},
    });

    $(".cmodule tbody").dragsort({
    	dragSelector:".mtr",
    	dragEnd:function(){
    		console.log("ok");
    	},
    });

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