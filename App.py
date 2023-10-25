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


app = Flask(__name__)

CORS(app)

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
   app.run(debug=True)
    # output = cli_command("execute -path=/home/pedro/Documents/Cursos/Archivos/lab/p1/src.adsj")
    # cli_command(output)
#     while True:
#         command = input(">> ")
#         if command == "exit":
#             break
#         content = cli_command(command)
#         if content != "":
#            cli_command(content)
    # size = 1024*1024*1
    # print(struct.calcsize(SuperBlock().FORMATSUPERBLOCK))
    # value_n = fn().calculate_value_of_n(size, SuperBlock(), Inode(), Content())
    # new_super_block = SuperBlock()
    # print(new_super_block.serialize_super_block())
    # print(value_n)
    # print(new_super_block.deserialize_super_block(new_super_block.serialize_super_block()))
    # print("size super block: ", struct.calcsize(new_super_block.FORMATSUPERBLOCK))
    # print("size inode: ", struct.calcsize(Inode().FORMARTINODETABLE))
    # print("size content: ", struct.calcsize(Content().FORMARTCONTENT)*4)
    # print("size total: ", 68+value_n+3*value_n+value_n*96+3*value_n*64)
    # print("size super Block: ", struct.calcsize(SuperBlock().FORMATSUPERBLOCK))
    # print("size inode: ", struct.calcsize(Inode().FORMARTINODETABLE))
    # print("size content: ", struct.calcsize(Content().FORMARTCONTENT)*4)
    # print("size ebr: ", struct.calcsize(EBR().FORMATEBR))
    # dato_block_data = "hola mundo desde no se donde"
    # block_data = BlockFile()
    # data = block_data.serialize_block_file(dato_block_data)
    # print(data)
    # print(block_data.deserialize_block_file(data))
    # data_block_folder = BlockFolder()
    # data_block_f = data_block_folder.serialize_block_folder()
    # print(data_block_f)
    # print(data_block_folder.deserialize_block_folder(data_block_f))    
    # newinode =  Inode()
    # print(newinode.serialize_inode())
    # print(newinode.deserialize_inode(newinode.serialize_inode()))
    # new_block_pointer = BlockPointer()
    # data_block_pointer = new_block_pointer.serialize_block_pointer()
    # print(data_block_pointer)
    # current_b_p = new_block_pointer.deserialize_block_pointer(data_block_pointer)
    # if current_b_p is not None:
    
    #     print(current_b_p.block_pointer)
    # print(fn().get_permission(640))