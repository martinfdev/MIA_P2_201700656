from src.Primitive import ID, Type, FS
from src.Functions import Functions as fn
from src.Mount import Mount


class Mkfs:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._id = ""
        self._type = "FULL"
        self._fs = "2FS"
        self._tmp_mount_partition = None

    def execute_mkfs(self, list_mounts):
        if not self._set_values_props_mkfs():
            return
        if len(list_mounts) == 0:
            fn().err_msg("MKFS", "No hay particiones montadas.")
            return

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

    def _check_mount_partition(self, list_mounts):
        for mount in list_mounts:
            if isinstance(mount, Mount):
                if mount.id == self._id:
                    self._tmp_mount_partition = mount
                    return True
        return True
