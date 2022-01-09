import struct

class NamedFileStruct:
    endian = '<'
    fields = None
    offset = None
    def __init__(self, fileobj, offset = None, endian = None, **fields):
        self.struct = None
        self.read(fileobj, offset, endian, **fields)
    def read_bytes(self, fileobj = None, offset = None, endian = None, **fields):
        if fileobj is not None:
            self.fileobj = fileobj
        if offset is not None:
            self.offset = offset
        if endian is not None:
            self.endian = endian
        if len(fields):
            self.fields = fields
            self.struct = None
        if self.struct is None:
            self.struct = struct.Struct(self.endian + ''.join(self.fields.values()))
        if self.offset is not None:
            self.fileobj.seek(self.offset)
        return self.fileobj.read(self.struct.size)
    def read(self, fileobj = None, offset = None, endian = None, **fields):
        bytes = self.read_bytes(fileobj, offset, endian, **fields)
        self.values = {
            key : val
            for key, val in zip(
                self.fields.keys(), 
                self.struct.unpack(bytes)
            )
        }
    def __getattr__(self, name):
        return self.values[name]
