from src.Functions import Functions as fn
from src.BinaryFileManager import BinaryFileManager as bfm
from src.UtilClass import *
from src.Primitive import *
import struct
from graphviz import Digraph


class REP:
    def __init__(self, list_params) -> None:
        self.params = list_params
        self.name = ""
        self.output_path = ""
        self.id = ""
        self.path_file_ls = ""
        self._tmp_partition = None

    def execute_rep(self, list_mounts):
        if not self._set_params():
            return
        if not self._find_partition(list_mounts):
            fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            return
        if self.name == "mbr":
            self._mbr()
        
            
    def _set_params(self):
        for param in self.params:
            if isinstance(param, Path):
                self.path = param.get_value()
            elif isinstance(param, ID):
                self.id = param.get_value()
            elif param['name']:
                self.name = param['name'].get_value()
            elif param['ruta']:
                self.path_file_ls = param['ruta'].get_value()

        if self.id == "":
            fn().err_msg("REP", "No se especificó el parámetro obligatorio ID")
            return False
        if self.name == "":
            fn().err_msg("REP", "No se especificó el parámetro obligatorio NAME")
            return False
        if self.path == "":
            fn().err_msg("REP", "No se especificó el parámetro obligatorio PATH")
            return False            
        return True


       
    def _mbr(self):
        if self._tmp_partition is None:
            fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            return False
        tmp_path = self._tmp_partition.get_path()
        tmp_mbr = MBR()
        total_bytes_to_read = struct.calcsize(
        tmp_mbr.FORMATMBR) + struct.calcsize(tmp_mbr.mbr_partition_1.FORMATPARTITION) * 4
        binary_data_mbr = bfm(tmp_path).read_binary_data(
             0, total_bytes_to_read)
        if binary_data_mbr is None:
             fn().err_msg("REP", "No se pudo leer el MBR")
             return
        tmp_mbr.deserialize_mbr(binary_data_mbr)
        list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2, tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]
        print(list_partitions)
        
        
        
        
        # # for partition in list_partitions:
        # #     if partition.part_name != "\0":
        # #         print("=============REP MBR=============")
        # #         print("Nombre: "+partition.part_name)
        # #         print("Status: "+partition.part_status)
        # #         print("Type: "+partition.part_type)
        # #         print("Fit: "+partition.part_fit)
        # #         print("Start: "+str(partition.part_start))
        # #         print("Size: "+str(partition.part_size))

        # size_disk = tmp_mbr.mbr_tamano
        # free_space = 0

        # list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2,
        #                    tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]
        # for partition in list_partitions:
        #     if partition.part_type != "\0":
        #         free_space += partition.part_size
        # free_space = size_disk - free_space
        # text_td = ""
        # for partition in list_partitions:
        #     if partition.part_status != "\0":
        #         text_td += f'''
        #            <TD BGCOLOR="yellow" WIDTH="5">{partition.part_name}<BR/>Tamaño: {partition.part_size}</TD>
        #           '''
        # if free_space > 0:
        #     text_td += f'''
        #            <TD BGCOLOR="gray" WIDTH="5">Libre<BR/>{free_space}</TD>
        #           '''

        # graph = Digraph(format='svg', node_attr={"rankdir": "LR"})
        # graph.node("table", label=f'''<<TABLE>
        #           <TR>
        #            <TD BGCOLOR="green" WIDTH="5">MBR</TD>
        #             {text_td}
        #           </TR>
        #           </TABLE>>''', shape="none")
        # #render graph
        # graph.render('disck',  view=True)

    def _find_partition(self, listMounts):
        for mount in listMounts:
            if mount.id == self.id:
                self._tmp_partition = mount
                return True
        return False