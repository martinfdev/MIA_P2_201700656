from src.Functions import Functions as fn
from src.BinaryFileManager import BinaryFileManager as bfm
from src.UtilClass import *
from src.Primitive import *
import struct
from graphviz import Digraph
from src.Blocks import *
import math

class REP:
    def __init__(self, list_params, arr_output_result) -> None:
        self.arr_output_result = arr_output_result
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
            # fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            self.arr_output_result.append("REP: No se encontró la partición con el ID especificado")
            return
        self._create_directory()

        if self.name.lower() == "mbr":
            self._mbr()
            return
        if self.name.lower() == "disk":
            self._disk()
            return
        if self.name.lower() == "bm_inode":
            self._rep_bm_inode()
            return

        if self.name.lower() == "bm_block":
            return

        if self.name.lower() == "block":
            self._rep_block()
            return

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
            # fn().err_msg("REP", "No se especificó el parámetro obligatorio ID")
            self.arr_output_result.append("REP: No se especificó el parámetro obligatorio ID")
            return False
        if self.name == "":
            # fn().err_msg("REP", "No se especificó el parámetro obligatorio NAME")
            self.arr_output_result.append("REP: No se especificó el parámetro obligatorio NAME")
            return False
        if self.output_path == "":
            # fn().err_msg("REP", "No se especificó el parámetro obligatorio PATH")
            self.arr_output_result.append("REP: No se especificó el parámetro obligatorio PATH")
            return False
        return True

    def _mbr(self):
        if self._tmp_partition is None:
            # fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            self.arr_output_result.append("REP: No se encontró la partición con el ID especificado")
            return False
        tmp_path = self._tmp_partition.get_path()
        tmp_mbr = MBR(self.arr_output_result)
        total_bytes_to_read = struct.calcsize(
            tmp_mbr.FORMATMBR) + struct.calcsize(tmp_mbr.mbr_partition_1.FORMATPARTITION) * 4
        binary_data_mbr = bfm(tmp_path, self.arr_output_result).read_binary_data(
            0, total_bytes_to_read)
        if binary_data_mbr is None:
            # fn().err_msg("REP", "No se pudo leer el MBR")
            self.arr_output_result.append("REP: No se pudo leer el MBR")
            return
        tmp_mbr.deserialize_mbr(binary_data_mbr)
        list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2,
                           tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]
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
        # digraph.render('mbr',  view=True)
        existExtendedPartition = False
        tmp_extended_partition = None
        for partition in list_partitions:
            if partition.part_type == "E":
                existExtendedPartition = True
                tmp_extended_partition = partition
                break
        list_ebr = []
        tmp_ebr = EBR(self.arr_output_result)
        if existExtendedPartition and tmp_extended_partition is not None:
            data_ebr = bfm(tmp_path, self.arr_output_result).read_binary_data(
                tmp_extended_partition.part_start, struct.calcsize(tmp_ebr.FORMATEBR))
            if data_ebr is None:
                # fn().err_msg("REP", "No se pudo leer el EBR")
                self.arr_output_result.append("REP: No se pudo leer el EBR")
                return
            tmp_ebr.deserialize_ebr(data_ebr)
            list_ebr.append(tmp_ebr)

            while tmp_ebr.ebr_next != -1:
                data_ebr = bfm(tmp_path, self.arr_output_result).read_binary_data(
                    tmp_ebr.ebr_next, struct.calcsize(tmp_ebr.FORMATEBR))
                if data_ebr is None:
                    # fn().err_msg("REP", "No se pudo leer el EBR")
                    self.arr_output_result.append("REP: No se pudo leer el EBR")
                    return
                tmp_ebr = EBR(self.arr_output_result)
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
        digraph.render(filename=self.file_name,
                       directory=self.output_path_folder)

    def _create_directory(self):
        if not fn(self.arr_output_result).check_status_folder(self.output_path_folder):
            return fn(self.arr_output_result).create_folder(self.output_path_folder)
        return False

    def _find_partition(self, listMounts):
        for mount in listMounts:
            if mount.id == self.id:
                self._tmp_partition = mount
                return True
        return False

    def _disk(self):
        if self._tmp_partition is None:
            # fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            self.arr_output_result.append("REP: No se encontró la partición con el ID especificado")
            return False
        tmp_path = self._tmp_partition.get_path()
        tmp_mbr = MBR(self.arr_output_result)
        total_bytes_to_read = struct.calcsize(
            tmp_mbr.FORMATMBR) + struct.calcsize(tmp_mbr.mbr_partition_1.FORMATPARTITION) * 4
        binary_data_mbr = bfm(tmp_path, self.arr_output_result).read_binary_data(
            0, total_bytes_to_read)
        if binary_data_mbr is None:
            # fn().err_msg("REP", "No se pudo leer el MBR")
            self.arr_output_result.append("REP: No se pudo leer el MBR")
            return
        tmp_mbr.deserialize_mbr(binary_data_mbr)
        list_partitions = [tmp_mbr.mbr_partition_1, tmp_mbr.mbr_partition_2,
                           tmp_mbr.mbr_partition_3, tmp_mbr.mbr_partition_4]

        free_space = 0
        for partition in list_partitions:
            if partition.part_status == "\0":
                free_space += partition.part_size

        label = "MBR"

        for partition in list_partitions:
            if partition.part_status != "\0":
                if partition.part_type == "E":
                    label += '''|{<f0> EXTENDIDA'''
                    current_ebr = EBR(self.arr_output_result)
                    data_ebr = bfm(tmp_path, self.arr_output_result).read_binary_data(
                        partition.part_start, struct.calcsize(current_ebr.FORMATEBR))
                    if data_ebr is None:
                        # fn().err_msg("REP", "No se pudo leer el EBR")
                        self.arr_output_result.append("REP: No se pudo leer el EBR")
                        return
                    current_ebr.deserialize_ebr(data_ebr)
                    label += '''|{<f0>EBR|'''
                    label += f'''{current_ebr.ebr_name}'''
                    while current_ebr.ebr_next != -1:
                        data_ebr = bfm(tmp_path, self.arr_output_result).read_binary_data(
                            current_ebr.ebr_next, struct.calcsize(current_ebr.FORMATEBR))
                        if data_ebr is None:
                            # fn().err_msg("REP", "No se pudo leer el EBR")
                            self.arr_output_result.append("REP: No se pudo leer el EBR")
                            return
                        current_ebr = EBR(self.arr_output_result)
                        current_ebr.deserialize_ebr(data_ebr)
                        label += f'''|EBR|<f0> {current_ebr.ebr_name}'''
                    label += ''''}}'''
                else:
                    label += f'''|<f0> {partition.part_name}'''
            else:
                label += f'''|<f0> LIBRE'''

        label += f'''|<f0> LIBRE'''

        # print(label)
        digraph = Digraph(format='svg', node_attr={"rankdir": "LR"})
        disk = Digraph(name="cluster0", node_attr={"color": "blue"})

        disk.node(name="disk", shape="record", label=label)
        digraph.subgraph(disk)

        digraph.render(filename=self.file_name,
                       directory=self.output_path_folder)

    def _rep_bm_inode(self):
        if self._tmp_partition is None:
            # fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            self.arr_output_result.append("REP: No se encontró la partición con el ID especificado")
            return False
        if self._tmp_partition._tmp_partition.part_type == "E":
            # fn().err_msg("REP", "No se puede ejecutar el reporte bm_inode en una partición lógica")
            self.arr_output_result.append("REP: No se puede ejecutar el reporte bm_inode en una partición lógica")
            return False
        binary_data = bfm(self._tmp_partition.get_path(), self.arr_output_result).read_binary_data(
            self._tmp_partition._tmp_partition.part_start, struct.calcsize(SuperBlock().FORMATSUPERBLOCK))
        if binary_data is None:
            # fn().err_msg("REP", "No se pudo leer el Super Bloque")
            self.arr_output_result.append("REP: No se pudo leer el Super Bloque")
            return
        super_block = SuperBlock()
        super_block.deserialize_super_block(binary_data)
        binary_data_bm_inode = bfm(self._tmp_partition.get_path(), self.arr_output_result).read_binary_data(
            super_block.s_bm_inode_start, super_block.s_inodes_count)
        bm_inode = Bitmap()
        bm_inode.deserialize_bitmap(binary_data_bm_inode, super_block.s_inodes_count)
        array_bitmap = bm_inode.array_bitmap
        dimesion = int(math.sqrt(super_block.s_inodes_count))
        label = ""
        count = 0
        for i in range(dimesion):
            label += f'''<TR>'''
            for j in range(dimesion):
                label += f'''<TD BGCOLOR="gray" WIDTH="5">{array_bitmap[count]}</TD>'''
                count += 1
            label += f'''</TR>'''   
                
        graph = Digraph(format='svg', node_attr={"rankdir": "LR"})
        graph.node(f'''REPORTE Bitmap Inodos''', label=f'''<<TABLE>
                    <TR>
                    <TD BGCOLOR="green" WIDTH="5">REPORTE Bitmap Inodos</TD>
                    <TD BGCOLOR="green" WIDTH="5">{self._tmp_partition._tmp_partition.part_name}</TD>
                    </TR>
                    {label}
                    </TABLE>>''', shape="none")
        graph.render(filename=self.file_name, directory=self.output_path_folder)
        

    def _rep_block(self):
        if self._tmp_partition is None:
            # fn().err_msg("REP", "No se encontró la partición con el ID especificado")
            self.arr_output_result.append("REP: No se encontró la partición con el ID especificado")
            return False
        if self._tmp_partition._tmp_partition.part_type == "E":
            # fn().err_msg("REP", "No se puede ejecutar el reporte bm_inode en una partición lógica")
            self.arr_output_result.append("REP: No se puede ejecutar el reporte bm_inode en una partición lógica")
            return False
        binary_data = bfm(self._tmp_partition.get_path(), self.arr_output_result).read_binary_data(
            self._tmp_partition._tmp_partition.part_start, struct.calcsize(SuperBlock().FORMATSUPERBLOCK))
        if binary_data is None:
            # fn().err_msg("REP", "No se pudo leer el Super Bloque")
            self.arr_output_result.append("REP: No se pudo leer el Super Bloque")
            return
        super_block = SuperBlock()
        super_block.deserialize_super_block(binary_data)
        graph = Digraph(format='svg', node_attr={"rankdir": "LR"})
        graph.node(f'''REPORTE Super Bloque''', label=f'''<<TABLE>
                    <TR>
                    <TD BGCOLOR="green" WIDTH="5">REPORTE Super Bloque</TD>
                    <TD BGCOLOR="green" WIDTH="5">{self._tmp_partition._tmp_partition.part_name}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_filesystem_type</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_filesystem_type}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_inodes_count</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_inodes_count}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_blocks_count</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_blocks_count}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_free_blocks_count</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_free_blocks_count}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_free_inodes_count</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_free_inodes_count}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_mtime</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{fn(self.arr_output_result).get_time_stamp_obj(super_block.s_mtime)}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_umtime</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{fn(self.arr_output_result).get_time_stamp_obj(super_block.s_umtime)}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_mnt_count</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_mnt_count}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_magic</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_magic}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_inode_s</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_inode_size}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_block_s</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_block_size}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_first_ino</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_first_ino}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_first_blo</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_first_blo}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_bm_inode_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_bm_inode_start}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_bm_block_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_bm_block_start}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_inode_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_inode_start}</TD>
                    </TR>
                    <TR>
                    <TD BGCOLOR="yellow" WIDTH="5">s_block_start</TD>
                    <TD BGCOLOR="yellow" WIDTH="5">{super_block.s_block_start}</TD>
                    </TR>
                    </TABLE>>''', shape="none")
        graph.render(filename=self.file_name,
                     directory=self.output_path_folder)

