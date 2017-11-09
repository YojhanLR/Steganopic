$("#btn_encode").on("click",function(){

	//console.log('RESULT', readerResult.result)
	var data = {
		message: $("#ipt_message").val(),
		img64: readerResult.result
	};

	console.log(JSON.stringify(data));

	$.ajax({
		type: 'POST',
		url: 'http://127.0.0.1:5000/encode_image',
		data: JSON.stringify(data),
		dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
		success: function(result){
			console.log(result)
		}
	});
});


var readerResult;
function encodeImageFileAsURL(element) {
  var file = element.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    console.log('encodeImage')
    readerResult = reader;
  }
  reader.readAsDataURL(file);
}

