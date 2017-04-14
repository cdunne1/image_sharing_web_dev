function zoomImage(id) {                                  // function to allow zoom on image in landing gallery
    document.getElementById(id).style.width = "500px";
    document.getElementById(id).style.height = "500px";
    }
function deeZoooooom(id) {                                  // remove zoom on image in landing gallery
    document.getElementById(id).style.height = "auto";
    document.getElementById(id).style.width = "300px";
    //document.getElementById(id)
    }
function goToDetailedImageView(deets){
    console.log(deets);
    window.location.href = "/image_details?image_name=" + deets[0] + "&uploader=" + deets[1] + "&time_uploaded=" + deets[2];
}
function validateFileUpload(fld) {                                     // validate correct file format uploaded
    if(!/(\.bmp|\.gif|\.jpg|\.jpeg|\.png)$/i.test(fld.value)) {       // code from http://stackoverflow.com/questions/833012/how-to-validate-a-file-upload-field-using-javascript-jquery
        alert("Invalid image file type.");
        fld.form.reset();
        fld.focus();
        return false;    }
    return true;
 }
function validateEmail() {                          //https://www.w3schools.com/js/tryit.asp?filename=tryjs_form_validate_email
    var x = document.forms["reg_user"]["email"].value;
    var atpos = x.indexOf("@");
    var dotpos = x.lastIndexOf(".");
    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length) {
        alert("Not a valid e-mail address");
        return false;
    }
}
