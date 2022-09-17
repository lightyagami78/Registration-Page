window.onload=function()
{
    xname.focus();
}

function validation(){
    var username=document.getElementById('xname').value;
    // var email=document.getElementById('xmail').value;
    var phone=document.getElementById('xphone').value;
    var password=document.getElementById('xpass').value;
    var vpassword=document.getElementById('xvpass').value;

    var usercheck= /^[A-Za-z. ]{3,30}$/ ;
    var passwordcheck= /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$/ ;
    // var emailcheck= /^[A-Za-z_]{3,}@[A-Za-z]{3,}[.]{1}[A-Za-z.]{2,6}$/ ;
    var mobilecheck = /^[789][0-9]{9}$/ ;

    if(usercheck.test(username)){
        document.getElementById('usererror').innerHTML = " ";
    }
    else{
        document.getElementById('usererror').innerHTML = "** Username is Invalid";
        return false;
    }

    // if(emailcheck.test(email)){
    //     document.getElementById('emailerror').innerHTML = " ";
    // }
    // else{
    //     document.getElementById('emailerror').innerHTML = "** Email is Invalid";
    //     return false;
    // }
    
    if(mobilecheck.test(phone)){
        document.getElementById('mobileerror').innerHTML = " ";
    }
    else{
        document.getElementById('mobileerror').innerHTML = "** Mobile No. is Invalid";
        return false;
    }
    
    if(passwordcheck.test(password)){
        document.getElementById('passworderror').innerHTML = " ";
    }
    else{
        document.getElementById('passworderror').innerHTML = "** Password is Invalid";
        return false;
    }

    if(vpassword.match(password)){
        document.getElementById('vpassworderror').innerHTML = " ";
    }
    else{
        document.getElementById('vpassworderror').innerHTML = "** Password isn't same";
        return false;
    }

}