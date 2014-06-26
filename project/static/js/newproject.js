$(document).ready(function(){
	count_relateduser();
	init0();
	
	function init0(){
		var a = window.location.pathname;
		if (a == "/newproject/"){
			$(".init0").attr("value",0);
	}
		
	}
	function show_staff (person){
      if(person.length > 0){
        $("#testerlist div").remove();
        for(var i=0; i<person.length;i++){
          $("#testerlist table").append("<div class=\"table-list\"><input id='"+person[i].id+"' type=\"checkbox\"><span>"+person[i].realname+"</span></div>");
        }
      }
      else{
        $("#testerlist div").remove();
        $("#testerlist table").append("<div>暂无数据<div>");
      } 
    }

    function findmaster (plist) {
      for(var i=0;i<plist.length;i++){
        item = plist.eq(i);
        if(item.children("input")[0].checked){
          return item.attr("value");
        }
      }
      //没找到
      return ""
    }
    
    function set_other_master(){
      var pm = $(".p-list").eq(0).children();
      var tm = $(".p-list").eq(2).children();
      var d = findmaster(pm);
      var t = findmaster(tm);

      $("[name='designer']").attr("value",d); 
      $("[name='tester']").attr("value",t);   
    } 


    function count_relateduser(){
      var p = $(".role-item");  
      var idlist =" ";
      for(var i=p.length-1; i >=0; i--){
        var item = p.eq(i);
        idlist = idlist + item.attr("value") + ","
      } 
      $("[name='relateduser']").attr("value",idlist);
    }
    
    $("input:first").blur(function(){
      if(parseInt($(this).attr("value")) > 1000){
        $(this).attr("style","border-color:red");
      }else{
        $(this).attr("style","border-color: #ccc");
      }

    });


    //选择人员后点确定，
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
	    }
      $("[title='1']").children("div").remove();
      //在页面显示已选人员
      var radioname = Math.floor(Math.random()*9999+1).toString();
      for (var i= jsontester.tester.length-1; i >=0; i--){
        $("[title='1']").append('<div class="role-item" value="' + jsontester.tester[i].value+'"><input type="radio" name='+radioname+'><span>'+jsontester.tester[i].name+'</span><span class="close">x</span></div>');
      }	
      
      //跟数量调整高度
      pl = $("[title='1']").children("div").length;
      if(pl >= 8){
        w = (pl/4+1)*30;
        $("[title='1']").attr("style","height:"+w+"px;");
      }
      $("[title='1']").attr("title","0");
      //负责人还在的话要选中
      var dv = $("[name='designer']").attr("value")
      var tv = $("[name='tester']").attr("value")
      if(dv){
        $("[value='"+dv+"'] input").attr("checked","checked");
      }
      if(tv){
        $("[value='"+tv+"'] input").attr("checked","checked");
      }

      //设置项目参与人员
      count_relateduser()

      //设置产品测试负责人
      set_other_master()

    });


    //删除人员,重新数一遍参与人员
    $(".role-item .close").live('click',function(){
        $(this).parent().remove();

        count_relateduser()
    });
    
    //点添加，弹出人员选择框展示数据
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
        allperson = eval('('+data+')');//全局变量
        allperson = allperson.person;
        var num = allperson.length;
        pagemaxnum = 45//全局变量
        var pnum = num/pagemaxnum;
        var anum = Math.floor(pnum);
        anum < pnum ? pagenum = anum+1 : pagenum = anum
        $(".pagination ul li").remove()
        $(".pagination ul").append("<li><a href=\"#\">&laquo;</a></li><li><a href=\"#\">&raquo;</a></li>");
        for(var i=0; i<pagenum; i++){
          var page = i+1;
          $(".pagination ul li:last").before("<li><a>"+page+"</a></li>");
        }
        if(pagenum>1){
          person = allperson.slice(0,pagemaxnum);
        }
        else{
          person = allperson;
        }
        show_staff(person);

        p = $("[title='1']").children();
        for(var i=0;i<p.length;i++){
          //选中之前已经选过的
          $("#"+p.eq(i).attr("value")).attr("checked","checked");
        }

      });
    

    });

   //点页码
  $(".pagination li").live('click',function(){
    var page = parseInt($(this).text());
    //console.log(allperson);
    var start = (page-1)*pagemaxnum;
    person = allperson.slice(start, start+pagemaxnum);
    console.log(person);
    show_staff(person);
  });

   //选择人员框里搜索
  $("#psearch").click(function(){
      var skey = $("#skey").val();
      if(skey.length >0){
        url = "/psearch"
        para = "key="+skey
        $.get(url, para, function(data){
          var person = eval('('+data+')');
          person = person.person;
          show_staff(person);
        });    
      }

   });

    //选择项目负责人
    $("#master").focus(function(){
      p = $(".role-item");  
      $("#master").children("option").remove();
      //var idlist =" ";
      for(var i=p.length-1; i >=0; i--){
        item = p.eq(i);
        $("#master").append("<option value="+item.attr("value")+">"+item.children('span').eq(0).text()+"</option>");
      } 

      //set_other_master();
    });
    
    $("#master").blur(function(){
      console.log("hahahah");
      var p = $('#master option:selected').val();
      //console.log(typeof(p));
      $("[name='leader']").attr("value",p);

      //设置测试和产品负责人
     // set_other_master();

    });

    $(".role-item input").live('click',function(){
      set_other_master();
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
