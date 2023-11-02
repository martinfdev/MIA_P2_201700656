
class Mkgrp:
    def __init__(self, name, arr_output_result):
        self.name = name
        self.arr_output_result = arr_output_result

    def execute(self):
        if self.name == "":
            self.arr_output_result.append("No se ha ingresado un nombre para el grupo")
            return
        
    