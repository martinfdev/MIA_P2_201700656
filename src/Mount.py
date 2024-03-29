from src.Functions import Functions as fn
from src.Primitive import Path, ID
from src.UtilClass import *
from src.BinaryFileManager import BinaryFileManager as bfm
class Mount:
    def __init__(self, list_params, arr_output_result) -> None:
        self.arr_output_result = arr_output_result
        self._list_params = list_params
        self._path = ""
        self._file_name = ""
        self._name = ""
        self.id = ""
        self._tmp_partition = None
        self.tmp_mbr = MBR([])
        self._tmp_list_mounts_partitions = []

    def execute_mount(self, list_mounts_partitions):
        self._tmp_list_mounts_partitions = list_mounts_partitions
        if not self._set_val_properties_mount(self._list_params):
            # fn().err_msg("Mount", "No se pudo montar la partición "+str(self._name))
            self.arr_output_result.append("No se pudo montar la partición "+str(self._name))
            return
        if not self._generateid():
            # fn().err_msg("Mount", "No se pudo montar la partición "+str(self._name))
            self.arr_output_result.append("No se pudo montar la partición "+str(self._name))
            return
        # fn().success_msg("Mount", "Se montó la partición "+str(self._name)+" con el id "+str(self.id))
        self.arr_output_result.append("Se montó la partición "+str(self._name)+" con el id "+str(self.id))
        return self

    #set and check properties for mount
    def _set_val_properties_mount(self, list_params):
        for param in list_params:
            if isinstance(param, Path):
                self._path = param.get_value()
                self._file_name = param.filename
            elif isinstance(param, ID):
                self._name = param.get_value()
        
        if self._path == "":
            # fn().err_msg("Mount", "No se encontró el parámetro -path")
            self.arr_output_result.append("No se encontró el parámetro -path")
            return False
        if self._name == "":
            # fn().err_msg("Mount", "No se encontró el parámetro -name")
            self.arr_output_result.append("No se encontró el parámetro -name")
            return False
        return True

    #generate id for mount
    def _generateid(self):
        tmp_mbr = MBR(self.arr_output_result)
        if not fn(self.arr_output_result).check_status_file(self._path):
            # fn().err_msg("Mount", "No se encontró el archivo "+self._path)
            self.arr_output_result.append("No se encontró el archivo "+self._path)
            return False
        tmp_mbr = tmp_mbr.deserialize_mbr(bfm(self._path, self.arr_output_result).read_binary_data(0, struct.calcsize(tmp_mbr.FORMATMBR)+struct.calcsize(tmp_mbr.mbr_partition_1.FORMATPARTITION)*4))
        if tmp_mbr is None:
            return False
        num_partitions = 0
        list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2, tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]
        found_partition = False
        for partition in list_partitions:
            num_partitions += 1
            if partition.part_type == "E":
                if self._find_logic_partition(partition):
                    return True
            if partition.part_name == self._name:
                self._tmp_partition = partition
                found_partition = True
                break
        if not found_partition:
            # fn().err_msg("Mount", "No se encontró la partición "+str(self._name))
            self.arr_output_result.append("No se encontró la partición "+str(self._name))
            return False    
        self.tmp_mbr = tmp_mbr
        self.id = "56"+str(num_partitions)+self._file_name.removesuffix(".dsk")
        for mount in self._tmp_list_mounts_partitions:
            if mount.id == self.id:
                # fn().err_msg("Mount", "La partición "+str(self._name)+" ya está montada")
                self.arr_output_result.append(f"La partición {self._name} con id {self.id} ya está montada")
                return False
        return True
    
    def _find_logic_partition(self, partition):
        tmp_ebr = EBR(self.arr_output_result)
        num_partitions = 3
        if partition.part_type == "E":
            tmp_ebr = tmp_ebr.deserialize_ebr(bfm(self._path, self.arr_output_result).read_binary_data(partition.part_start, struct.calcsize(tmp_ebr.FORMATEBR)))
            if tmp_ebr is None:
                return False
            num_partitions += 1
            if tmp_ebr.ebr_name == self._name:
                self._tmp_partition = tmp_ebr
                self.id = "56"+str(num_partitions)+self._file_name.removesuffix(".dsk")
                return True
            
            while tmp_ebr.ebr_next != -1:
                num_partitions += 1
                tmp_ebr = tmp_ebr.deserialize_ebr(bfm(self._path, self.arr_output_result).read_binary_data(tmp_ebr.ebr_next, struct.calcsize(tmp_ebr.FORMATEBR)))
                if tmp_ebr is None:
                    return False
                if tmp_ebr.ebr_name == self._name:
                    self._tmp_partition = tmp_ebr
                    self.id = "56"+str(num_partitions)+self._file_name.removesuffix(".dsk")
                    return True
        return False
    
    def get_partition(self):
        return self._tmp_partition
    
    def get_mbr(self):
        return self.tmp_mbr
    
    def get_path(self):
        return self._path