$(document).ready(function(){
    


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

   $("icon-plus").live("click", function(){
   	   var casehtml = "<tr><td><input class=\"casecheck\" type=\"checkbox\">1</td>"+
	      		"<td class=\"editable\"></td>"+
	      		"<td class=\"editable\"></td>"+
	    		"<td class=\"editable\"></td>"+
	      		"<td>2</td>"+
	      		"<td>PASS</td>"+
	    		"<td class=\"editable\">-</td>"+
	      		"<td>2015/01/01</td>"+
	      		"<td>易璐璐</td>"+
	      		"<td class=\"editable\">-</td>"+
	      		"<td>"+
	      			"<a class=\"icon-plus\"></a>"+
	      			"<a class=\"icon-download-alt\"></a>"+
	      			"<a class=\"icon-eye-open\"></a>"+
	      			"<a class=\"icon-trash\"></a>"+
	      		"</td>"+			
	    	"</tr>";
       console.log($(this));
       $(this).parents("tbody").append(casehtml);

   });

});