import os
from re import T
from flask import Flask, request, send_file, url_for, render_template,send_from_directory,redirect
from werkzeug.utils import secure_filename
from mdtable import MDTable

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] ='./uploads'
app.config['DOWNLOAD_FOLDER'] ='./converted/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}

# check for allowed file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return 'hello world'

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            secureName = secure_filename(file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secureName)
            file.save(filename)
        
            print(f'filename1 is:{file}')
            print(f'filename2 is:{secureName}')

            markdown = MDTable(filename)
            markdown_string = markdown.get_table()
            saveAs = secureName.split('.')[0]+'.txt'
            print(f'file is saved as: {saveAs}')
            markdown.save_table(os.path.join(app.config['DOWNLOAD_FOLDER'],saveAs ))

            # return 'file uploaded successfully'
            # return redirect(url_for('download_file', name=saveAs))
            return(redirect('/download/'+ saveAs))
    return render_template('upload.html')

# downlaod path


@app.route('/download/<name>')
def download_file(name):
    # return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)
    return  render_template('download.html',value=name)



@app.route('/return-files/<filename>')
def return_files(filename):
    filePath = os.path.join(app.config["DOWNLOAD_FOLDER"] + filename)
    return send_file(filePath,as_attachment=True)


if __name__== '__main__':
    app.run(debug=True)
