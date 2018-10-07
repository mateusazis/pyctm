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
    out.write(struct.pack('i', len(mesh.vertices) // 3))
    out.write(struct.pack('i', len(mesh.indexes) // 3))
    out.write(struct.pack('i', 0 if not mesh.uv_maps else len(mesh.uv_maps)))
    out.write(struct.pack('i', len(mesh.attribute_maps)))
    boolean_flags = 0
    out.write(struct.pack('i', boolean_flags))
    self.write_string_(mesh.comments, out)

  def write_body_(self, mesh, out):
    if self.compression_method == CompressionMethod.RAW:
      self.write_body_raw_(mesh, out)
    else:
      # TODO: support other compression methods
      raise Exception('Compression method not implemented yet')

  def write_body_raw_(self, mesh, out):
    out.write(b'INDX')
    for index in mesh.indexes:
      out.write(struct.pack('i', index))

    out.write(b'VERT')
    for vertex_coord in mesh.vertices:
      out.write(struct.pack('f', vertex_coord))

    # Normals are optional, therefore check if there is any
    if mesh.normals:
      out.write(b'NORM')
      for normal_coord in mesh.normals:
        out.write(struct.pack('f', normal_coord))

    for uv_map in mesh.uv_maps:
      out.write(b'TEXC')
      self.write_string_(uv_map.name, out)
      self.write_string_(uv_map.texture_file_name, out)
      for uv_coord in uv_map.coords:
        out.write(struct.pack('f', uv_coord))

    for attribute_map in mesh.attribute_maps:
      out.write(b'ATTR')
      self.write_string_(attribute_map.name, out)
      for attribute_value in attribute_map.values:
        out.write(struct.pack('f', attribute_value))

  def write_string_(self, string, out):
    encoded = string.encode('utf-8')
    out.write(struct.pack('i', len(encoded)))
    out.write(bytearray(encoded))
