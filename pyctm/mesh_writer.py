import struct

RAW_COMPRESSION = 0x00574152
FILE_FORMAT_VERSION = 5

class MeshWriter(object):
  def __init__(self, mesh, out):
    self.mesh = mesh
    self.out = out

  def write_header(self):
    self.out.write(bytearray('OCTM'))
    self.out.write(struct.pack('i', FILE_FORMAT_VERSION))
    self.out.write(struct.pack('i', RAW_COMPRESSION))
    self.out.write(struct.pack('i', len(self.mesh.vertices)))
    self.out.write(struct.pack('i', len(self.mesh.indexes) / 3))
    self.out.write(struct.pack('i', 0 if not self.mesh.uv else len(self.mesh.uv)))
    self.out.write(struct.pack('i', len(self.mesh.attributes)))
    boolean_flags = 0
    self.out.write(struct.pack('i', boolean_flags))
    self.write_string(self.mesh.comments)

  def write_string(self, string):
    encoded = string.encode('utf-8')
    self.out.write(struct.pack('i', len(encoded)))
    self.out.write(bytearray(encoded))
