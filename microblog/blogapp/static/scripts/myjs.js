$(document).ready(function(){
	// add all event handlers here
	console.log("Adding event handlers");
	$("#username").on("change", check_username);
	console.log("function registered");
});

function check_username(){
	// get the source element
	console.log("check_username called");
	var chosen_user = $(this).find("input");
	console.log("User chose: " + chosen_user.val());
	
	$("#checkuser").removeClass();
	$("#checkuser").html('<img src="static/style/loading.gif")>');
	
	// ajax code 
	$.post('/checkuser', {
		'username': chosen_user.val() //field value being sent to the server
	}).done(function (response){
		var server_response = response['text']
		var server_code = response['returnvalue']
		if (server_code == 0){ // success: Username does not exist in the database
			$("#password").focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("success");
		}else{ // failure: Username already exists in the database
			chosen_user.val("");
			chosen_user.focus();
			$("#checkuser").html('<span>' + server_response + '</span>');
			$("#checkuser").addClass("failure");
		}
	}).fail(function() {
		$("#checkuser").html('<span>Error contacting server</span>');
		$("#checkuser").addClass("failure");
	});
	// end of ajax code
	
	console.log("finished check_username");
}