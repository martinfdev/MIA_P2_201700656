from src.Functions import Functions as fn
import struct
class SuperBlock:
    def __init__(self)->None:
        self.FORMATSUPERBLOCK = "17i"
        self.s_filesystem_type = 0 #0 = EXT3 - 1 = EXT2
        self.s_inodes_count = 0
        self.s_blocks_count = 0
        self.s_free_blocks_count = 0
        self.s_free_inodes_count = 0
        self.s_mtime = 0 #last mount time
        self.s_umtime = 0 #last unmount time
        self.s_mnt_count = 0
        self.s_magic = 0xEF53
        self.s_inode_size = 0
        self.s_block_size = 0
        self.s_first_ino = 0
        self.s_first_blo = 0
        self.s_bm_inode_start = 0 #inode bitmap start
        self.s_bm_block_start = 0 #block bitmap start
        self.s_inode_start = 0 #inodes start
        self.s_block_start = 0 #blocks start
   
    def set_values_super_block(self, s_filesystem_type, s_inodes_count, s_blocks_count, s_free_blocks_count, s_free_inodes_count, s_mtime, s_umtime, s_mnt_count, s_magic, s_inode_size, s_block_size, s_first_ino, s_first_blo, s_bm_inode_start, s_bm_block_start, s_inode_start, s_block_start):
        self.s_filesystem_type = s_filesystem_type #0 = EXT3 - 1 = EXT2
        self.s_inodes_count = s_inodes_count
        self.s_blocks_count = s_blocks_count
        self.s_free_blocks_count = s_free_blocks_count
        self.s_free_inodes_count = s_free_inodes_count
        self.s_mtime = s_mtime
        self.s_umtime = s_umtime
        self.s_mnt_count = s_mnt_count
        self.s_magic = s_magic
        self.s_inode_size = s_inode_size
        self.s_block_size = s_block_size
        self.s_first_ino = s_first_ino
        self.s_first_blo = s_first_blo
        self.s_bm_inode_start = s_bm_inode_start
        self.s_bm_block_start = s_bm_block_start
        self.s_inode_start = s_inode_start
        self.s_block_start = s_block_start

    def serialize_super_block(self):
        fns = fn([])
        return fns.serialize(self.FORMATSUPERBLOCK, self.s_filesystem_type, self.s_inodes_count, self.s_blocks_count, self.s_free_blocks_count, self.s_free_inodes_count, self.s_mtime, self.s_umtime, self.s_mnt_count, self.s_magic, self.s_inode_size, self.s_block_size, self.s_first_ino, self.s_first_blo, self.s_bm_inode_start, self.s_bm_block_start, self.s_inode_start, self.s_block_start)

    def deserialize_super_block(self, data):
        data =  fn([]).deserialize(self.FORMATSUPERBLOCK, data)
        if data is None:
            print("Error al deserializar super bloque")
            return None
        self.s_filesystem_type = data[0]
        self.s_inodes_count = data[1]
        self.s_blocks_count = data[2]
        self.s_free_blocks_count = data[3]
        self.s_free_inodes_count = data[4]
        self.s_mtime = data[5]
        self.s_umtime = data[6]
        self.s_mnt_count = data[7]
        self.s_magic = data[8]
        self.s_inode_size = data[9]
        self.s_block_size = data[10]
        self.s_first_ino = data[11]
        self.s_first_blo = data[12]
        self.s_bm_inode_start = data[13]
        self.s_bm_block_start = data[14]
        self.s_inode_start = data[15]
        self.s_block_start = data[16]
        return self

class Inode:
    def __init__(self)->None:
        self.FORMARTINODETABLE = "6i15ici"
        self.i_uid = 0
        self.i_gid = 0
        self.i_size = 0
        self.i_atime = 0
        self.i_ctime = 0
        self.i_mtime = 0
        self.i_block = [-1]*15 #15 pointers
        self.i_type = '\0' #char
        self.i_perm = 0

    def set_values_inode(self, i_uid, i_gid, i_size, i_atime, i_ctime, i_mtime, i_block, i_type, i_perm):
        if len(i_block) > 15:
            print("Error al asignar valores al inodo, el numero de punteros no puede ser mayor a 15")
            return self
        self.i_uid = i_uid
        self.i_gid = i_gid
        self.i_size = i_size
        self.i_atime = i_atime
        self.i_ctime = i_ctime
        self.i_mtime = i_mtime
        self.i_block = i_block
        self.i_type = i_type
        self.i_perm = i_perm

    def serialize_inode(self):
        fns = fn([])
        return fns.serialize(self.FORMARTINODETABLE, self.i_uid, self.i_gid, self.i_size, self.i_atime, self.i_ctime, self.i_mtime, *self.i_block, fn([]).string_to_bytes(self.i_type), self.i_perm)
    
    def deserialize_inode(self, data):
        data = fn([]).deserialize(self.FORMARTINODETABLE, data)
        if data is None:
            print("Error al deserializar inodo")
            return None
        self.i_uid = data[0]
        self.i_gid = data[1]
        self.i_size = data[2]
        self.i_atime = data[3]
        self.i_ctime = data[4]
        self.i_mtime = data[5]
        self.i_block = data[6:21]
        self.i_type = fn([]).bytes_to_string(data[22])
        self.i_perm = data[23]
        return self

class BlockFolder:
    def __init__(self)->None:
        self.content =  self.content = [Content() for _ in range(4)] #4 content

    def serialize_block_folder(self):
        data = b''
        for item in self.content:
            data += item.serialize_content()
        return data
    
    def deserialize_block_folder(self, data):
        if len(data) != 64:
            print("Error al deserializar bloque de carpeta")
            return None
        tmp_content = Content()
        for i in range(4):
            self.content[i].deserialize_content(data[i*struct.calcsize(tmp_content.FORMARTCONTENT):(i+1)*struct.calcsize(tmp_content.FORMARTCONTENT)])
        return self

class Content:
    def __init__(self)->None:
        self.FORMARTCONTENT = "12si"
        self.b_name = ""
        self.b_inodo = -1

    def serialize_content(self):
        fns = fn([])
        return fns.serialize(self.FORMARTCONTENT, fns.string_to_bytes(self.b_name), self.b_inodo)

    def deserialize_content(self, data):
        data = fn([]).deserialize(self.FORMARTCONTENT, data)
        if data is None:
            print("Error al deserializar Contenido")
            return None
        self.b_name = fn([]).bytes_to_string(data[0])
        self.b_inodo = data[1]
        return self   

class BlockFile:
    def __init__(self)->None:
        self.FORMATBLOCKFILE = "64s"

    def serialize_block_file(self, data):
        fns = fn([])
        return fns.serialize(self.FORMATBLOCKFILE, fns.string_to_bytes(data))

    def deserialize_block_file(self, data):
        data = fn([]).deserialize(self.FORMATBLOCKFILE, data)
        if data is None:
            print("Error al deserializar bloque de archivo")
            return None
        return fn([]).bytes_to_string(data[0])    

class BlockPointer:
    def __init__(self)->None:
        self.FORMATBLOCKPOINTER = "16i"
        self.block_pointer = [-1]*16 #15 pointers

    def serialize_block_pointer(self):
        fns = fn([])
        return fns.serialize(self.FORMATBLOCKPOINTER, *self.block_pointer)

    def deserialize_block_pointer(self, data):
        data = fn([]).deserialize(self.FORMATBLOCKPOINTER, data)
        if data is None:
            print("Error al deserializar bloque de punteros")
            return None
        self.block_pointer = data
        return self    

class Journaling:
    def __init__(self)->None:
        self.FORMATJOURNALING = "16s16s64sI"
        self.operation = "0"
        self.path = "0"
        self.cotent = "0"
        self.date = 0                

    def serialize_journaling(self):
        fns = fn([])
        return fns.serialize(self.FORMATJOURNALING, fns.string_to_bytes(self.operation), fns.string_to_bytes(self.path), fns.string_to_bytes(self.cotent), self.date)
    
    def deserialize_journaling(self, data):
        data = fn([]).deserialize(self.FORMATJOURNALING, data)
        if data is None:
            print("Error al deserializar journaling")
            return None
        self.operation = fn([]).bytes_to_string(data[0])
        self.path = fn([]).bytes_to_string(data[1])
        self.cotent = fn([]).bytes_to_string(data[2])
        self.date = data[3]
        return self

class Bitmap:
    def __init__(self)->None:
        self._FORMATBITMAPINODE = "c"
        self.size_bitmap = 0
        self.array_bitmap = []

    def serialize_bitmap(self, array_bitmap, size_bitmap):
        if len(array_bitmap) == 0:
            self.size_bitmap = size_bitmap
            self._FORMATBITMAPINODE = str(self.size_bitmap) + self._FORMATBITMAPINODE
            self.array_bitmap = [b'0'] * self.size_bitmap
        else:
            self.size_bitmap = len(array_bitmap)
            self.array_bitmap = [fn([]).string_to_bytes(item) for item in array_bitmap]
            self._FORMATBITMAPINODE = str(len(self.array_bitmap)) + self._FORMATBITMAPINODE    
        fns = fn([])
        return fns.serialize(self._FORMATBITMAPINODE, *self.array_bitmap)

    def deserialize_bitmap(self, data, size_bitmap):
        if len(data) != size_bitmap:
            print("Error al deserializar bitmap de inodos no coincide con el tamaño")
            return None
        self.size_bitmap = size_bitmap
        self._FORMATBITMAPINODE = str(self.size_bitmap) + self._FORMATBITMAPINODE
        data = fn([]).deserialize(self._FORMATBITMAPINODE, data)
        if data is None:
            print("Error al deserializar bitmap de inodos")
            return None
        self.array_bitmap = [fn([]).bytes_to_string(item) for item in data]
        return self