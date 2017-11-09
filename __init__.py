import os
from flask import Flask, render_template, request, url_for, redirect
import stegapy


UPLOAD_FOLDER = 'tests'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/enc', methods=["GET", "POST"])
def try_encode():
    try:

        if request.method == "POST":
                print ('Try to encode!')
                message = request.form['message']

                image = request.files['image']
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'imgtoencode.jpg'))
                print(' - Imagen guardada /tests')

                img_out = stegapy.encode(message, image)
                img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'finaldecoded.png'))

                print(' - Imagen codificada lista.')
                return render_template("main.html", message_en=message)

    except Exception as e:
        return render_template("main.html", error=e)


@app.route('/dec', methods=["GET", "POST"])
def try_decode():
    try:

        if request.method == "POST":
                print ('Try to decode!')
                image = request.files['image_up']
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'imgtodecode.jpg'))
                print(' - Imagen guardada /tests')

                message = stegapy.decode(image)

                return render_template("main.html", message_de=message)

    except Exception as e:
        return render_template("main.html", error=e)


if __name__ == "__main__":
    app.run()
