class Size:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        if self.value == None:
            return None
        return int(self.value)

class Path:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
        
    def get_value(self):
        if self.path == None:
            return ""
        return self.path + self.filename
    
class Fit:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        if self.value == None:
            return None
        return str.upper(self.value) #return value in uppercase

class Unit:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        if self.value == None:
            return None
        return str.upper(self.value) #return value in uppercase

class ID:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        if self.value == None:
            return None
        return self.value

class Type:
    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        if self.value == None:
            return None
        return str.upper(self.value)

class Delete:
    def __init__(self, line, column, value=None):
        self.value = value
        self.line = line
        self.column = column

    def get_value(self):
        if self.value == None:
            return None
        return str.upper(self.value)                        
    
class Add:
    def __init__(self, line, column, value=None) -> None:
        self.value = value
        self.line = line
        self.column = column

    def get_value(self):
        if self.value == None:
            return None
        return int(self.value)     