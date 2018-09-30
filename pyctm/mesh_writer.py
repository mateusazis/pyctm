import struct

FILE_FORMAT_VERSION = 5

class CompressionMethod(object):
  RAW = 0x00574152
  MG1 = 0x0031474d
  MG2 = 0x0032474d

class MeshWriter(object):

  def __init__(self, compression_method=CompressionMethod.RAW):
    self.compression_method = compression_method

  def write(self, mesh, out):
    self.write_header_(mesh, out)
    self.write_body_(mesh, out)

  def write_header_(self, mesh, out):
    out.write(b'OCTM')
    out.write(struct.pack('i', FILE_FORMAT_VERSION))
    out.write(struct.pack('i', CompressionMethod.RAW))
    out.write(struct.pack('i', len(mesh.vertices)))
    out.write(struct.pack('i', len(mesh.indexes) // 3))
    out.write(struct.pack('i', 0 if not mesh.uv else len(mesh.uv)))
    out.write(struct.pack('i', len(mesh.attributes)))
    boolean_flags = 0
    out.write(struct.pack('i', boolean_flags))
    self.write_string_(mesh.comments, out)

  def write_body_(self, mesh, out):
    if self.compression_method == CompressionMethod.RAW:
      self.write_body_raw_(mesh, out)

  def write_body_raw_(self, mesh, out):
    out.write(b'INDX')
    for index in mesh.indexes:
      out.write(struct.pack('I', index))

    out.write(b'VERT')
    for vertex in mesh.vertices:
      out.write(struct.pack('f', vertex[0]))
      out.write(struct.pack('f', vertex[1]))
      out.write(struct.pack('f', vertex[2]))

  def write_string_(self, string, out):
    encoded = string.encode('utf-8')
    out.write(struct.pack('i', len(encoded)))
    out.write(bytearray(encoded))
