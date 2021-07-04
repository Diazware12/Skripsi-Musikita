
//register sign-up modal
$("#register").on( "click", function() {
	$('#loginModal').modal('hide');  
});

$("#register").on( "click", function() {
  $('#signUpModal').modal('show');  
});

$("#forgotPass").on( "click", function() {
	$('#loginModal').modal('hide');  
});

$("#forgotPass").on( "click", function() {
  $('#forgotPasswordModal').modal('show');  
});

loginStatus = document.getElementById('logged_in').innerHTML; 
response_messages = document.getElementById('responseMsg').innerHTML;
message = document.getElementById('msg').innerHTML;

if (loginStatus == 'false'){
  if (message != '') {
    $('#loginModal').modal('show'); 
  }
} else {
  if (response_messages != 'success') {
    $('#responseModal').modal('show'); 
  }
}





    



