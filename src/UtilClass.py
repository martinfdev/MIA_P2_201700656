from src.Functions import Functions as fn
import struct
class MBR:
    def __init__(self) -> None:
        self.FORMATMBR = '3Ic' # 4 int y 1 char
        self.mbr_tamano = 0 # 4 bytes tipo int
        self.mbr_time_stamp = 0 # 4 bytes tipo int
        self.mbr_disk_signature = 0 # 4 bytes tipo int
        self.mbr_disk_fit = b'\0' # 1 byte tipo char
        self.mbr_partition_1 = Partition()
        self.mbr_partition_2 = Partition()
        self.mbr_partition_3 = Partition()
        self.mbr_partition_4 = Partition()
    
    def setValues(self, mbr_tamano, mbr_time_stamp, disk_signature, mbr_disk_fit):
        self.mbr_tamano = mbr_tamano
        self.mbr_time_stamp = mbr_time_stamp
        self.mbr_disk_signature = disk_signature
        self.mbr_disk_fit = fn().string_to_bytes(mbr_disk_fit)
        self.mbr_partition_1 = Partition()
        self.mbr_partition_2 = Partition()
        self.mbr_partition_3 = Partition()
        self.mbr_partition_4 = Partition()

    def serialize_mbr(self):
        bytesMBR = fn().serialize(self.FORMATMBR, self.mbr_tamano, self.mbr_time_stamp, self.mbr_disk_signature, self.mbr_disk_fit)
        return bytesMBR + self.mbr_partition_1.serialize_partition() + self.mbr_partition_2.serialize_partition() + self.mbr_partition_3.serialize_partition() + self.mbr_partition_4.serialize_partition()
    
    def deserialize_mbr(self, data):
        const_mbr = struct.calcsize(self.FORMATMBR)
        const_partition = struct.calcsize(self.mbr_partition_1.FORMATPARTITION)
        fns = fn()
        bytesMBR = fns.deserialize(self.FORMATMBR, data[:const_mbr])
        if bytesMBR is None:
            fns.err_msg("MBR", "No se pudo deserializar el MBR")
            return None
        self.mbr_tamano = bytesMBR[0]
        self.mbr_time_stamp = fns.get_time_stamp_obj(bytesMBR[1])
        self.mbr_disk_signature = bytesMBR[2]
        self.mbr_disk_fit = fns.bytes_to_string(bytesMBR[3])
        #partition 1
        data_p1 = const_mbr,  const_mbr+const_partition
        self.mbr_partition_1 = Partition().deserialize_partition(data[data_p1[0]:data_p1[1]], 1)
        #partition 2
        data_p2 = const_mbr+const_partition, const_mbr+const_partition*2
        self.mbr_partition_2 = Partition().deserialize_partition(data[data_p2[0]:data_p2[1]], 2)
        #partition 3
        data_p3 = const_mbr+const_partition*2, const_mbr+const_partition*3
        self.mbr_partition_3 = Partition().deserialize_partition(data[data_p3[0]:data_p3[1]], 3)
        #partition 4
        datap4 = const_mbr+const_partition*3, const_mbr+const_partition*4
        self.mbr_partition_4 = Partition().deserialize_partition(data[datap4[0]:datap4[1]], 4)
        return self


#-------------------PARTITION-------------------
class Partition:
    def __init__(self) -> None:
        self.FORMATPARTITION = '3c2I16s' # 1 char, 1 char, 2 int unsigned, 16 char
        self.part_status = b'\0' # 1 byte tipo char
        self.part_type = b'\0' # 1 byte tipo char
        self.part_fit = b'\0' # 1 byte tipo char
        self.part_start = 0 # 4 bytes tipo int
        self.part_size = 0 # 4 bytes tipo int
        self.part_name = b'\0'* 16 # 16 bytes char[16]    

    def setValues(self, part_status, part_type, part_fit, part_start, part_size, part_name):
        fns = fn()
        self.part_status = fns.string_to_bytes(part_status)
        self.part_type = fns.string_to_bytes(part_type)
        self.part_fit = fns.string_to_bytes(part_fit)
        self.part_start = part_start
        self.part_size = part_size
        self.part_name = fns.string_to_bytes(part_name)

    def serialize_partition(self):
        return fn().serialize(self.FORMATPARTITION, self.part_status, self.part_type, self.part_fit, self.part_start, self.part_size, self.part_name)

    def deserialize_partition(self, data, num_partition = 1):
        partiontion_data = fn().deserialize(self.FORMATPARTITION, data)
        if partiontion_data is None:
            fn().err_msg("PARTITION", "No se pudo deserializar la partición" + str(num_partition))
            return self
        self.part_status = partiontion_data[0]
        self.part_type = partiontion_data[1]
        self.part_fit = partiontion_data[2]
        self.part_start = partiontion_data[3]
        self.part_size = partiontion_data[4]
        self.part_name = partiontion_data[5]
        return self
    
#-------------------EBR-------------------
class EBR:
    def __init__(self) -> None:
        self.FORMATEBR = '3c2I16s' # 1 char, 1 char, 2 int unsigned, 16 char
        self.part_status = '\0' # 1 byte tipo char
        self.part_fit = '\0' # 1 byte tipo char
        self.part_start = '\0'* 4 # 4 bytes tipo int
        self.part_size = '\0'* 4 # 4 bytes tipo int
        self.part_next = '-1'* 4 # 4 bytes tipo int
        self.part_name = '\0'* 16 # 16 bytes char[16]    

    def setValues(self, part_status, part_fit, part_start, part_size, part_next, part_name):
        fns = fn()
        self.part_status = fns.string_to_bytes(part_status)
        self.part_fit = fns.string_to_bytes(part_fit)
        self.part_start = part_start
        self.part_size = part_size
        self.part_next = part_next
        self.part_name = fns.string_to_bytes(part_name)

    def serialize_ebr(self):
        return fn().serialize(self.FORMATEBR, self.part_status, self.part_fit, self.part_start, self.part_size, self.part_next, self.part_name)

    def deserialize_ebr(self, data):
        return fn().deserialize(self.FORMATEBR, data)    