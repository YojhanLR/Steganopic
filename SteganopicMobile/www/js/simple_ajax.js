$("#btn_encode").on("click",function(){

	var data = {
		message: $("#ipt_message").val(),
		name: $("#ipt_name").val()
	};

	console.log(JSON.stringify(data));

	$.ajax({
		type: 'POST',
		url: 'http://127.0.0.1:5000/simple_ajax',
		data: JSON.stringify(data),
		dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
		success: function(result){
			console.log(result)
		}
	});
});

