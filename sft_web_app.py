from flask import Flask, render_template_string, request, send_file, redirect, url_for, flash
import os
import webbrowser

# Flask App Setup
app = Flask(__name__)
app.secret_key = "secure_file_transfer"

# Directory for storing uploaded files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML Template (Dark Digital Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Secure File Transfer</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            height: 100vh;
        }
        header {
            background: #161b22;
            width: 100%;
            padding: 20px;
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            color: #58a6ff;
            letter-spacing: 2px;
            box-shadow: 0px 0px 10px #58a6ff;
        }
        .container {
            margin-top: 40px;
            background: #161b22;
            padding: 20px;
            border-radius: 10px;
            width: 50%;
            text-align: center;
            box-shadow: 0px 0px 20px #58a6ff;
        }
        input[type=file] {
            margin: 20px;
            color: white;
        }
        .btn {
            background: #238636;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }
        .btn:hover {
            background: #2ea043;
        }
        .file-list {
            margin-top: 20px;
            text-align: left;
        }
        .file-item {
            background: #0d1117;
            padding: 8px;
            border-radius: 5px;
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .download-link {
            text-decoration: none;
            color: #58a6ff;
            font-weight: bold;
        }
        .flash {
            margin: 10px;
            padding: 10px;
            background: #238636;
            color: white;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <header>🔒 Secure File Transfer</header>
    <div class="container">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for msg in messages %}
                    <div class="flash">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <h2>Upload a File</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <button class="btn" type="submit">Upload</button>
        </form>
        <h2>Available Files</h2>
        <div class="file-list">
            {% for file in files %}
                <div class="file-item">
                    {{ file }}
                    <a class="download-link" href="{{ url_for('download_file', filename=file) }}">Download</a>
                </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# Home Route (Upload + List Files)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)
            flash(f"File '{uploaded_file.filename}' uploaded successfully!")
            return redirect(url_for("home"))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files)

# Download Route
@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

# Run App & Auto Open Browser
if __name__ == "__main__":
    url = "http://127.0.0.1:5000"
    print(f"Server running on {url}")
    webbrowser.open(url)
    app.run()
