function togglePassword()
{
   var passType = document.getElementById("password");
  if (passType.type === "password") {
    passType.type = "text";
	document.getElementById("passVisibility").src = "https://icon-library.net/images/white-eye-icon/white-eye-icon-4.jpg";
  } else {
    passType.type = "password";
	document.getElementById("passVisibility").src = "https://icon-library.net/images/white-eye-icon/white-eye-icon-4.jpg";
  }
}

function validateLogin() {
  var flag = true;
  var emailId = document.forms["userForm"]["email"].value;
  var passWord = document.forms["userForm"]["password"].value;
  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (emailId === "") {
    document.getElementById("emailid").style.borderColor = "red";
    document.getElementById("invalidEmail").innerHTML =
      "*Email id is mandatory";
    flag = false;
  } else if (!emailId.match(mailformat)) {
    document.getElementById("emailid").style.borderColor = "red";
    document.getElementById("invalidEmail").innerHTML =
      "*Please enter valid email.";
    flag = false;
  } else {
    document.getElementById("emailid").style.borderColor = "transparent";
    document.getElementById("invalidEmail").innerHTML = "";
  }
  if (passWord == "") {
    document.getElementById("password").style.borderColor = "red";
    document.getElementById("invalidPass").innerHTML = "*Password is mandatory";
    flag = false;
  } else {
    document.getElementById("password").style.borderColor = "transparent";
    document.getElementById("invalidPass").innerHTML = "";
  }
  if (flag) {
    document.getElementById("notification").innerHTML = "Login Success!!";
  } else {
    document.getElementById("notification").innerHTML = "";
  }
}

function validateEmail(email)
{
	var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	 if (email === "") {
	document.getElementById("emailid").style.borderColor = "hsl(0, 0%, 10%)";	
  	}
	else if (!email.match(mailformat)) {
    	document.getElementById("emailid").style.borderColor = "red";
  	} else {
    	document.getElementById("emailid").style.borderColor = "#28B463";
  }
}

function showdesc(desc){
	document.getElementById("login-desc").innerHTML = desc;
}
