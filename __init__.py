import os
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import stegapy


UPLOAD_FOLDER = 'tests'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def homepage():
    return render_template("main.html")


@app.route('/', methods=["GET", "POST"])
def try_encode():
    try:

        if request.method == "POST":
            print ('Try_encode!')
            message = request.form['message']
            image = request.files['image']

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'prueba.jpg'))
            print(' - Imagen guardada /tests')

            img_out = stegapy.encode(message, image)
            img_out.save(os.path.join(app.config['UPLOAD_FOLDER'], 'final.png'))

            print(' - Imagen codificada lista.')

        return render_template("main.html", error=message)

    except Exception as e:
        return render_template("main.html", error=e)


if __name__ == "__main__":
    app.run()
