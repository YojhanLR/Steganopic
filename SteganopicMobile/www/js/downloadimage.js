var folderName = 'Steganopic';
var fileName;




function downloadFile(URL) {
    //step to request a file system 
    console.log("Comienza a descargar la imagen...")
    window.requestFileSystem(LocalFileSystem.PERSISTENT, 0, fileSystemSuccess, fileSystemFail);

    function fileSystemSuccess(fileSystem) {
        var download_link = encodeURI(URL);
        fileName = download_link.substr(download_link.lastIndexOf('/') + 1); //Get filename of URL
        var directoryEntry = fileSystem.root; // to get root path of directory
        directoryEntry.getDirectory(folderName, {
            create: true,
            exclusive: false
        }, onDirectorySuccess, onDirectoryFail); // creating folder in sdcard


       /* var rootdir = fileSystem.root;
        var fp = fileSystem.root.toNativeURL(); // Returns Fullpath of local directory*/

        //fp = fp + "/" + folderName + "/" + fileName; // fullpath and name of the file which we want to give
        var fp = "/sdcard/Download/" + fileName; // fullpath and name of the file which we want to give
        console.log("File path: "+fp)
        // download function call
        filetransfer(download_link, fp);
    }

    function onDirectorySuccess(parent) {
        // Directory created successfuly
    }

    function onDirectoryFail(error) {
        //Error while creating directory
        alert("No se ha podido crear directorio: " + error.code);

    }

    function fileSystemFail(evt) {
        //Unable to access file system
        alert(evt.target.error.code);
    }
}

function filetransfer(download_link, fp) {
    var fileTransfer = new FileTransfer();
    // File download function with URL and local path
    fileTransfer.download(download_link, fp,
        function(entry) {
            alert("Descarga completa: " + entry.fullPath);
        },
        function(error) {
            //Download abort errors or download failed errors
            alert("Error al obtener la imagen: " + error.source);
        }
    );
}