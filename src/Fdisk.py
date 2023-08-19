from src.Primitive import *
from src.UtilClass import *
from src.Functions import Functions as fns
from src.BinaryFileManager import BinaryFileManager as bfm
class Fdisk:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._size = None
        self._folders_dir = ""
        self._file_name = ""
        self._path = ""
        self._name = None
        self._unit = "K"
        self._type = "P"
        self._fit = "WF"
        self._delete = None
        self._add = None
        self._mbr_size = 0
        self._mbr_fit = ''
        self._tmp_mbr = None

    def executefdisk(self):
        fn = fns()
        if not self._set_params():
            fn.err_msg("FDISK", "No se pudo agregar la partición")
            return

        self._tmp_mbr = self._read_mbr_in_file()
        if self._tmp_mbr is None:
            fn.err_msg("FDISK", "No se pudo leer el MBR")
            fn.err_msg("FDISK", "No se pudo agregar la partición")
            return
        list_partition=[self._tmp_mbr.mbr_partition_1, self._tmp_mbr.mbr_partition_2, self._tmp_mbr.mbr_partition_3, self._tmp_mbr.mbr_partition_4]
        self._mbr_size = self._tmp_mbr.mbr_tamano
        self._mbr_fit = self._tmp_mbr.mbr_disk_fit
     
        #check data name is not None
        if self._check_name_is_none():
            fn.err_msg("FDISK", "No se pudo agregar la partición")
            return

        #check if name partition exist
        if self._check_exist_partition(self._tmp_mbr, self._name):
            fn.err_msg("FDISK", "Ya existe una partición con el nombre "+fn.RED+str(self._name))
            return
        
        #check free space in disk
        if self._get_free_space_disk(list_partition) < self._get_unit_partition():
            fn.err_msg("FDISK", "No hay espacio disponible en el disco "+fn.RED+self._path)
            return

        #check if exist extended partition
        if self._type == 'E' and self._check_exist_extented_partition(self._tmp_mbr):
            fn.err_msg("FDISK", "Ya existe una partición extendida en el disco "+fn.RED+self._path)
            return
        
        #check if exist entended partition for logical partition
        if self._type == 'L' and not self._check_exist_extented_partition(self._tmp_mbr):
            fn.err_msg("FDISK", "No existe una partición extendida en el disco "+fn.RED+self._path)
            return
           
        newpart = self._create_partition()
        if newpart is None:
            return
        if self._mbr_fit == 'F':
            value = self._set_partitition_with_first_fit(list_partition, newpart)
            if value:
                fn.err_msg("FDISK", "No se pudo agregar la partición "+fn.RED+str(self._name))
                return
        self._tmp_mbr.mbr_partition_1 = list_partition[0]
        self._tmp_mbr.mbr_partition_2 = list_partition[1]
        self._tmp_mbr.mbr_partition_3 = list_partition[2]
        self._tmp_mbr.mbr_partition_4 = list_partition[3]

        bfm(self._path).write_binary_data(self._tmp_mbr.serialize_mbr(), 0)

    #error = False; success = True 
    def _set_params(self):
        fn = fns()
        for param in self._list_params:
            if isinstance(param, Size):
                self._size = param.get_value()
            elif isinstance(param, Path):
                self._folders_dir = param.path 
                self._file_name = param.filename
                self._path = param.get_value()
            elif isinstance(param, ID):
                self._name = param.get_value()    
            elif isinstance(param, Unit):
                self._unit = param.get_value()
            elif isinstance(param, Type):
                self._type = param.get_value()
            elif isinstance(param, Fit):
                self._fit = param.get_value()
            elif isinstance(param, Delete):
                self._delete = param.get_value()
            elif isinstance(param, Add):
                self._add = param.get_value()
            if self._type != "P" and self._type != "E" and self._type != "L":
                fn.err_msg("FDISK", "El valor del parámetro TYPE no es válido solo se acepta P, E o L")
                return False
            if self._fit != "BF" and self._fit != "FF" and self._fit != "WF":
                fn.err_msg("FDISK", "El valor del parámetro FIT no es válido solo se acepta BF, FF o WF")
                return False
            if self._unit != "K" and self._unit != "M" and self._unit != "B":
                fn.err_msg("FDISK", "El valor del parámetro UNIT no es válido solo se acepta K, M o B")
                return False
        return True

    def _read_mbr_in_file(self):
        fn = fns()
        if self._path == "":
            fn.err_msg("FDISK", "No se especificó el parámetro obligatorio PATH");
            return None
        if not fn.check_status_file(self._path):
            fn.err_msg("FDISK", "El archivo no existe "+fn.RED+self._path);
            return None
        self._tmp_mbr = MBR()
        total_bytes_to_read = struct.calcsize(self._tmp_mbr.FORMATMBR) + struct.calcsize(self._tmp_mbr.mbr_partition_1.FORMATPARTITION) * 4
        binary_data_mbr = bfm(self._path).read_binary_data(0, total_bytes_to_read)
        self._tmp_mbr.deserialize_mbr(binary_data_mbr)
        print("=============REP MBR=============")
        print(f"MBR_TAMANO: {self._tmp_mbr.mbr_tamano} bytes")
        print(f"MBR_TIME_STAMP: {self._tmp_mbr.mbr_time_stamp}")
        print(f"MBR_DISK_SIGNATURE: {self._tmp_mbr.mbr_disk_signature}")
        return self._tmp_mbr
    
    def _create_partition(self):
        fn = fns()
       
        if self._name == None:
            fn.err_msg("FDISK", "No se especificó el parámetro obligatorio NAME");
            return None
        new_part = Partition()
        new_part.part_status = '0'
        new_part.part_type = self._type
        new_part.part_fit = self._get_fit_partition()
        new_part.part_size = self._get_unit_partition()
        #new_part.part_start = self._calculate_partition_start()
        new_part.part_name = self._name
        return new_part

    def _get_fit_partition(self):
        fn = fns()
        if self._fit == "BF":
            return 'B'
        elif self._fit == "FF":
            return 'F'
        elif self._fit == "WF":
            return 'W'
        fn.err_msg("FDISK", "El valor del parámetro FIT no es válido solo se acepta BF, FF o WF");
        return b'0'   

    def _get_unit_partition(self):
        fn = fns()
        if self._size == None:
            fn.err_msg("FDISK", "No se especificó el parámetro obligatorio SIZE");
            return 0
        if self._unit == "K":
            return 1024*self._size
        elif self._unit == "M":
            return 1024*1024 *self._size
        elif self._unit == "B":
            return self._size
        fn.err_msg("FDISK", "El valor del parámetro UNIT no es válido solo se acepta K, M o B");
        return 0
    
    def _check_exist_extented_partition(self, mbr):
        if mbr.mbr_partition_1.part_type == 'E' or mbr.mbr_partition_2.part_type == 'E' or mbr.mbr_partition_3.part_type == 'E' or mbr.mbr_partition_4.part_type == 'E':
            return True
        return False

    def _calculate_partition_start(self, lits_partion):
        if len(lits_partion) == 0:
            return 0
        elif len(lits_partion) == 1:
            return lits_partion[0].part_start + lits_partion[0].part_size
        else:
            return lits_partion[len(lits_partion)-1].part_start + lits_partion[len(lits_partion)-1].part_size

    def _check_exist_partition(self, mbr, name):
        if mbr.mbr_partition_1.part_name == name or mbr.mbr_partition_2.part_name == name or mbr.mbr_partition_3.part_name == name or mbr.mbr_partition_4.part_name == name:
            return True
        return False

    def _get_free_space_disk(self, list_partition):
        free_space = self._mbr_size
        for part in list_partition:
            free_space -= part.part_size
        return free_space
    
    def _check_exist_partition_with_name(self, list_partition, name):
        for part in list_partition:
            if part.part_name == name:
                return True
        return False
    
    # False = exist data, True = None
    def _check_name_is_none(self):
        fn = fns()
        if self._size == None:
            fn.err_msg("FDISK", "No se especificó el parámetro obligatorio SIZE");
            return True
        if self._size < 1:
            fn.err_msg("FDISK", "El valor del parámetro SIZE debe ser mayor a 0");
            return True
        return False
    
    def _set_partitition_with_first_fit(self, list_partition, new_part):
        for i in range(0, len(list_partition)):
            if list_partition[i].part_type == '\0':
                list_partition[i] = new_part
                return False
        return True