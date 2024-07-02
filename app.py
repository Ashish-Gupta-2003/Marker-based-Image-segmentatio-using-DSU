from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os,cv2,zipfile
from marker_based_img_seg_using_dsu import segment_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template('mark.html', filename=filename)
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    filename = data['filename']
    markers = data['markers']


    print("Received markers:", markers)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    coordinates = [(int(marker['scaledY']), int(marker['scaledX'])) for marker in markers]
    print("Coordinates: ", coordinates)
    # Apply segmentation using the markers
    segmented_image_path= segment_image(filepath, coordinates=coordinates)

    return jsonify({
        'segmented_image_path': os.path.basename(segmented_image_path)
    })

@app.route('/result/<segmented_image_path>')
def show_result(segmented_image_path):
    return render_template('result.html', segmented_image_path=segmented_image_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download_zip/<filename>')
def download_zip(filename):
    zip_filename = filename.rsplit('.', 1)[0] + '.zip'
    zip_filepath = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_filepath, 'w') as zipf:
        zipf.write(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], zip_filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
