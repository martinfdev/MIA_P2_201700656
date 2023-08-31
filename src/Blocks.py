from src.Functions import Functions as fn
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
        fns = fn()
        return fns.serialize(self.FORMATSUPERBLOCK, self.s_filesystem_type, self.s_inodes_count, self.s_blocks_count, self.s_free_blocks_count, self.s_free_inodes_count, self.s_mtime, self.s_umtime, self.s_mnt_count, self.s_magic, self.s_inode_size, self.s_block_size, self.s_first_ino, self.s_first_blo, self.s_bm_inode_start, self.s_bm_block_start, self.s_inode_start, self.s_block_start)

    def deserialize_super_block(self, data):
        data =  fn().deserialize(self.FORMATSUPERBLOCK, data)
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
        self.FORMARTINODETABLE = "6i16ici"

class BlockFolder:
    def __init__(self)->None:
        self.content = [Content]*4 #4 content

class Content:
    def __init__(self)->None:
        self.FORMARTCONTENT = "12si"

class BlockFile:
    def __init__(self)->None:
        self.FORMATBLOCKFILE = "64s"

class BlockPointer:
    def __init__(self)->None:
        self.FORMATBLOCKPOINTER = "16i"
        self.block_pointer = []

class Journaling:
    def __init__(self)->None:
        self.FORMATJOURNALING = "32s"                

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
            self.array_bitmap = [fn().string_to_bytes(item) for item in array_bitmap]
            self._FORMATBITMAPINODE = str(len(self.array_bitmap)) + self._FORMATBITMAPINODE    
        fns = fn()
        return fns.serialize(self._FORMATBITMAPINODE, *self.array_bitmap)

    def deserialize_bitmap(self, data, size_bitmap):
        if len(data) != size_bitmap:
            print("Error al deserializar bitmap de inodos no coincide con el tamaño")
            return None
        self.size_bitmap = size_bitmap
        self._FORMATBITMAPINODE = str(self.size_bitmap) + self._FORMATBITMAPINODE
        data = fn().deserialize(self._FORMATBITMAPINODE, data)
        if data is None:
            print("Error al deserializar bitmap de inodos")
            return None
        self.array_bitmap = [fn().bytes_to_string(item) for item in data]
        return self