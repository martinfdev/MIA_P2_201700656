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
        self._tmp_mbr = MBR()

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

        #delete partition with name
        if self._delete is not None:
            if not self._check_exist_partition_with_name(list_partition, self._name):
                fn.err_msg("FDISK", "delete no existe la partición con el nombre "+fn.RED+str(self._name))
                return
            if not self._delete_partition(list_partition):
                fn.err_msg("FDISK", "delte no se pudo eliminar la partición "+fn.RED+str(self._name))
                return
            else:
                fn.success_msg("FDISK", "Se eliminó la partición "+fn.RED+str(self._name))
                return
        
        #add partition size to partition with name
        if self._add is not None:
            if not self._check_exist_partition_with_name(list_partition, self._name):
                fn.err_msg("FDISK", "add no existe partición con el nombre "+fn.RED+str(self._name))
                return
            if not self._add_size_partition(list_partition):
                fn.err_msg("FDISK", "add no se pudo agregar el tamaño a la partición "+fn.RED+str(self._name))
                return
            else:
                fn.success_msg("FDISK", "Se agregó el tamaño a la partición "+fn.RED+str(self._name))
                return

        #check if exist entended partition for logical partition
        if self._type == 'L':
            if not self._check_exist_extented_partition(self._tmp_mbr):
                fn.err_msg("FDISK", "No existe una partición extendida para particion logica en "+fn.RED+self._path)
                return
            if not self._add_logic_partition(list_partition):
                fn.err_msg("FDISK", "No se pudo agregar la partición logica "+fn.RED+str(self._name))
                return
            else:
                fn.success_msg("FDISK", "Se agregó la partición logica "+fn.RED+str(self._name))
                return
            
        #check if name partition exist
        if self._check_exist_partition(self._tmp_mbr, self._name):
            fn.err_msg("FDISK", "Ya existe una partición con el nombre "+fn.RED+str(self._name))
            return
        
        #check free space in disk
        if self._get_free_space_disk(list_partition) < self._get_value_unit_partition():
            fn.err_msg("FDISK", "No hay espacio disponible en el disco "+fn.RED+self._path)
            return

        #check if exist extended partition
        if self._type == 'E' and self._check_exist_extented_partition(self._tmp_mbr):
            fn.err_msg("FDISK", "Ya existe una partición extendida en el disco "+fn.RED+self._path)
            return
        elif self._type == 'E' and not self._check_exist_extented_partition(self._tmp_mbr):
            newEBR = EBR()
            bfm(self._path).write_binary_data(newEBR.serialize_ebr(), self._calculate_partition_start(list_partition))

        #create partition
        newpart = self._create_partition()
        if newpart is None:
            return
        newpart.part_start = self._calculate_partition_start(list_partition)
        if newpart is None:
            return
        if self._mbr_fit == 'F':
            value = self._set_partitition_with_first_fit(list_partition, newpart)
            if value:
                fn.err_msg("FDISK", "No se pudo agregar la partición maximo 4 particiones "+fn.RED+str(self._name))
                return

        if self._mbr_fit == 'B':
            value = self._set_partitition_with_best_fit(list_partition, newpart)
            if value:
                fn.err_msg("FDISK", "No se pudo agregar la partición maximo 4 particiones "+fn.RED+str(self._name))
                return
            
        if self._mbr_fit == 'W':
            value = self._set_partitition_with_worst_fit(list_partition, newpart)
            if value:
                fn.err_msg("FDISK", "No se pudo agregar la partición maximo 4 particiones "+fn.RED+str(self._name))
                return

        self._tmp_mbr.mbr_partition_1 = list_partition[0]
        self._tmp_mbr.mbr_partition_2 = list_partition[1]
        self._tmp_mbr.mbr_partition_3 = list_partition[2]
        self._tmp_mbr.mbr_partition_4 = list_partition[3]

        bfm(self._path).write_binary_data(self._tmp_mbr.serialize_mbr(), 0)
        fn.success_msg("FDISK", "Se agregó la partición "+fn.RED+str(self._name))




    #error = False; success = True 
    def _set_params(self):
        param_add_delete_found = False
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
            elif not param_add_delete_found and isinstance(param, Delete):
                self._delete = param.get_value()
                param_add_delete_found = True
            elif not param_add_delete_found and isinstance(param, Add):
                self._add = param.get_value()
                param_add_delete_found = True
            if self._type != "P" and self._type != "E" and self._type != "L":
                fn.err_msg("FDISK", "El valor del parámetro TYPE no es válido solo se acepta P, E o L")
                return False
            if self._fit != "BF" and self._fit != "FF" and self._fit != "WF":
                fn.err_msg("FDISK", "El valor del parámetro FIT no es válido solo se acepta BF, FF o WF")
                return False
            if self._unit != "K" and self._unit != "M" and self._unit != "B":
                fn.err_msg("FDISK", "El valor del parámetro UNIT no es válido solo se acepta K, M o B")
            if self._add is not None:
                if self._add < 1:
                    fn.err_msg("FDISK", "El valor del parámetro ADD debe ser mayor a 0")
                    return False    
            if self._delete is not None:
                if self._delete != "FULL":
                    fn.err_msg("FDISK", "El valor del parámetro DELETE no es válido solo se acepta FULL")
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

        return self._tmp_mbr
    
    def _create_partition(self):
        fn = fns()
       
        if self._name == None:
            fn.err_msg("FDISK", "No se especificó el parámetro obligatorio NAME");
            return None
        new_part = Partition()
        new_part.part_status = '1'
        new_part.part_type = self._type
        new_part.part_fit = self._get_fit_partition()
        new_part.part_size = self._get_value_unit_partition()
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

    def _get_value_unit_partition(self):
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

    def _calculate_partition_start(self, list_part):
        start = struct.calcsize(self._tmp_mbr.FORMATMBR)+struct.calcsize(self._tmp_mbr.mbr_partition_1.FORMATPARTITION)*4
        for part in list_part:
            if part.part_type != '\0':
                start += part.part_size
        return start

    def _check_exist_partition(self, mbr, name):
        if mbr.mbr_partition_1.part_name == name or mbr.mbr_partition_2.part_name == name or mbr.mbr_partition_3.part_name == name or mbr.mbr_partition_4.part_name == name:
            return True
        return False

    def _get_free_space_disk(self, list_partition):
        free_space = 0
        free_space = self._mbr_size
        for part in list_partition:
            if part.part_type != '\0':
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
    
    def _set_partitition_with_best_fit(self, list_partition, new_part):
        best_fit = None
        for i in range(0, len(list_partition)):
            if list_partition[i].part_type == '\0':
                if best_fit is None:
                    best_fit = list_partition[i]
                elif best_fit.part_size > list_partition[i].part_size:
                    best_fit = list_partition[i]
        if best_fit is None:
            return True
        best_fit = new_part
        return False

    def _set_partitition_with_worst_fit(self, list_partition, new_part):
        worst_fit = None
        for i in range(0, len(list_partition)):
            if list_partition[i].part_type == '\0':
                if worst_fit is None:
                    worst_fit = list_partition[i]
                elif worst_fit.part_size < list_partition[i].part_size:
                    worst_fit = list_partition[i]
        if worst_fit is None:
            return True
        worst_fit = new_part
        return False

    def _delete_partition(self, list_partition):
        state = False
        pointer_to_delete = 0 
        size_to_delete = 0
        for part in list_partition:
            if part.part_name == self._name:
                pointer_to_delete = part.part_start
                size_to_delete = part.part_size
                part.part_status = '\0'
                part.part_type = '\0'
                part.part_fit = '\0'
                part.part_start = 0
                part.part_name = '\0'*16
                state = True
        if state:
            self._tmp_mbr.mbr_partition_1 = list_partition[0]
            self._tmp_mbr.mbr_partition_2 = list_partition[1]
            self._tmp_mbr.mbr_partition_3 = list_partition[2]
            self._tmp_mbr.mbr_partition_4 = list_partition[3]
            bfm(self._path).write_binary_data(self._tmp_mbr.serialize_mbr(), 0)
            bfm(self._path).fill_binary_file(size_to_delete, pointer_to_delete)
        return state
    
    def _add_size_partition(self, list_partition):
        if self._add is None:
            return False
        self._size = self._add
        self._add = self._get_value_unit_partition()
        if self._get_free_space_disk(list_partition) < self._add:
            fn().err_msg("FDISK", "Add no hay espacio disponible en el disco "+fn().RED+self._path)
            return False
        state = False
        for part in list_partition:
            if part.part_name == self._name:
                part.part_size += self._add
                state = True
        if state:
            self._tmp_mbr.mbr_partition_1 = list_partition[0]
            self._tmp_mbr.mbr_partition_2 = list_partition[1]
            self._tmp_mbr.mbr_partition_3 = list_partition[2]
            self._tmp_mbr.mbr_partition_4 = list_partition[3]
            bfm(self._path).write_binary_data(self._tmp_mbr.serialize_mbr(), 0)
        return state
    
    def _add_logic_partition(self, list_partition):
        current_ebr = EBR()
        ext_partition = None
        for part in list_partition:
            if part.part_type == 'E':
                ext_partition = part
                break
        if ext_partition is None:
            return False
        
        if ext_partition.part_size < self._get_value_unit_partition():
            fn().err_msg("FDISK", "No hay espacio disponible en la partición extendida "+fn().RED+self._path)
            return False
        #read default ebr in extended partition
        current_ebr.deserialize_ebr(bfm(self._path).read_binary_data(ext_partition.part_start, struct.calcsize(current_ebr.FORMATEBR)))

        #default ebr is empty write new ebr
        free_space = ext_partition.part_size
        if current_ebr.ebr_size == 0:
            current_ebr.ebr_status = '1'
            current_ebr.ebr_fit = self._get_fit_partition()
            current_ebr.ebr_size = self._get_value_unit_partition()
            current_ebr.ebr_next = -1
            current_ebr.ebr_name = self._name
            current_ebr.ebr_start = ext_partition.part_start
            bfm(self._path).write_binary_data(current_ebr.serialize_ebr(), ext_partition.part_start)
            return True
        free_space -= current_ebr.ebr_size
        if current_ebr.ebr_name == self._name:
                fn().err_msg("FDISK", "Ya existe una partición logica con el nombre "+fn().RED+str(self._name))
                return False
        while current_ebr.ebr_next != -1:
            current_ebr.deserialize_ebr(bfm(self._path).read_binary_data(current_ebr.ebr_next, struct.calcsize(current_ebr.FORMATEBR)))
            free_space -= current_ebr.ebr_size
            if current_ebr.ebr_name == self._name:
                fn().err_msg("FDISK", "Ya existe una partición logica con el nombre "+fn().RED+str(self._name))
                return False
        
        if free_space < self._get_value_unit_partition():
            fn().err_msg("FDISK", "No se puede agregar particion logica insuficiente espacio en la partición extendida "+fn().RED+self._path)
            return False

        current_ebr.ebr_next = current_ebr.ebr_start + current_ebr.ebr_size
        bfm(self._path).write_binary_data(current_ebr.serialize_ebr(), current_ebr.ebr_start)
        new_ebr = EBR()
        new_ebr.ebr_status = '1'
        new_ebr.ebr_fit = self._get_fit_partition()
        new_ebr.ebr_size = self._get_value_unit_partition()
        new_ebr.ebr_next = -1
        new_ebr.ebr_name = self._name
        bfm(self._path).write_binary_data(new_ebr.serialize_ebr(), current_ebr.ebr_next)
        return True
