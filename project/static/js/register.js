var nameId;
var name;
var pwd;
var repeaPwd;
var departmentid;
var flag = true;
var errorMessage = "";

function init() {
	flag = true;
	errorMessage = "";
	nameId = document.getElementById("Text_nameid").value;
	name = document.getElementById("Text_name").value;
	pwd = document.getElementById("Text_password").value;
	repeaPwd = document.getElementById("Text_repeatpassword").value;
	departmentid = document.getElementById("Select_part").value;
	document.getElementById("nameIdErrorMsg").innerHTML = errorMessage;
	document.getElementById("nameErrorMsg").innerHTML = errorMessage;
	document.getElementById("pwdErrorMsg").innerHTML = errorMessage;
	document.getElementById("repeatpwdErrorMsg").innerHTML = errorMessage;
	document.getElementById("departmentidErrorMsg").innerHTML = errorMessage
}
function checkRegistMsg() {
	init();
	checkRegIsNull();
	return flag
}
function checkRegIsNull() {
	if (!isNull(nameId)) {
		errorMessage = "请输入帐号";
		document.getElementById("nameIdErrorMsg").innerHTML = errorMessage;
		flag = false
	} else {
		if (getByteLen(nameId) < 6 || getByteLen(nameId) > 40) {
			errorMessage = "帐号长度为3-20位字符";
			document.getElementById("nameIdErrorMsg").innerHTML = errorMessage;
			flag = false
		} else {
			if (!nameId.match(/^[a-zA-Z0-9_]{1,}$/)) {
				errorMessage = "帐号只能输入英文、数字或下划线";
				document.getElementById("nameIdErrorMsg").innerHTML = errorMessage;
				flag = false
			}
		}
	}
	if (!isNull(name)) {
		errorMessage = "请输入姓名";
		document.getElementById("nameErrorMsg").innerHTML = errorMessage;
		flag = false
	} else {
		if (getByteLen(name) < 6 || getByteLen(name) > 40) {
			errorMessage = "姓名长度为3-20位字符";
			document.getElementById("nameErrorMsg").innerHTML = errorMessage;
			flag = false
		} else {
			if (!name.match(/^[a-zA-Z_一-龥]+$/)) {
				errorMessage = "姓名只能输入中文、英文或下划线";
				document.getElementById("nameErrorMsg").innerHTML = errorMessage;
				flag = false
			}
		}
	}
	if (!isNull(pwd)) {
		errorMessage = "请输入密码";
		document.getElementById("pwdErrorMsg").innerHTML = errorMessage;
		flag = false
	} else {
		if (getByteLen(pwd) < 4 || getByteLen(pwd) > 64) {
			errorMessage = "密码长度为4-32位字符";
			document.getElementById("pwdErrorMsg").innerHTML = errorMessage;
			flag = false
		}
	}
	if (!isNull(repeaPwd)) {
		errorMessage = "请输入确认密码";
		document.getElementById("repeatpwdErrorMsg").innerHTML = errorMessage;
		flag = false
	}
	if (pwd != "" && pwd != repeaPwd) {
		errorMessage = "两次输入的密码不一致";
		document.getElementById("repeatpwdErrorMsg").innerHTML = errorMessage;
		flag = false
	}
	if (!isNull(departmentid)) {
		errorMessage = "请选择您所在的部门";
		document.getElementById("departmentidErrorMsg").innerHTML = errorMessage;
		flag = false
	}
}
function isNull(text) {
	if (text == "") {
		return false
	} else {
		return true
	}
}
function getByteLen(val) {
	var len = 0;
	for (var i = 0; i < val.length; i++) {
		var a = val.charAt(i);
		if (a.match(/[^-ÿ]/ig) != null) {
			len += 2
		} else {
			len += 1
		}
	}
	return len
};