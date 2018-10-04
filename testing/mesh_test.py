import io
import unittest
import struct
import sys

from pyctm import mesh
from pyctm import uv_map
from pyctm import attribute_map
from pyctm import mesh_writer


class BufferReader(object):
  def __init__(self, buffer):
    self.buffer = buffer

  def seek(self, position):
    self.buffer.seek(position)

  def read_int(self):
    result = struct.unpack('i', self.buffer.read(4))[0]
    return result

  def read_float(self):
    result = struct.unpack('f', self.buffer.read(4))[0]
    return result

  def read_string(self, size):
    result = self.buffer.read(size).decode('ASCII')
    return result


VERTICES = [
  [0.0, 0.1, 0.2],
  [1.1, 1.2, 1.3],
  [2.2, 2.3, 2.4],
  [3.3, 3.4, 3.5],
]
INDEXES = [0, 1, 2, 1, 2, 3]
NORMALS = [
  [1.0, 0.0, 0.0],
  [0.0, 1.0, 0.0],
  [0.0, 0.0, 1.0],
  [0.4, -0.7, 0.5],
]
COORDS_UV_MAP_0  = [
    [0.0, 0.0],
    [0.1, 0.1],
    [0.2, 0.2],
    [0.3, 0.3],
]
COORDS_UV_MAP_1  = [
    [0.1, 0.5],
    [0.3, 0.2],
    [-0.7, 0.3],
    [0.4, 0.3],
]
UV_MAPS = [
  uv_map.UvMap(coords=COORDS_UV_MAP_0, name='map_0', texture_file_name='tex0.png'),
  uv_map.UvMap(coords=COORDS_UV_MAP_1, name='another_map', texture_file_name='t1.png'),
]
ATTRIBUTES_0 = [
  [1, 2, 3, 4],
  [8, 7, 6, 5],
  [10, 15, 20, 25],
  [400, 200, 100, 300],
]
ATTRIBUTES_1 = [
  [15, 14, 13, 12],
  [11, 10, 9, 8],
  [7, 6, 5, 4],
  [3, 2, 1, 0],
]
ATTRIBUTES_2 = [
  [0, 4, 8, 12],
  [1, 5, 9, 13],
  [2, 6, 10, 14],
  [3, 7, 11, 15],
]
ATTRIBUTE_MAPS = [
  attribute_map.AttributeMap(values=ATTRIBUTES_0, name='attr0'),
  attribute_map.AttributeMap(values=ATTRIBUTES_1, name='a1'),
  attribute_map.AttributeMap(values=ATTRIBUTES_2, name='attributes2'),
]


class MeshTest(unittest.TestCase):

  def testWritesHeader(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES, uv_maps=UV_MAPS, attribute_maps=ATTRIBUTE_MAPS)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)

    with io.BytesIO() as out:
      writer.write(test_mesh, out)
      out.seek(0)
      reader = BufferReader(out)

      self.assertEqual(reader.read_int(), 0x4d54434f)  # 'OCTM' in ASCII
      self.assertEqual(reader.read_int(), 5)  # version
      self.assertEqual(reader.read_int(), 0x00574152)  # compression method
      self.assertEqual(reader.read_int(), 4)  # vertex count
      self.assertEqual(reader.read_int(), 2)  # triangle count
      self.assertEqual(reader.read_int(), 2)  # UV map count
      self.assertEqual(reader.read_int(), 3)  # attribute map count
      self.assertEqual(reader.read_int(), 0)  # boolean flags
      self.assertEqual(reader.read_int(), 0)  # comment length

  def testWritesHeaderMissingOptionalFields(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)

    with io.BytesIO() as out:
      writer.write(test_mesh, out)
      reader = BufferReader(out)

      out.seek(0)
      self.assertEqual(reader.read_int(), 0x4d54434f)  # 'OCTM' in ASCII
      self.assertEqual(reader.read_int(), 5)  # version
      self.assertEqual(reader.read_int(), 0x00574152)  # compression method
      self.assertEqual(reader.read_int(), 4)  # vertex count
      self.assertEqual(reader.read_int(), 2)  # triangle count
      self.assertEqual(reader.read_int(), 0)  # UV map count
      self.assertEqual(reader.read_int(), 0)  # attribute map count
      self.assertEqual(reader.read_int(), 0)  # boolean flags
      self.assertEqual(reader.read_int(), 0)  # comment length

  def testWritesBody(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES, normals=NORMALS, uv_maps=UV_MAPS, attribute_maps=ATTRIBUTE_MAPS)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)
    body_index = 36 + 0  # 36 + comment length

    with io.BytesIO() as out:
      writer.write(test_mesh, out)
      reader = BufferReader(out)

      reader.seek(body_index)
      # Indexes
      self.assertEqual(reader.read_int(), 0x58444e49)  # 'INDX'
      self.assertEqual(reader.read_int(), INDEXES[0])
      self.assertEqual(reader.read_int(), INDEXES[1])
      self.assertEqual(reader.read_int(), INDEXES[2])
      self.assertEqual(reader.read_int(), INDEXES[3])
      self.assertEqual(reader.read_int(), INDEXES[4])
      self.assertEqual(reader.read_int(), INDEXES[5])

      # Vertices
      self.assertEqual(reader.read_int(), 0x54524556)  # 'VERT'
      self.assertAlmostEqual(reader.read_float(), 0.0, places=1)
      self.assertAlmostEqual(reader.read_float(), 0.1, places=1)
      self.assertAlmostEqual(reader.read_float(), 0.2, places=1)
      self.assertAlmostEqual(reader.read_float(), 1.1, places=1)
      self.assertAlmostEqual(reader.read_float(), 1.2, places=1)
      self.assertAlmostEqual(reader.read_float(), 1.3, places=1)
      self.assertAlmostEqual(reader.read_float(), 2.2, places=1)
      self.assertAlmostEqual(reader.read_float(), 2.3, places=1)
      self.assertAlmostEqual(reader.read_float(), 2.4, places=1)
      self.assertAlmostEqual(reader.read_float(), 3.3, places=1)
      self.assertAlmostEqual(reader.read_float(), 3.4, places=1)
      self.assertAlmostEqual(reader.read_float(), 3.5, places=1)

      # Normals
      self.assertEqual(reader.read_int(), 0x4d524f4e)  # 'NORM'
      self.assertAlmostEqual(reader.read_float(), NORMALS[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[0][2], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[1][2], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[2][2], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[3][1], places=1)
      self.assertAlmostEqual(reader.read_float(), NORMALS[3][2], places=1)

      # Textures
      self.assertEqual(reader.read_int(), 0x43584554)  # 'TEXC'
      self.assertEqual(reader.read_int(), 5) # length of 'map_0'
      self.assertEqual(reader.read_string(5), 'map_0')
      self.assertEqual(reader.read_int(), 8) # length of 'tex0.png'
      self.assertEqual(reader.read_string(8), 'tex0.png')
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_0[3][1], places=1)

      self.assertEqual(reader.read_int(), 0x43584554)  # 'TEXC'
      self.assertEqual(reader.read_int(), 11) # length of 'another_map'
      self.assertEqual(reader.read_string(11), 'another_map')
      self.assertEqual(reader.read_int(), 6) # length of 't1.png'
      self.assertEqual(reader.read_string(6), 't1.png')
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), COORDS_UV_MAP_1[3][1], places=1)

      self.assertEqual(reader.read_int(), 0x52545441)  # 'ATTR'
      self.assertEqual(reader.read_int(), 5) # length of 'attr0'
      self.assertEqual(reader.read_string(5), 'attr0')
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_0[3][1], places=1)
      self.assertEqual(reader.read_int(), 0x52545441)  # 'ATTR'
      self.assertEqual(reader.read_int(), 2) # length of 'a1'
      self.assertEqual(reader.read_string(2), 'a1')
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_1[3][1], places=1)
      self.assertEqual(reader.read_int(), 0x52545441)  # 'ATTR'
      self.assertEqual(reader.read_int(), 11) # length of 'attributes2'
      self.assertEqual(reader.read_string(11), 'attributes2')
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[0][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[0][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[1][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[1][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[2][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[2][1], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[3][0], places=1)
      self.assertAlmostEqual(reader.read_float(), ATTRIBUTES_2[3][1], places=1)


if __name__ == '__main__':
  unittest.main()
