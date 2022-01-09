import struct

class NamedFileStruct:
    endian = '<'
    fields = None
    offset = None
    def __init__(self, fileobj, offset = None, endian = None, **fields):
        self.read(fileobj, offset, endian, **fields)
    def read(self, fileobj = None, offset = None, endian = None, **fields):
        if fileobj is not None:
            self.fileobj = fileobj
        if offset is not None:
            self.offset = offset
        if endian is not None:
            self.endian = endian
        if len(fields):
            self.fields = fields
            self.struct = struct.Struct(self.endian + ''.join(self.fields.values()))
        if self.offset is not None:
            self.fileobj.seek(self.offset)
        self.values = {
            key : val
            for key, val in zip(
                self._keys, 
                self.struct.iter_unpack(self.fileobj.read(len(self.struct)))
            )
        }
    def __getattr__(self, name):
        return self.values[name]
