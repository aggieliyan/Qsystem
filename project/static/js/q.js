<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" /> 
<meta http-equiv="Content-Language" content="zh-CN" /> 
<meta content="all" name="robots" /> 
<meta name="Copyright" content="" /> 
<meta name="description" content="" /> 
<meta content="" name="keywords" /> 
<link rel="stylesheet" type="text/css" href="css.css" /> 
<title>原料库管理</title> 
<script> 
function Page(iAbsolute,sTableId,sTBodyId,page) 
{ 
this.absolute = iAbsolute; //每页最大记录数 
this.tableId = sTableId; 
this.tBodyId = sTBodyId; 
this.rowCount = 0;//记录数 
this.pageCount = 0;//页数 
this.pageIndex = 0;//页索引 
this.__oTable__ = null;//表格引用 
this.__oTBody__ = null;//要分页内容 
this.__dataRows__ = 0;//记录行引用 
this.__oldTBody__ = null; 
this.__init__(); //初始化; 
}; 
/**//* 
初始化 
*/ 
Page.prototype.__init__ = function(){ 
this.__oTable__ = document.getElementById(this.tableId);//获取table引用 
this.__oTBody__ = this.__oTable__.tBodies[this.tBodyId];//获取tBody引用 
this.__dataRows__ = this.__oTBody__.rows; 
this.rowCount = this.__dataRows__.length; 
try{ 
this.absolute = (this.absolute <= 0) || (this.absolute>this.rowCount) ? this.rowCount : this.absolute; 
this.pageCount = parseInt(this.rowCount%this.absolute == 0 
? this.rowCount/this.absolute : this.rowCount/this.absolute+1); 
}catch(exception){} 
this.__updateTableRows__(); 
}; 
Page.prototype.GetBar=function(obj) 
{ 
var bar= document.getElementById(obj.id); 
bar.innerHTML= "每页"+this.absolute+"条/共"+this.rowCount+"条";// 第2页/共6页 首页 上一页 1 2 3 4 5 6 下一页 末页 
} 
/**//* 
下一页 
*/ 
Page.prototype.nextPage = function(){ 
if(this.pageIndex + 1 < this.pageCount){ 
this.pageIndex += 1; 
this.__updateTableRows__(); 
} 
}; 
/**//* 
上一页 
*/ 
Page.prototype.prePage = function(){ 
if(this.pageIndex >= 1){ 
this.pageIndex -= 1; 
this.__updateTableRows__(); 
} 
}; 
/**//* 
首页 
*/ 
Page.prototype.firstPage = function(){ 
if(this.pageIndex != 0){ 
this.pageIndex = 0; 
this.__updateTableRows__(); 
} 
}; 
/**//* 
尾页 
*/ 
Page.prototype.lastPage = function(){ 
if(this.pageIndex+1 != this.pageCount){ 
this.pageIndex = this.pageCount - 1; 
this.__updateTableRows__(); 
} 
}; 
/**//* 
页定位方法 
*/ 
Page.prototype.aimPage = function(){ 
var abc = document.getElementById("pageno"); 
var iPageIndex = abc.value; 
var iPageIndex = iPageIndex*1; 
if(iPageIndex > this.pageCount-1){ 
this.pageIndex = this.pageCount -1; 
}else if(iPageIndex < 0){ 
this.pageIndex = 0; 
}else{ 
this.pageIndex = iPageIndex-1; 
} 
this.__updateTableRows__(); 
}; 
/**//* 
执行分页时，更新显示表格内容 
*/ 
Page.prototype.__updateTableRows__ = function(){ 
var iCurrentRowCount = this.absolute * this.pageIndex; 
var iMoreRow = this.absolute+iCurrentRowCount > this.rowCount ? this.absolute+iCurrentRowCount - this.rowCount : 0; 
var tempRows = this.__cloneRows__(); 
var removedTBody = this.__oTable__.removeChild(this.__oTBody__); 
var newTBody = document.createElement("TBODY"); 
newTBody.setAttribute("id", this.tBodyId); 
for(var i=iCurrentRowCount; i < this.absolute+iCurrentRowCount-iMoreRow; i++){ 
newTBody.appendChild(tempRows[i]); 
} 
this.__oTable__.appendChild(newTBody); 
this.__dataRows__ = tempRows; 
this.__oTBody__ = newTBody; 
//页脚显示分 
var divFood = document.getElementById("divFood");//分页工具栏 
divFood.innerHTML=""; 
var rightBar = document.createElement("divFood"); 
rightBar.setAttribute("display",""); 
rightBar.setAttribute("float","left"); 
rightBar.innerHTML="第"+(this.pageIndex+1)+"页/共"+this.pageCount+"页"; 
var isOK="Y"; 
var cssColor=""; 
divFood.appendChild(rightBar); 
////页脚显示分页结 
}; 
/**//* 
克隆原始操作行集合 
*/ 
Page.prototype.__cloneRows__ = function(){ 
var tempRows = []; 
for(var i=0; i<this.__dataRows__.length; i++){ 
tempRows[i] = this.__dataRows__[i].cloneNode(1); 
} 
return tempRows; 
}; 
</script> 
<script type="text/javascript" language="javascript"> 
window.onload = function(){ 
page = new Page(3,'senfe','group_one'); }; 
</script> 
<style type="text/css"><!-- 
#senfe { 
border-top: #000 1px solid; 
border-left: #000 1px solid; 
} 
#senfe td { 
border-right: #000 1px solid; 
border-bottom: #000 1px solid; 
} 
--></style> 
<script language="javascript"><!-- 
function senfe(o,a,b,c,d){ 
var t=document.getElementById(o).getElementsByTagName("tr"); 
for(var i=0;i<t.length;i++){ 
t[i].style.backgroundColor=(t[i].sectionRowIndex%2==0)?a:b; 
} 
} 
--></script> 
</head> 
<body> 
<div> 
<table border="0" cellpadding="0" cellspacing="0" bordercolor="#006600" id="senfe"> 
<thead> 
<tr align="center" valign="middle"> 
<td width="46" height="23" bgcolor="#FFFFFF">编号</td> 
<td width="71" bgcolor="#FFFFFF"><select name="select" dir="ltr"> 
<option>套类别</option> 
<option>A套</option> 
<option>B套</option> 
</select></td> 
<td width="53" bgcolor="#FFFFFF">名称</td> 
<td width="53" bgcolor="#FFFFFF">数量</td> 
<td width="53" bgcolor="#FFFFFF">单价</td> 
<td width="95" bgcolor="#FFFFFF"><select name="select" dir="ltr"> 
<option>单位</option> 
<option>个</option> 
<option>双</option> 
</select></td> 
<td width="80" bgcolor="#FFFFFF">酒店名称</td> 
<td width="35" bgcolor="#FFFFFF">备注</td> 
</tr> 
</thead> 
<tbody id="group_one"> 
<tr> 
<td>1</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>2</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>3</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>4</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>5</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>6</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>7</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>8</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
<tr> 
<td>9</td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
<td> </td> 
</tr> 
</tbody> 
</table> 
<script language="javascript"><!-- 
//senfe("表格名称","奇数行背景","偶数行背景","鼠标经过背景","点击后背景"); 
senfe("senfe","#fff","#ccc","#cfc","#f00"); 
--></script> 
</div> 
<div><a href="#" onclick="page.firstPage();">首 页</a>/<a href="#" onclick="page.nextPage();">下一页</a>/<a href="#" onclick="page.prePage();">上一页</a>/<a href="#" onclick="page.lastPage();">末 页</a><span id="divFood"> 
</span> 
/第 
<input id="pageno" value="1" style="width:20px"/>页/<a href="#" onclick="page.aimPage();">跳转</a></div> 
</div> 
</div> 
</body> 
</html>