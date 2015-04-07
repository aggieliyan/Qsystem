$(document).ready(function(){
/*    var swidth = $(window).width();
    console.log(swidth);
    console.log("width:"+swidth+"px;");
    $(".fixbar").attr("style", "width:"+swidth+"px;");*/

    var casehtml = "<tr class=\"mtr\" value=\"\"><td><input class=\"casecheck\" type=\"checkbox\" checked='checked'>1</td>"+
			      		"<td class=\"editable nodrag\"></td>"+
			      		"<td class=\"editable nodrag\"></td>"+
			    		"<td class=\"editable nodrag\"></td>"+
			      		"<td class=\"nodrag\">2</td>"+
			      		"<td class=\"nodrag\"><a class=\"icon-play-circle\"></a></td>"+
			    		"<td class=\"editable nodrag\">-</td>"+
			      		"<td></td>"+
			      		"<td></td>"+
			      		"<td class=\"editable nodrag\">-</td>"+
			      		"<td class=\"nodrag\">"+
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

    var resulthtml = "<select class=\"cresult\">"+
                        "<option>-</option>"+
                        "<option>Pass</option>"+
                        "<option>Fail</option>"+
                        "<option>block</option>"+
                    "</select>"

    var levelhtml = "<select class=\"lselect\">"+
                        "<option>1</option>"+
                        "<option>2</option>"+
                        "<option>3</option>"+
                    "</select>"


	function insert_update_rank(celement){	
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

    function delete_update_rank(celement){
    	var nextele = celement.next();
    	if(nextele.length !== 0){
	    	var classname = celement.attr("class")
	    	var nx = celement.nextAll().filter("."+classname);
	    	nx.each(function(){
	    		var newrank = parseInt($(this).attr("rank"))-1;
	    		$(this).attr("rank", newrank);
	    		$(this).find("input").eq(0).attr("checked", "checked");
	    	});
	    	//如果删掉模块，模块下用例的rank值也要变化
	    	if(classname == "cmodule"){
	    		var ccase = celement.find(".mtr");
	    		var cnum = celement.prev().find(".mtr").length;
	    		var i = 1;

		    	ccase.each(function(){
		    		var newrank = cnum+i;
		    		i = i+1;
		    		$(this).attr("rank", newrank);
		    		$(this).find("input").eq(0).attr("checked", "checked");
		    	});	    		
	    	}  	
    	}
    }

    // click create case
    $("#newcase").click(function(){
        $(".mtr").last().after(casehtml);
        insert_update_rank($(".mtr").last());

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


    //点击选择级别
    $(".level").live('dblclick', function(){
        var tdnode = $(this);
        var tdTest = tdnode.text();
        tdnode.empty();
        var tx = $(levelhtml);
        tx.attr("value", tdTest);
        tdnode.append(tx);
    })

    $(".lselect").live('change', function(){
        var tx = $(this);
        var etext = tx.val();
        var tp = tx.parent();
        tx.remove();
        tp.attr("value", etext);
        tp.html(etext);
        tp.siblings().eq(0).find("input").attr("checked", "checked");    
    })

    //点击执行用例
    $(".icon-play-circle").live('click', function(){
        var caseid = $(this).parents(".mtr").attr("value");
        if(caseid !== ""){//有用例id的才可以执行
            $(this).next().next().remove();
            var sel = $(this).next();
            if(sel.length == 0){
                $(this).after(resulthtml);
                $(this).toggle();       
            }else{
                sel.toggle();
                $(this).toggle();
            }
        }

    });
    $(".cresult").live('change', function(){
        var result = $(this).val();
        $(this).prev().toggle();
        $(this).after("<span>"+result+"<span>");
        $(this).toggle();
    })

	//插入模块后用例后，赋rank值

    //添加用例
    $(".icon-plus").live("click", function(){
    	var ccase = $(this).parent().parent();
        ccase.after(casehtml);
        insert_update_rank(ccase.next());
    });

    //添加模块
    $(".icon-plus-sign").live('click', function(){
        var cmodule = $(this).parents(".cmodule");
        cmodule.after(modulehtml);
        update_rank(cmodule.next());
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






    function drag_update_rank(){
    	insert_update_rank($(this));
    }

    //模块拖拽
    $("#caselist tbody").dragsort({
    	dragSelector:".cmodule",
    	dragEnd:drag_update_rank,
    });
    //用例拖拽
    $(".cmodule tbody").dragsort({
    	dragSelector:".mtr",
        dragSelectorExclude:".nodrag",
    	dragEnd:drag_update_rank,
    });

    //删除
    $(".icon-trash").live('click', function(){

    	if(confirm("你确定要删除吗？")){
    		var node = $(this).parent().parent();
    		if(node.attr("class") == "mtr"){//删除用例
    			delete_update_rank(node);
    			node.remove();
    		}else{//删除模块
    		  
    		    //找到该模块的前一个模块下的
    		    var currentm = node.parents(".cmodule")
	    		var prevmodule = currentm.prev().find('tbody');

	    		if(prevmodule.length){

	        		//更新rank值
	        		delete_update_rank(currentm);

	    			//克隆一份该模块下的用例
	        		var snode = node.siblings().clone(true);

	        		//将这些将被转移的用例checkbox都勾上因为父级模块变了
	        		snode.each(function(){
	        			$(this).find(".casecheck").attr("checked", "checked");
	        		});

	        		//删掉

                    //删掉该模块,将模块下用例复制到前一个模块下
	        		currentm.remove();
	        		prevmodule.append(snode);
    		    }else{
    		    	alert("抱歉~第一个模块不能删除。");
    		    }
            }
    	}
    });


    //搜索模块js       
    var url = "/case/casecate/";
    var areaJson;
    var temp_html;
    var category1 = $(this).find(".category_select_1");
    var category2 = $(this).find(".category_select_2");
    var category3 = $(this).find(".category_select_3");      
     //初始化一级类目
    var category_select_1 = function(){
        var c1=$(".cate1").val();
        temp_html="<option>"+'全部'+"</option>";
        $.each(areaJson,function(i,category_select_1){
             temp_html+="<option value='"+category_select_1.masterid+"'>"+category_select_1.master+"</option>";
        });
        category1.html(temp_html); 
        var n = category1.get(0).selectedIndex;
        console.log(n);
        if(c1){
            $(".category_select_1 option[value="+c1+"]").attr("selected","true")
        }       
        if(n != 0){
            if((areaJson[n-1].slist).length != 0){
            category2.show();
            category_select_2();
            console.log("mmm");
            if (!c1){
                $(".cate").attr("value",'aa');
            }                    
            $(".cate1").attr("value",category1.children().eq(n).val());
        };
        }else{
          category2.hide();
          category3.hide();  
        }

                       
     };
    //赋值二级
    var category_select_2 = function(){
        var c2=$(".cate2").val();
        temp_html="<option>"+'请选择'+"</option>"; 
        var n = category1.get(0).selectedIndex;
        console.log(n);
        if(n !=0 ){
            if((areaJson[n-1].slist).length == 0){
            category2.css("display","none");
            category3.css("display","none");
        }else{
            $.each(areaJson[n-1].slist,function(i,category_select_2){
                temp_html+="<option value='"+category_select_2.secondid+"'>"+category_select_2.second+"</option>";
            });
            category2.html(temp_html);
            if(c2){
                $(".category_select_2 option[value="+c2+"]").attr("selected","true");
            }
            category_select_3();
        };
        }                    
    };
    //赋值三级
    var category_select_3 = function(){
        var c3=$(".cate3").val();
        temp_html="<option>"+'请选择'+"</option>"; 
        var m = category1.get(0).selectedIndex;
        var n = category2.get(0).selectedIndex;
        if(c3){
            category3.css("display","inline");
            $.each(areaJson[m-1].slist[n-1].thirdlist,function(i,category_select_3){
                temp_html+="<option value='"+category_select_3.thirdid+"'>"+category_select_3.third+"</option>";
            });
            category3.html(temp_html);
            $(".category_select_3 option[value="+c3+"]").attr("selected","true");
        }else{
            if(n != 0){
                if((areaJson[m-1].slist[n-1].thirdlist).length == 0){
                    category3.css("display","none");
                }else{
                    category3.css("display","inline");
                    $.each(areaJson[m-1].slist[n-1].thirdlist,function(i,category_select_3){
                        temp_html+="<option value='"+category_select_3.thirdid+"'>"+category_select_3.third+"</option>";
                    });
                    category3.html(temp_html);
                };
            }else{
                category3.css("display","none");
            };
        }                                
    };        

    //选择一级改变二级
    category1.change(function(){
        var c1=$(".cate1").attr('value','');
        var c2=$(".cate2").attr('value','');
        var c3=$(".cate3").attr('value','');

        category2.show();
        category3.hide();
        category_select_2();
    });
    //选择二级改变三级
    category2.change(function(){
        var c3=$(".cate3").attr('value','');
        category3.hide();
        category_select_3();
    });
    //获取json数据
    $.getJSON(url,function(data){
        areaJson = data;
        category_select_1();
    });

    $('.selectList select').live('click',function(){
        if ($(this).val() !== '请选择'){
            $(".cate").attr("value",$(this).val());
            $(".next").attr("action","/case/caselist/" + $(this).val() + "/");
        }
    });

    $('.category_select_1').click(function(){
        $(".cate1").attr("value",$(this).val());
    });

    $('.category_select_2').live('click',function(){
        if ($(this).val() !== '请选择'){
            $(".cate2").attr("value",$(this).val());
        }
    });
    $('.category_select_3').live('click',function(){
        if ($(this).val() !== '请选择'){
            $(".cate3").attr("value",$(this).val());
        }
    }); 


     // 展开/收起搜索项
     $("#searchicon").click(function(){
        $("#searchbar").toggle();
    });
    //状态没有选中时，隐藏执行结果类型 
    $('.statue').click(function(){
        if ($(this).val() !== ''){
            $(".mold").show();            
        }else{
            $(".mold").hide();
        }
    });

    if($(".hide-statue").val()){
        $(".statue").removeAttr("selected");
        $(".statue option[value="+$(".hide-statue").val()+"]").attr("selected",true);
        $(".mold").show();
        if ($(".hide-mold").val()){
            $(".mold").removeAttr("selected");
            $(".mold option[value="+$(".hide-mold").val()+"]").attr("selected",true);
        }
    };

     $(".form_datetime").datetimepicker({
        format: "yyyy-mm-dd",
        autoclose: true,
        todayBtn: true,
        pickerPosition: "bottom-left",
        language:"zh-CN",
        minView:2 
      });
     

/*    $(window).bind('beforeunload', function(){

    });*/
/*
    window.onbeforeunload = function(event){return confirm("确定离开此页面吗？"); }*/
});