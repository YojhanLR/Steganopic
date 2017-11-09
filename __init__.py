import os
from flask import Flask, render_template, request, session,url_for, redirect, jsonify
import stegapy
from PIL import Image
from PIL import PngImagePlugin
import urllib
import re
import cStringIO


UPLOAD_FOLDER = 'tests'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
# Configuracion de carpeta de upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuracion secret key para mantener session
app.config['SECRET_KEY'] = SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


# check if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def homepage():
    try:
        if session['flag']:
            print('Hay valor.')
            session.pop('flag', None)
            return render_template("main.html")

    except Exception as e:
        print ('No encontro variable')
        session.clear()
        return render_template("main.html")


@app.route('/', methods=["GET", "POST"])
def try_encode():
    try:

        if request.method == "POST":

                print ('Try to encode!')
                message = request.form['message']
                image = request.files['image']

                if allowed_file(image.filename):
                    print('archivo valido')
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'toencode.jpg'))
                    print(' - Imagen guardada /tests')

                    img_out = stegapy.encode(message, image)
                    img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'decoded.png'))

                    print(' - Imagen codificada lista.')

                    session['message_en'] = message
                    session['flag'] = True

                    return redirect(url_for('homepage'))

                else:
                    return render_template("main.html", error='Este tipo de archivo no es valido')

    except Exception as e:
        return render_template("main.html", error=e)


@app.route('/dec', methods=["GET", "POST"])
def try_decode():
    try:

        if request.method == "POST":
                print ('Try to decode!')
                image = request.files['image_up']

                if allowed_file(image.filename):
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg'))
                    print(' - Imagen guardada /tests')

                    message = stegapy.decode(image)
                    session['message_de'] = message
                    session['flag'] = True

                    return redirect(url_for('homepage'))

                else:
                    return render_template("main.html", error='Este tipo de archivo no es valido')

    except Exception as e:
        return render_template("main.html", error=e)


# Envia informacion basica en ajax, para tomar como ejemplo
@app.route('/simple_ajax', methods=["POST"])
def simple_ajax():

    # Guarda el objeto JSON enviado.
    data = request.get_json()

    name = data.get('name')
    message = data.get('message')
    idnumber = 2

    print ('Nombre: %s' % name)
    print ('Mensaje: %s' % message)

    send_json = {
        'name': 'Este es mi nombre: %s ' % name,
        'message': 'Este es mi mensaje: %s ' % message,
        'id': idnumber
    }

    return jsonify(send_json)


# Envia informacion basica en ajax, para tomar como ejemplo
@app.route('/encode_image', methods=["POST"])
def encode_image():
    try:

        if request.method == "POST":

            # Guarda el objeto JSON enviado.
            data = request.get_json()

            message = data.get('message')
            img64 = data.get('img64')

            # borra metadata de data:image/jpeg..
            image_data = re.sub('^data:image/.+;base64,', '', img64).decode('base64')
            # abre la imagen a partir de la decodificacion anterior
            image = Image.open(cStringIO.StringIO(image_data))
            # guarda la imagen
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'toencode.jpg'))
            print(' - Imagen guardada /tests')

            img_out = stegapy.encode(message, image)
            img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'decoded.png'))

            return jsonify('Imagen codificada con exito')

    except Exception as e:
        print(e)
        return jsonify('Error')


# Run main
if __name__ == "__main__":
    app.run()
