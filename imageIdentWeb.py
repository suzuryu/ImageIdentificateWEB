from flask import Flask, request, render_template, send_from_directory
import os


from imageIdenti import resize_img, identifies_img

app = Flask(__name__, template_folder='templates')
app.config.update({'DEBUG': True})

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['png', 'PNG', 'jpg', 'JPEG', 'gif']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def file_is_allowed(filename):
    return filename[filename.find('.') + 1:] in ALLOWED_EXTENSIONS

@app.route ('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    try:
        if request.method == 'POST':
            img_file = request.files['img_file']
            filename = img_file.filename
            print(img_file)
            if img_file and file_is_allowed(filename):
                img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_url = '/uploads/' + filename
                result = identifies_img('./uploads/' + filename)

                return render_template('index.html', img_url=img_url, result=result)
            else:
                return ''' <p> img upload failed </p> '''

    except Exception:
        return render_template("index.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run()
