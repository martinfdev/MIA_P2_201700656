from src.Primitive import User, Pwd, ID
from src.Functions import Functions as fn
class Login:
    def __init__(self, list_params) -> None:
        self._list_params = list_params
        self._usr = ""
        self._pwd = ""
        self._id = ""
        self._tmp_mount = ""

    def execute_login(self, list_mounts):
        if not self._set_values_props_login():
            return
        if not self._find_partition(list_mounts):
            fn().err_msg("LOGIN", "La partición "+str(self._id)+" no está montada.")
            return

    def _set_values_props_login(self):
        for param in self._list_params:
            if isinstance(param, User):
                self._usr = param.value
            elif isinstance(param, Pwd):
                self._pwd = param.value
            elif isinstance(param, ID):
                self._id = param.value
        if self._usr == "":
            fn().err_msg("LOGIN", "No se ha especificado el -usr=? del usuario.")
            return False
        if self._pwd == "":
            fn().err_msg("LOGIN", "No se ha especificado el -pwd=? del usuario.")
            return False
        if self._id == "":
            fn().err_msg("LOGIN", "No se ha especificado el -id=? de la partición.")
            return False
        return True

    def _find_partition(self, list_mounts):
        for mount in list_mounts:
            if mount.id == self._id:
                self._tmp_mount = mount
                return True
        return False



