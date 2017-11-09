$("#btn_encode").on("click",function(){
	console.log('im here');

	var sendInfo = {
		message: $("#ipt_message").val(),
		name: $("#ipt_name").val()
	};

	console.log(JSON.stringify(sendInfo));

	$.ajax({
		type: 'POST',
		url: 'http://127.0.0.1:5000/showMessage',
		data: sendInfo,
		dataType: 'json',
		success: function(result){
			console.log("Exito!!")
		}
	});
});


