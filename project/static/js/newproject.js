$(document).ready(function(){

     function show_staff (person){
        $("#testerlist div").remove();
        for(var i=0; i<person.length;i++){
          $("#testerlist table").append("<div class=\"table-list\"><input id='"+person[i].id+"' type=\"checkbox\"><span>"+person[i].realname+"</span></div>");
        }
     }
    
    //选择人员后点确定，在页面显示已选人员
    $("#test").click(function(){
      var testerlist = $("#testerlist input");
    	var jsontester = { tester:[]};
      if(testerlist.length == 0){
	      console.log('no data');
     	}
	    for (var i = testerlist.length - 1; i >= 0; i--) {
	      var item = testerlist.eq(i);
	      if(item.attr("checked") === "checked"){
		      var temp = {value:item.attr("id"), name:item.parent().text()};
		      jsontester.tester.push(temp);
	      }
	      //console.log(jsontester);
	    }
        $("[title='1']").children("div").remove();
        for (var i= jsontester.tester.length-1; i >=0; i--){
            $("[title='1']").append('<div class="role-item" value="' + jsontester.tester[i].value+'" type="radio"><span>'+jsontester.tester[i].name+'</span><span class="close">x</span></div>');
        }	

        pl = $("[title='1']").children("div").length;
        console.log(pl);
        if(pl >= 8){
          w = (pl/5+1)*30;
          $("[title='1']").attr("style","height:"+w+"px;");
        }
        $("[title='1']").attr("title","0");

    });

    $(".role-item .close").live('click',function(){
        $(this).parent().remove();
    });
    
    //点添加
    $(".roles .btn-success").click(function(){      
      $("#select").modal("show");
      var roles = $(this).attr("name"); 
      $("#psearch").attr("value",roles)
      var p = $("[title='1']");
      var num = p.length;
      if(num > 0){
        for(var i=0;i<num;i++){
          p.eq(i).attr("title","0");
        }
      }
 
      $(this).next().attr("title","1");

      var url="/showperson";
      var para="role=" + roles;
      $.get(url, para, function(data, status){
        var person = eval('('+data+')')
        person = person.person
        show_staff(person);
        //$("#testerlist div").remove();
        //for(var i=0; i<person.length;i++){
        //  $("#testerlist table").append("<div class=\"table-list\"><input id='"+person[i].id+"' type=\"checkbox\"><span>"+person[i].realname+"</span></div>");
       // }
      });
    });

   //选择人员框里搜索
   $("#psearch").click(function(){
      var skey = $("#skey").val();
      if(skey.length >0){
        url = "/psearch"
        para = "key="+skey
        $.get(url, para, function(data){
          var person = eval('('+data+')')
          person = person.person
          show_staff(person);
        });    
      }

   });

    //选择项目负责人
    $("#master").focus(function(){
      p = $(".role-item");  
      $("#master").children("option").remove();
      var idlist =" ";
      for(var i=p.length-1; i >=0; i--){
        item = p.eq(i);
        $("#master").append("<option value="+item.attr("value")+">"+item.children('span').eq(0).text()+"</option>");
        //console.log(item.children('span').eq(0).text());
        idlist = idlist + item.attr("value") + ","
      } 
      console.log(idlist);
      $("[name='relateduser']").attr("value",idlist);
    });
    
    $("#master").blur(function(){
      var p = $('#master option:selected').val();
      //console.log(typeof(p));
      $("[name='leader']").attr("value",p);
    });

    //计算天数
    $(".range input").change(function(){
        var endtime = $(this).val().split("-", 3);
        var s = $(this).parent().prev("span").prev("span");
        if(s.length > 0){
          var startime = s.eq(0).children('input').val().split("-", 3);
          var stime = Date.UTC(startime[0], startime[1], startime[2]);
          var etime = Date.UTC(endtime[0], endtime[1], endtime[2]);
          var diff = etime - stime; 
          var days = diff/1000/60/60/24 + 1;
          $(this).parent().siblings('div').children('span').text(days);
        }
    });

});
