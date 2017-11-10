import os
from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import stegapy
from PIL import Image
import re
import cStringIO

# Ubicacion carpeta de descargas llamada 'tests'
UPLOAD_FOLDER = 'tests'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
# Configuracion de carpeta de upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuracion secret key para mantener session
app.config['SECRET_KEY'] = SECRET_KEY = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'


# checkea si una extension es validad
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#                     #
#     Version WEB     #
#                     #

#
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
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'to_encode.jpg'))
                    print(' - Imagen guardada /tests')

                    img_out = stegapy.encode(message, image)
                    img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'finished_coded.png'))

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
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.png'))
                    print(' - Imagen guardada /tests')

                    message = stegapy.decode(image)
                    session['message_de'] = message
                    session['flag'] = True

                    return redirect(url_for('homepage'))

                else:
                    return render_template("main.html", error='Este tipo de archivo no es valido')

    except Exception as e:
        return render_template("main.html", error=e)


#                       #
#     Version Movil     #
#                       #

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


# Codifica la imagen!
@app.route('/encode_image', methods=["POST"])
def encode_image():
    try:

        if request.method == "POST":
            print('1. Inicia codificacion')

            # Guarda el objeto JSON enviado.
            data = request.get_json()

            message = data.get('message')
            img64 = data.get('img64')

            # borra metadata de data:image/jpeg..
            image_data = re.sub('^data:image/.+;base64,', '', img64).decode('base64')
            # abre la imagen a partir de la decodificacion anterior
            image = Image.open(cStringIO.StringIO(image_data))
            # guarda la imagen
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'to_encode.jpg'))
            print(' - Imagen guardada /tests')

            img_out = stegapy.encode(message, image)
            img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'finished_coded.png'))

            with open("tests/finished_coded.png", "rb") as f:
                data = f.read()
                base64str = data.encode("base64")
                print("Imagen codificada con exito. Envio imagen")

            send_json = {
                'flag': 'Llego base64str',
                'base64str': base64str
            }

            return jsonify(send_json)

    except Exception as e:
        print(e)
        return jsonify('Error')


# Decodifica la imagen!
@app.route('/decode_image', methods=["POST"])
def decode_image():
    try:
        if request.method == "POST":
            print('2. Inicia decodificacion')

            # Guarda el objeto JSON enviado.
            data = request.get_json()
            img64 = data.get('img64')

            # borra metadata de data:image/png..
            image_data = re.sub('^data:image/.+;base64,', '', img64).decode('base64')
            # abre la imagen a partir de la decodificacion anterior
            image = Image.open(cStringIO.StringIO(image_data))
            # guarda la imagen
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'temp.png'))
            print(' - Imagen guardada /tests')

            message = stegapy.decode(image)
            print(message)

            send_json = {
                'flag': 'Llego mensaje desencriptado',
                'message': message
            }

            return jsonify(send_json)

    except Exception as e:
        print(e)
        return jsonify('Error')


# Run main
if __name__ == "__main__":
    app.run()
