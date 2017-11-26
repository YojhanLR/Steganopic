//urlCall = 'http://10.0.2.2:5000';
//urlCall =  'http://127.0.0.1:5000';

//Genymotion
urlCall =  'http://10.0.3.2:5000';



$("#btn_encode").on("click",function(){

	//console.log('RESULT', readerResult.result)
	console.log('1. Voy a enviar texto e imagen para encriptar!')
	var data = {
		message: $("#ipt_message").val(),
		img64: readerResult.result
	};

	console.log(data);
	AjaxCallEncode(urlCall, data);
});

$("#btn_decode").on("click",function(){

	console.log('RESULT', readerResult.result)
	console.log('2. Voy imagen para desencriptar!')

	var data = {
		img64: readerResult.result
	};

	console.log(data);
	AjaxCallDecode(urlCall, data);
	
});



var readerResult = new FileReader();
function encodeImageFileAsURL(element) {
  
  var file = element.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    console.log('Image in base64');
    //console.log(reader);
    readerResult = reader;
  }
  reader.readAsDataURL(file);
  //console.log("aqui")
}


function AjaxCallEncode (urlCall, data){
	$.ajax({
		type: 'POST',
		url: urlCall+'/encode_image',
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
			//document.querySelector('#imgContainer').innerHTML = newImage.outerHTML;//where to insert your image
			document.getElementById("linkDownload").appendChild(newImage)
			document.getElementById("imgContainer").style.display = "block";
			document.getElementById('imgMessage').style.display = "block";
			document.getElementById("linkDownload").href=urlCall+'/static/tests/final.png'; 
			
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			console.log("Error en la URL, intentando alternativa...");
			urlCall = 'http://127.0.0.1:5000';
            AjaxCallEncode(urlCall, data);
                }  
	});
}

function AjaxCallDecode (urlCall, data){
	$.ajax({
		type: 'POST',
		url: urlCall+'/decode_image',
		data: JSON.stringify(data),
		dataType: 'json',
        contentType: 'application/json;charset=UTF-8',
		success: function(result){
			console.log(result)
			document.getElementById("imgMessagedec").style.display = "block";
			document.getElementById("imgMessagedec").innerHTML = "El mensaje codificado es: "+result.message;
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
			console.log("Error en la URL, intentando alternativa...");
			urlCall = 'http://127.0.0.1:5000';
            AjaxCallDecode(urlCall, data);
                }  
	});
}

function descargar(){
	console.log("Vamos a descargar")
	downloadFile(urlCall+'/static/tests/final.png')
}







