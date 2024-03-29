from src.Functions import Functions as fn
import struct
class MBR:
    def __init__(self, arr_output_result) -> None:
        self.arr_output_result = arr_output_result
        self.FORMATMBR = '3Ic' # 4 int y 1 char
        self.mbr_tamano = 0 # 4 bytes tipo int
        self.mbr_time_stamp = 0 # 4 bytes tipo int
        self.mbr_disk_signature = 0 # 4 bytes tipo int
        self.mbr_disk_fit = '0' # 1 byte tipo char
        self.mbr_partition_1 = Partition([])
        self.mbr_partition_2 = Partition([])
        self.mbr_partition_3 = Partition([])
        self.mbr_partition_4 = Partition([])
    
    def setValues(self, mbr_tamano, disk_signature, mbr_disk_fit):
        self.mbr_tamano = mbr_tamano
        self.mbr_time_stamp = fn(self.arr_output_result).get_time_stamp_now()
        self.mbr_disk_signature = disk_signature
        self.mbr_disk_fit = mbr_disk_fit
        self.mbr_partition_1 = Partition(self.arr_output_result)
        self.mbr_partition_2 = Partition(self.arr_output_result)
        self.mbr_partition_3 = Partition(self.arr_output_result)
        self.mbr_partition_4 = Partition(self.arr_output_result)

    def serialize_mbr(self):
        fns = fn(self.arr_output_result)
        bytesMBR = fns.serialize(self.FORMATMBR, self.mbr_tamano,  fns.get_time_stamp(self.mbr_time_stamp), self.mbr_disk_signature, fns.string_to_bytes(self.mbr_disk_fit))
        return bytesMBR + self.mbr_partition_1.serialize_partition() + self.mbr_partition_2.serialize_partition() + self.mbr_partition_3.serialize_partition() + self.mbr_partition_4.serialize_partition()
    
    def deserialize_mbr(self, data):
        const_mbr = struct.calcsize(self.FORMATMBR)
        const_partition = struct.calcsize(self.mbr_partition_1.FORMATPARTITION)
        fns = fn(self.arr_output_result)
        bytesMBR = fns.deserialize(self.FORMATMBR, data[:const_mbr])
        if bytesMBR is None:
            # fns.err_msg("MBR", "No se pudo deserializar el MBR")
            self.arr_output_result.append("No se pudo deserializar el MBR")
            return None
        self.mbr_tamano = bytesMBR[0]
        self.mbr_time_stamp = fns.get_time_stamp_obj(bytesMBR[1])
        self.mbr_disk_signature = bytesMBR[2]
        self.mbr_disk_fit = fns.bytes_to_string(bytesMBR[3])
        #partition 1
        data_p1 = const_mbr,  const_mbr+const_partition
        self.mbr_partition_1 = Partition(self.arr_output_result).deserialize_partition(data[data_p1[0]:data_p1[1]], 1)
        #partition 2
        data_p2 = const_mbr+const_partition, const_mbr+const_partition*2
        self.mbr_partition_2 = Partition(self.arr_output_result).deserialize_partition(data[data_p2[0]:data_p2[1]], 2)
        #partition 3
        data_p3 = const_mbr+const_partition*2, const_mbr+const_partition*3
        self.mbr_partition_3 = Partition(self.arr_output_result).deserialize_partition(data[data_p3[0]:data_p3[1]], 3)
        #partition 4
        datap4 = const_mbr+const_partition*3, const_mbr+const_partition*4
        self.mbr_partition_4 = Partition(self.arr_output_result).deserialize_partition(data[datap4[0]:datap4[1]], 4)
        return self


#-------------------PARTITION-------------------
class Partition:
    def __init__(self, arr_output_result) -> None:
        self.arr_output_result = arr_output_result
        self.FORMATPARTITION = '3c2I16s' # 1 char, 1 char, 2 int unsigned, 16 char
        self.part_status = '\0' # 1 byte tipo char
        self.part_type = '\0' # 1 byte tipo char
        self.part_fit = '\0' # 1 byte tipo char
        self.part_start = 0 # 4 bytes tipo int
        self.part_size = 0 # 4 bytes tipo int
        self.part_name = '\0'* 16 # 16 bytes char[16]    

    def setValues(self, part_status, part_type, part_fit, part_start, part_size, part_name):
        self.part_status = part_status
        self.part_type = part_type
        self.part_fit = part_fit
        self.part_start = part_start
        self.part_size = part_size
        self.part_name = part_name.truncate(16)

    def serialize_partition(self):
        fns = fn(self.arr_output_result)
        return fn(self.arr_output_result).serialize(self.FORMATPARTITION, fns.string_to_bytes(self.part_status), fns.string_to_bytes(self.part_type), fns.string_to_bytes(self.part_fit), self.part_start, self.part_size, fns.string_to_bytes(self.part_name))

    def deserialize_partition(self, data, num_partition = 1):
        fns = fn(self.arr_output_result)
        partiontion_data = fns.deserialize(self.FORMATPARTITION, data)
        if partiontion_data is None:
            # fn(self.arr_output_result).err_msg("PARTITION", "No se pudo deserializar la partición" + str(num_partition))
            self.arr_output_result.append("No se pudo deserializar la partición" + str(num_partition))
            return self
        
        if partiontion_data[1] == b'\x00' and partiontion_data[2] == b'\x00' and partiontion_data[3] == 0:
            self.part_status = '\0'
            self.part_type = '\0'
            self.part_fit = '\0'
            self.part_start = 0
            self.part_size = 0
            self.part_name = '\0'* 16
            return self

        self.part_status = fns.bytes_to_string(partiontion_data[0])
        self.part_type = fns.bytes_to_string(partiontion_data[1])
        self.part_fit = fns.bytes_to_string(partiontion_data[2])
        self.part_start = partiontion_data[3]
        self.part_size = partiontion_data[4]
        self.part_name = fns.bytes_to_string(partiontion_data[5])
        return self
    
#-------------------EBR-------------------
class EBR:
    def __init__(self, arr_output_result) -> None:
        self.arr_output_result = arr_output_result
        self.FORMATEBR = '2c2Ii16s' # 1 char, 1 char, 2 int unsigned, 16 char
        self.ebr_status = '\0' # 1 byte tipo char
        self.ebr_fit = '\0' # 1 byte tipo char
        self.ebr_start = 0 # 4 bytes tipo int
        self.ebr_size = 0 # 4 bytes tipo int
        self.ebr_next = -1 # 4 bytes tipo int
        self.ebr_name = '\0'*16 # 16 bytes char[16]    

    def setValues(self, ebr_status, ebr_fit, ebr_start, ebr_size, ebr_next, ebr_name):
        self.ebr_status = ebr_status
        self.ebr_fit = ebr_fit
        self.ebr_start = ebr_start
        self.ebr_size = ebr_size
        self.ebr_next = ebr_next
        self.ebr_name = ebr_name.truncate(16)

    def serialize_ebr(self):
        fns = fn(self.arr_output_result)
        return fns.serialize(self.FORMATEBR, fns.string_to_bytes(self.ebr_status), fns.string_to_bytes(self.ebr_fit
        ), self.ebr_start, self.ebr_size, self.ebr_next, fns.string_to_bytes(self.ebr_name))

    def deserialize_ebr(self, data):
        dataebr = fn(self.arr_output_result).deserialize(self.FORMATEBR, data)
        if dataebr is None:
            # fn(self.arr_output_result).err_msg("EBR", "No se pudo deserializar el EBR")
            self.arr_output_result.append("No se pudo deserializar el EBR")
            return self
        
        if dataebr[0] == b'\x00' and dataebr[1] == b'\x00' and dataebr[2] == 0 and dataebr[3] == 0 and dataebr[4] == -1:
            self.ebr_status = '\0'
            self.ebr_fit = '\0'
            self.ebr_start = 0
            self.ebr_size = 0
            self.ebr_next = -1
            self.ebr_name = '\0'*16
            return self

        self.ebr_status = fn(self.arr_output_result).bytes_to_string(dataebr[0])
        self.ebr_fit = fn(self.arr_output_result).bytes_to_string(dataebr[1])
        self.ebr_start = dataebr[2]
        self.ebr_size = dataebr[3]
        self.ebr_next = dataebr[4]
        self.ebr_name = fn(self.arr_output_result).bytes_to_string(dataebr[5])
        return self    