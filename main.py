from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'avatar' not in request.files:
        return "No file part"
    file = request.files['avatar']
    if file.filename == '':
        return "No selected file"
    if file and file.filename.lower().endswith(('png', 'jpeg', 'jpg')):
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('gallery'))
    return "Invalid file type"

@app.route('/gallery')
def gallery():
    # Lister tous les fichiers dans le dossier d'uploads
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [f for f in file_list if f.lower().endswith(('png', 'jpeg', 'jpg'))]
    return render_template('gallery.html', images=images)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return redirect(url_for('gallery'))
        else:
            return f"File {filename} not found."
    except Exception as e:
        return f"An error occurred while deleting the file: {str(e)}"

@app.route('/delete_all', methods=['POST'])
def delete_all():
    try:
        file_list = os.listdir(app.config['UPLOAD_FOLDER'])
        images = [f for f in file_list if f.lower().endswith(('png', 'jpeg', 'jpg'))]
        for image in images:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], image)
            os.remove(filepath)
        return redirect(url_for('gallery'))
    except Exception as e:
        return f"An error occurred while deleting all files: {str(e)}"

@app.route('/rename/<filename>', methods=['POST'])
def rename_file(filename):
    new_name = request.form['new_name']
    if new_name:
        # Sécuriser le nom et garder l'extension de l'image
        from werkzeug.utils import secure_filename
        name, ext = os.path.splitext(filename)  # Sépare le nom de l'extension
        new_filename = secure_filename(new_name) + ext  # Ajouter l'extension d'origine

        old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        try:
            # Vérifier si le nouveau nom existe déjà
            if os.path.exists(new_filepath):
                return f"Error: A file with the name '{new_filename}' already exists."

            # Renommer le fichier
            os.rename(old_filepath, new_filepath)
            return redirect(url_for('gallery'))
        except Exception as e:
            return f"An error occurred while renaming the file: {str(e)}"

    return "Invalid file name"

if __name__ == '__main__':
    app.run(debug=True)
