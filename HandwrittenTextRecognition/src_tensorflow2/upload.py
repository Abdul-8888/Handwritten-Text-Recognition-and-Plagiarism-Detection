import os
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory

from main import infer_by_web
import traceback

import sys

sys.path.insert(1, '../../../HTRandPD')
from  PlagiarismDetection.detector import checkPlagiarism


__author__ = 'Susan'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # project abs path


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_page", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/plagiarism-detection")
def upload_plagiarism_page():
    return render_template("plagiarism.html")


@app.route("/detect-plagiarism", methods=["POST"])
def detectPlagiarism():
    print("Plagiarism Detection called")
    files = request.files.getlist("file")
    saveTextInFile(files)
    res = detect_Plagiarism()
    return res


@app.route("/upload", methods=["POST"])
def upload():
    # folder_name = request.form['uploads']
    target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    option = request.form.get('optionsPrediction')
    print("Selected Option:: {}".format(option))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        savefname = datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + "."+ext
        destination = "/".join([target, savefname])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        result = predict_image(destination, option)
        print("Prediction: ", result)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=savefname, result=result)


def predict_image(path, type):
    print(path)
    return infer_by_web(path, type)


def saveTextInFile(uploadedFiles):
    folderName = "uploaded_files"
    filePath = os.path.join(f"../../PlagiarismDetection/{folderName}")

    # Remove existing files in the folder, if any
    for filename in os.listdir(filePath):
        file_path = os.path.join(filePath, filename)
        os.remove(file_path)
    
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    # Save each file with its original filename
    for file in uploadedFiles:
        if file.filename != '':  # Check if a file is selected
            filename = file.filename
            file.save(os.path.join(filePath, filename))  # Save in the new folder


def detect_Plagiarism():
    try:
        # response = subprocess.run(['python', '../../PlagiarismDetection/detector.py', 'checkPlagiarism'], check=True)
        response = checkPlagiarism()

        # Validate the response (replace with your specific validation logic)
        # if not isinstance(response, str):
        #     raise TypeError("checkPlagiarism() must return a string")

    except (SyntaxError, TypeError, ValueError) as e:  # Catch specific errors
        print(f"Error calling plagiarism detector: {e}")
        traceback.print_exc()  # Print detailed traceback for debugging
        response = "Error: Plagiarism detection failed"
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        response = "Error: An unexpected error occurred"

    return response


if __name__ == "__main__":
    app.run(port=4555, debug=True)