import os
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import flash, render_template

UPLOAD_FOLDER = '/Users/amir/projects/PycharmProjects/carpsweb'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_resource_as_string(name, charset='utf-8'):
    with app.open_resource(name) as f:
        return f.read().decode(charset)

app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

cities = []

@app.route('/cities', methods=['GET'])
def cities():
    return jsonify(['Amir', 'Ehsan'])

@app.route('/cities', methods=['POST'])
def insert_city():
    requested_data = request.form['name']
    return jsonify(requested_data)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("matched.html", filename=filename)
            # return redirect(url_for('uploaded_file', filename=filename))
    return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# photos = []
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# @app.route('/delete/<string:name>')
# def delete_photo(name):
#     photos.remove(name)
#     return " ".join(f for f in photos)
#
# @app.route('/insert/<string:name>')
# def add_photo(name):
#     photos.append(name)
#     return jsonify({'photos': photos})


if __name__ == '__main__':
    app.run()
