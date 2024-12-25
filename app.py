import os
import random
from flask import Flask, send_from_directory, render_template, request
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/corrupt', methods=['POST'])
def corrupt_file():
    file_format = request.form['file_format']

    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"corrupted_file.{file_format}")

    with open(file_path, "w") as file:
        file.write(f"This is a test {file_format.upper()} file.\n")
        file.write(
            f"Technology has become an integral part of our daily lives. It enhances communication, simplifies tasks, and boosts productivity.")

    with open(file_path, "r+b") as file:
        data = file.read()
        file.seek(5)
        file.write(bytearray(random.getrandbits(8) for _ in range(len(data))))

    return send_from_directory(temp_dir, f"corrupted_file.{file_format}", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
