from src.Functions import Functions as fn
from src.Primitive import ID
class Unmount:
    def __init__(self, id) -> None:
        self._id = id

    def execute_unmount(self, list_mounts):
        if isinstance(self._id, ID):
            self._id = self._id.get_value()
        if not self._set_val_properties_unmount(list_mounts):
            fn().err_msg("Unmount", "No se pudo desmontar la partición "+str(self._id))
            return
        fn().success_msg("Unmount", "Se desmontó la partición "+str(self._id))
        return 
    
    #set and check properties for unmount
    def _set_val_properties_unmount(self, list_mounts):
        if self._id == "":
            fn().err_msg("Unmount", "No se encontró el parámetro -id")
            return False
        found = False
        for mount in list_mounts:
            if mount.id == self._id:
                list_mounts.remove(mount)
                found = True
                break
        if not found:
            fn().err_msg("Unmount", "No se encontró la partición "+str(self._id))
            return False
        return True