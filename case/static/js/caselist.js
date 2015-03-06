$(document).ready(function(){

    var casehtml = "<tr><td><input class=\"casecheck\" type=\"checkbox\">1</td>"+
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
			      			"<a class=\"icon-plus\"></a> "+
			      			"<a class=\"icon-plus-sign\"></a> "+
			      			"<a class=\"icon-download-alt\"></a> "+
			      			"<a class=\"icon-eye-open\"></a> "+
			      			"<a class=\"icon-trash\"></a>"+
			      		"</td>"+			
			    	"</tr>";

    var modulehtml = "<tr class=\"cmodule success\">"+
	    		"<td colspan=\"1\"><input class=\"modulecheck\" type=\"checkbox\"></td>"+
	    		"<td colspan=\"9\" class=\"editable\"></td>"+
	    		"<td >"+
	    		    "<a class=\"icon-arrow-up\"></a> "+
	      			"<a class=\"icon-arrow-down\"></a> "+
	      		    "<a class=\"icon-plus\"></a> "+
	      		    "<a class=\"icon-trash\"></a> "+
	    		"</td>"+
	    	"<tr>"
    // click create case
    $("#newcase").click(function(){
        $("#caselist").children('tbody').append(casehtml);
    });

	$(".editable").live('dblclick', function(){

		var tdnode = $(this);
		var tdTest = tdnode.text();
   
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

	});

   // click + 
   $(".icon-plus").live("click", function(){
        $(this).parent().parent().after(casehtml);
   });

   $(".icon-plus-sign").live('click', function(){
        $(this).parent().parent().after(modulehtml);
   });

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

    $(".icon-arrow-up").live("click", function(){

    });



});