from os import name
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from src.CLI import cli_command
from src.Exec import Exec
from src.Functions import Functions as fn
from src.BinaryFileManager import BinaryFileManager as bfm
from src.UtilClass import *
import datetime
import struct
from src.Blocks import *
from src.CLI import cli_command
from src.Primitive import Path

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "{output: 'Hello World'}"

@app.route('/execute', methods=['POST'])
def execute():
    if request.method == 'POST':
        data = request.get_json()
        content = data.get('content')
        if content != "":
            output = cli_command(content)
            return jsonify({"output": output})
        else:
            return jsonify({"output": ["No se ha ingresado un comando"]})
    else:
        return jsonify({"output": ["No se ha ingresado un comando"]})

@app.route('/reports', methods=['GET'])
def getreports():
    image_folder = 'static/images'
    image_urls = []
    import os
    list_images = os.listdir(image_folder)
    # filter images for type
    list_images = [img for img in list_images if img.endswith(".svg")]

    for filename in list_images:
        name = filename.split(".")[0]
        image_url = url_for('static', filename='images/'+filename, _external=True)
        image_urls.append({"url": image_url, "name": name})
    return jsonify(image_urls)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
    # input = Exec(Path(path='/home/pedro/Documents/Cursos/Archivos/lab/p1/avanzado.adsj', filename="")).read_file()
    # output = cli_command("execute -path=/home/pedro/Documents/Cursos/Archivos/lab/p1/basico.adsj")
    # output = cli_command(input)
    # for value in output:
    #     print(value)

#     while True:
#         command = input(">> ")
#         if command == "exit":
#             break
#         content = cli_command(command)
#         if content != "":
#            cli_command(content)