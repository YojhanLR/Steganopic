$("#btn_encode").on("click",function(){

	//console.log('RESULT', readerResult.result)
	console.log('1. Voy a enviar texto e imagen para encriptar!')
	var data = {
		message: $("#ipt_message").val(),
		img64: readerResult.result
	};

	console.log(data);

	$.ajax({
		type: 'POST',
		url: 'http://127.0.0.1:5000/encode_image',
		data: JSON.stringify(data),
		dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
		success: function(result){
			console.log(result)

			var src = "data:image/png;base64,";
			src += result.base64str;

			var newImage = document.createElement('img');
			newImage.src = src;
			newImage.width = newImage.height = "180";
			document.querySelector('#imgContainer').innerHTML = newImage.outerHTML;//where to insert your image
			document.getElementById("imgContainer").style.display = "block";
			document.getElementById('imgMessage').style.display = "block";
		}
	});
});

$("#btn_decode").on("click",function(){

	//console.log('RESULT', readerResult.result)
	console.log('2. Voy imagen para desencriptar!')

	var data = {
		img64: readerResult.result
	};

	console.log(data);

	$.ajax({
		type: 'POST',
		url: 'http://127.0.0.1:5000/decode_image',
		data: JSON.stringify(data),
		dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
		success: function(result){
			console.log(result)

			/*var src = "data:image/png;base64,";
			src += result.base64str;

			var newImage = document.createElement('img');
			newImage.src = src;
			newImage.width = newImage.height = "180";
			document.querySelector('#imgContainer').innerHTML = newImage.outerHTML;//where to insert your image
			document.getElementById("imgContainer").style.display = "block";
			document.getElementById('imgMessage').style.display = "block";*/
		}
	});
});


var readerResult;
function encodeImageFileAsURL(element) {
  var file = element.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    console.log('Image in base64')
    readerResult = reader;
  }
  reader.readAsDataURL(file);
}

