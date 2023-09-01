from src.Primitive import ID, Type, FS
from src.Functions import Functions as fn
from src.Mount import Mount
from src.UtilClass import *
from src.Blocks import *
from src.BinaryFileManager import BinaryFileManager as bfm

class Mkfs:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._id = ""
        self._type = "FULL"
        self._fs = "2FS"
        self._tmp_partition = None
        self._tmp_path = ""

    def execute_mkfs(self, list_mounts):
        if not self._set_values_props_mkfs():
            return
        if len(list_mounts) == 0:
            fn().err_msg("MKFS", "No hay particiones montadas.")
            return
        if not self._check_is_mounted_partition(list_mounts):
            fn().err_msg("MKFS", "La partición "+str(self._id)+" no está montada.")
            return
        
        if self._fs == "2FS":
            if not self._mkfs_2fs():
                fn().err_msg("MKFS", "No se pudo formatear la partición "+str(self._id))
                return
            
        if self._fs == "3FS":
            if not self._mkfs_3fs():
                fn().err_msg("MKFS", "No se pudo formatear la partición "+str(self._id))
                return
        fn().success_msg("MKFS", "Se formateó la partición "+str(self._id)+" con exito.")

    def _set_values_props_mkfs(self):
        for param in self._list_params:
            if isinstance(param, ID):
                self._id = param.value
            elif isinstance(param, Type):
                if param.value != None:
                    self._type = param.value.upper()
            elif isinstance(param, FS):
                if param.value != None:
                    self._fs = param.value.upper()

        if self._id == "":
            fn().err_msg("MKFS", "No se ha especificado el -id=? de la partición.")
            return False
        if self._type != "FULL":
            fn().err_msg("MKFS", "El parametro de -type no es valido.")
            return False
        if self._fs != "2FS" and self._fs != "3FS":
            fn().err_msg("MKFS", "El parametro de -fs no es valido.")
            return False
        return True

    def _check_is_mounted_partition(self, list_mounts):
        for mount in list_mounts:
            if isinstance(mount, Mount):
                if mount.id == self._id:
                    self._tmp_partition = mount.get_partition()
                    self._tmp_path = mount.get_path()
                    return True
        return False
    
    def _mkfs_2fs(self):
        if self._tmp_partition == None:
            fn().err_msg("MKFS", "No se encontró la partición "+str(self._id))
            return False
        if isinstance(self._tmp_partition, Partition):
            if str(self._tmp_partition.part_type) == "E":   
                fn().err_msg("MKFS", "No se puede formatear una partición extendida.")
                return False
        if not self._create_superblock(1):  #0 = EXT3 - 1 = EXT2   
            fn().err_msg("MKFS", "No se pudo crear el super bloque.")
            return False
        return True

    def _mkfs_3fs(self):
        if self._tmp_partition == None:
            fn().err_msg("MKFS", "No se encontró la partición "+str(self._id))
            return False
        if isinstance(self._tmp_partition, Partition):
            if str(self._tmp_partition.part_type) == "E":   
                fn().err_msg("MKFS", "No se puede formatear una partición extendida.")
                return False
        if not self._create_superblock(0):  #0 = EXT3 - 1 = EXT2   
            fn().err_msg("MKFS", "No se pudo crear el super bloque.")
            return False
        return True

    def _create_superblock(self, type_fs):
        new_super_block = SuperBlock()
        inode = Inode()
        block = Content()
        bitmap = Bitmap()
        value_of_n = 0
        fns = fn()
        pos_init_value = {}
        if isinstance(self._tmp_partition, Partition):
            if self._fs == "2FS":
                value_of_n = fns.calculate_value_of_n(self._tmp_partition.part_size, new_super_block , inode, block)
            if self._fs == "3FS":
                value_of_n = fns.calculte_n_with_journaling(self._tmp_partition.part_size, Journaling(), new_super_block , inode, block)
            bitmap.size_bitmap = value_of_n
            if self._fs == "2FS":
                pos_init_value = self._first_pos(value_of_n, self._tmp_partition.part_start)
            if self._fs == "3FS":
                pos_init_value = self._first_pos_with_journaling(value_of_n, self._tmp_partition.part_start)
            if pos_init_value is None:
                return False
            #print("primary partition", value_of_n)
            #print(pos_init_value)
        
        if isinstance(self._tmp_partition, EBR):
            if self._fs == "2FS":           
                value_of_n = fns.calculate_value_of_n(self._tmp_partition.ebr_size, new_super_block , inode, block)
            if self._fs == "3FS":
                value_of_n = fns.calculte_n_with_journaling(self._tmp_partition.ebr_size, Journaling(), new_super_block , inode, block)
            bitmap.size_bitmap = value_of_n
            if self._fs == "2FS":
                pos_init_value = self._first_pos(value_of_n, self._tmp_partition.ebr_start, struct.calcsize(EBR().FORMATEBR))
            if self._fs == "3FS":
                pos_init_value = self._first_pos_with_journaling(value_of_n, self._tmp_partition.ebr_start, struct.calcsize(EBR().FORMATEBR))
            if pos_init_value is None:
                return False
           # print("logical partition", value_of_n)
           # print(pos_init_value)
        #typefs is int 0 = ext3, 1 = ext2
        if len(pos_init_value) == 0:
            return False
        
        new_super_block.set_values_super_block(type_fs, value_of_n, 3*value_of_n, 3*value_of_n, value_of_n, fns.get_time_stamp(fns.get_time_stamp_now()), fns.get_time_stamp(fns.get_time_stamp_now()), 1, 0xEF53, struct.calcsize(inode.FORMARTINODETABLE), struct.calcsize(block.FORMARTCONTENT)*4, pos_init_value["inode"], pos_init_value["block"], pos_init_value["bitmap_inode"], pos_init_value["bitmap_block"], pos_init_value["inode"], pos_init_value["block"])

        bf = bfm(self._tmp_path)

        if self._fs == "3FS":
            journaling = Journaling()
            bf.write_binary_data(journaling.serialize_journaling(), pos_init_value["journaling"])

        bf.write_binary_data(new_super_block.serialize_super_block(), pos_init_value["super_block"])
        inode_bitmap = Bitmap()
        #bitmap inode, new bitmap serialize array of 0 = []
        bf.write_binary_data(inode_bitmap.serialize_bitmap([], value_of_n), pos_init_value["bitmap_inode"])
        #bitmap block, new bitmap serialize array of 0 = []
        block_bitmap = Bitmap()
        bf.write_binary_data(block_bitmap.serialize_bitmap([], (value_of_n*3)), pos_init_value["bitmap_block"])
        #inodes
        first_inode = Inode()
        size_inode = struct.calcsize(first_inode.FORMARTINODETABLE)
        time_stamp = fns.get_time_stamp(fns.get_time_stamp_now())
        list_pointers = [-1]*15
        list_pointers[0] = pos_init_value["block"]
        first_inode.set_values_inode(0, 0, size_inode, time_stamp, time_stamp, time_stamp, list_pointers, '1', 0)
        bf.write_binary_data(first_inode.serialize_inode(), pos_init_value["inode"])
        #blocks
        first_block = BlockFolder()
        bf.write_binary_data(first_block.serialize_block_folder(), pos_init_value["block"])
        return True


    def _first_pos(self, value_n, part_start, size_ebr=0):
        init_pos_value = {"super_block":0, "bitmap_inode": 0, "bitmap_block": 0, "inode": 0, "block": 0}
        init_pos_value["super_block"] = part_start+size_ebr
        init_pos_value["bitmap_inode"] = init_pos_value["super_block"]+struct.calcsize(SuperBlock().FORMATSUPERBLOCK) 
        init_pos_value["bitmap_block"] = init_pos_value["bitmap_inode"]+value_n
        init_pos_value["inode"] = init_pos_value["bitmap_block"]+value_n*3
        init_pos_value["block"] = init_pos_value["inode"]+value_n*struct.calcsize(Inode().FORMARTINODETABLE)
        return init_pos_value     
    
    def _first_pos_with_journaling(self, value_n, part_start, size_ebr=0):
        init_pos_value = {"super_block":0, "journaling": 0, "bitmap_inode": 0, "bitmap_block": 0, "inode": 0, "block": 0}
        init_pos_value["super_block"] = part_start+size_ebr
        init_pos_value["journaling"] = init_pos_value["super_block"]+struct.calcsize(SuperBlock().FORMATSUPERBLOCK)
        init_pos_value["bitmap_inode"] = init_pos_value["journaling"]+struct.calcsize(Journaling().FORMATJOURNALING)*value_n
        init_pos_value["bitmap_block"] = init_pos_value["bitmap_inode"]+value_n
        init_pos_value["inode"] = init_pos_value["bitmap_block"]+value_n*3
        init_pos_value["block"] = init_pos_value["inode"]+value_n*struct.calcsize(Inode().FORMARTINODETABLE)
        return init_pos_value