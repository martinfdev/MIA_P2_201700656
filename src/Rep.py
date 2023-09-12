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


    def execute_rep(self):
        pass
        
    def _set_params(self):
        for param in self.params:
            if isinstance(param, Path):
                self.path = param
            elif isinstance(param, ID):
                self.id = param
       
       
       
       
       
       
       
        # tmp_path = ""
        # if type(self.path) is Path:
        #     tmp_path = self.path.get_value()
        # else:
        #     fn().err_msg("REP", "No se especificó el parámetro obligatorio PATH")
        #     return

        # tmp_mbr = MBR()
        # total_bytes_to_read = struct.calcsize(
        #     tmp_mbr.FORMATMBR) + struct.calcsize(tmp_mbr.mbr_partition_1.FORMATPARTITION) * 4
        # binary_data_mbr = bfm(tmp_path).read_binary_data(
        #     0, total_bytes_to_read)
        # if binary_data_mbr is None:
        #     fn().err_msg("REP", "No se pudo leer el MBR")
        #     return
        # tmp_mbr.deserialize_mbr(binary_data_mbr)
        # # list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2, tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]
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
