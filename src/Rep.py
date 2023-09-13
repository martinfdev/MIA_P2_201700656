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
        self.output_path_folder = ""
        self.file_name = ""
        self.id = ""
        self.path_file_ls = ""
        self._tmp_partition = None

    def execute_rep(self, list_mounts):
        if not self._set_params():
            return
        if not self._find_partition(list_mounts):
            fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            return
        self._create_directory()
        
        if self.name == "mbr":
            self._mbr()
        
            
    def _set_params(self):
        for param in self.params:
            if isinstance(param, Path):
                self.output_path = param.get_value()
                self.output_path_folder = param.path
                self.file_name = param.filename
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
        if self.output_path == "":
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
        digraph = Digraph(format='svg', node_attr={"rankdir": "LR"})
        digraph.node(f'''REPORTE MBR''', label=f'''<<TABLE>
                    <TR>
                    <TD BGCOLOR="green" WIDTH="5">MBR</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">mbr_tamano: {tmp_mbr.mbr_tamano}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">mbr_fecha_creacion: {tmp_mbr.mbr_time_stamp}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">mbr_disk_signature: {tmp_mbr.mbr_disk_signature}</TD>
                    </TR>
                    </TABLE>>''', shape="none")
        for partition in list_partitions:
            if partition.part_status != "\0":
                digraph.node(f'''{partition.part_name}''', label=f'''<<TABLE>
                    <TR>
                    <TD BGCOLOR="#3BB6E7C9" WIDTH="5">PARTICION</TD>
                    <TD BGCOLOR="#3BB6E7C9" WIDTH="5">{partition.part_type}</TD>
                    </TR>         
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_name</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_name}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_status</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_status}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_type</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_type}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_fit</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_fit}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_start}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_size</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{partition.part_size}</TD>
                    </TR>
                    </TABLE>>''', shape="none")
        #digraph.render('mbr',  view=True)
        existExtendedPartition = False
        tmp_extended_partition = None
        for partition in list_partitions:
            if partition.part_type == "E":
                existExtendedPartition = True
                tmp_extended_partition = partition
                break
        list_ebr = []
        tmp_ebr = EBR()
        if existExtendedPartition and tmp_extended_partition is not None:
            data_ebr = bfm(tmp_path).read_binary_data(tmp_extended_partition.part_start, struct.calcsize(tmp_ebr.FORMATEBR))
            if data_ebr is None:
                fn().err_msg("REP", "No se pudo leer el EBR")
                return
            tmp_ebr.deserialize_ebr(data_ebr)
            list_ebr.append(tmp_ebr)

            while tmp_ebr.ebr_next != -1:
                data_ebr = bfm(tmp_path).read_binary_data(tmp_ebr.ebr_next, struct.calcsize(tmp_ebr.FORMATEBR))
                if data_ebr is None:
                    fn().err_msg("REP", "No se pudo leer el EBR")
                    return
                tmp_ebr = EBR()
                tmp_ebr.deserialize_ebr(data_ebr)
                list_ebr.append(tmp_ebr)
        for ebr in list_ebr:
            digraph.node(f'''{ebr.ebr_name}''', label=f'''<<TABLE>
                    <TR>
                    <TD BGCOLOR="#3BB6E7C9" WIDTH="5">PARTICION</TD>
                    <TD BGCOLOR="#3BB6E7C9" WIDTH="5">LOGICA</TD>
                    </TR>         
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_name</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_name}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_status</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_status}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_fit</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_fit}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_start}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_size</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_size}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">part_next</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{ebr.ebr_next}</TD>
                    </TR>
                    </TABLE>>''', shape="none")
        digraph.render(filename=self.file_name, directory=self.output_path_folder)

    def _create_directory(self):
        if not fn().check_status_folder(self.output_path_folder):
            return fn().create_folder(self.output_path_folder)
        return False
       


        

    def _find_partition(self, listMounts):
        for mount in listMounts:
            if mount.id == self.id:
                self._tmp_partition = mount
                return True
        return False