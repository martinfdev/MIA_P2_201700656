from src.Functions import Functions as fns
from src.Primitive import Path
import os
class Rmdisk:
    def __init__(self, obj_path, arr_output_result):
        self.arr_output_result = arr_output_result
        self._folders_dir = ""
        self._file_name ="" 
        self._obj_path = obj_path

    def execute_rmdisk(self):
        fn = fns()
        if isinstance(self._obj_path, Path):
            self._folders_dir = self._obj_path.path
            self._file_name = self._obj_path.filename
        else:
            # fn.err_msg("RMDISK", "No se pudo eliminar el disco")
            self.arr_output_result.append("RMDISK: No se pudo eliminar el disco")
            return
    
        # print("RMDISK", "¿Está seguro que desea eliminar el disco "+fn.YELLOW+self._file_name+fn.YELLOW+"? [Y/N]: ")
        # answer = input()
        answer = "Y"
        if answer == "Y" or answer == "y":
            pass
        else:
            return
        if fn.check_status_file(self._folders_dir+self._file_name):
            try:
                os.remove(self._folders_dir+self._file_name)
                # fn.success_msg("RMDISK", "Disco eliminado: " + fn.YELLOW+self._file_name)
                self.arr_output_result.append("RMDISK: Disco eliminado: " + self._file_name)
            except:
                # fn.err_msg("RMDISK", "No se puede disco "+fn.RED+self._file_name)
                self.arr_output_result.append("RMDISK: No se puede disco "+self._file_name)
        else:
            # fn.err_msg("RMDISK", "No se pudo eliminar el disco "+fn.RED+self._file_name+fn.YELLOW+" no existe")
            self.arr_output_result.append("RMDISK: No se pudo eliminar el disco "+self._file_name+" no existe")