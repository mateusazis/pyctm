import io
import unittest
import struct
import sys
sys.path.append('/Users/azis/pyctm')

from pyctm import mesh
from pyctm import mesh_writer


def read_int(bytestring, index):
  return struct.unpack('i', bytestring[index:index+4])[0]

def read_float(bytestring, index):
  return struct.unpack('f', bytestring[index:index+4])[0]


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
UV = [
  [0.0, 0.0],
  [0.1, 0.1],
  [0.2, 0.2],
  [0.3, 0.3],
]
ATTRIBUTES = [
  [1, 2, 3, 4]
]


class MeshTest(unittest.TestCase):


  def testWritesHeader(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES, uv=UV, attributes=ATTRIBUTES)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)
    out = io.BytesIO()

    writer.write(test_mesh, out)
    value = out.getvalue()
    out.close()

    # self.assertEqual(len(value), 36)
    self.assertEqual(read_int(value, 0), 0x4d54434f)  # 'OCTM' in ASCII
    self.assertEqual(read_int(value, 4), 5)  # version
    self.assertEqual(read_int(value, 8), 0x00574152)  # compression method
    self.assertEqual(read_int(value, 12), 4)  # vertex count
    self.assertEqual(read_int(value, 16), 2)  # triangle count
    self.assertEqual(read_int(value, 20), 4)  # UV map count
    self.assertEqual(read_int(value, 24), 1)  # attribute map count
    self.assertEqual(read_int(value, 28), 0)  # boolean flags
    self.assertEqual(read_int(value, 32), 0)  # comment length

  def testWritesHeaderMissingOptionalFields(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)
    out = io.BytesIO()

    writer.write(test_mesh, out)
    value = out.getvalue()
    out.close()

    self.assertEqual(read_int(value, 0), 0x4d54434f)  # 'OCTM' in ASCII
    self.assertEqual(read_int(value, 4), 5)  # version
    self.assertEqual(read_int(value, 8), 0x00574152)  # compression method
    self.assertEqual(read_int(value, 12), 4)  # vertex count
    self.assertEqual(read_int(value, 16), 2)  # triangle count
    self.assertEqual(read_int(value, 20), 0)  # UV map count
    self.assertEqual(read_int(value, 24), 0)  # attribute map count
    self.assertEqual(read_int(value, 28), 0)  # boolean flags
    self.assertEqual(read_int(value, 32), 0)  # comment length

  def testWritesBody(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)
    out = io.BytesIO()
    body_index = 36 + 0  # 36 + comment length

    writer.write(test_mesh, out)
    value = out.getvalue()
    out.close()

    self.assertEqual(read_int(value, body_index), 0x58444e49)  # 'INDX'
    self.assertEqual(read_int(value, body_index + 4), INDEXES[0])
    self.assertEqual(read_int(value, body_index + 8), INDEXES[1])
    self.assertEqual(read_int(value, body_index + 12), INDEXES[2])
    self.assertEqual(read_int(value, body_index + 16), INDEXES[3])
    self.assertEqual(read_int(value, body_index + 20), INDEXES[4])
    self.assertEqual(read_int(value, body_index + 24), INDEXES[5])

    self.assertEqual(read_int(value, body_index + 28), 0x54524556)  # 'VERT'
    self.assertAlmostEqual(read_float(value, body_index + 32), 0.0, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 36), 0.1, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 40), 0.2, places=1)

    self.assertAlmostEqual(read_float(value, body_index + 44), 1.1, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 48), 1.2, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 52), 1.3, places=1)

    self.assertAlmostEqual(read_float(value, body_index + 56), 2.2, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 60), 2.3, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 64), 2.4, places=1)

    self.assertAlmostEqual(read_float(value, body_index + 68), 3.3, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 72), 3.4, places=1)
    self.assertAlmostEqual(read_float(value, body_index + 76), 3.5, places=1)

  def testWritesBodyWithNormals(self):
    test_mesh = mesh.Mesh(VERTICES, INDEXES, normals=NORMALS)
    writer = mesh_writer.MeshWriter(mesh_writer.CompressionMethod.RAW)
    out = io.BytesIO()
    normal_index = 36 + 0 + 80  # 36 (header) + comment length + 80 (body up to vertices)

    writer.write(test_mesh, out)
    value = out.getvalue()
    out.close()

    self.assertEqual(read_int(value, normal_index), 0x4d524f4e)  # 'NORM'
    self.assertAlmostEqual(read_float(value, normal_index + 4), NORMALS[0][0], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 8), NORMALS[0][1], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 12), NORMALS[0][2], places=1)

    self.assertAlmostEqual(read_float(value, normal_index + 16), NORMALS[1][0], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 20), NORMALS[1][1], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 24), NORMALS[1][2], places=1)

    self.assertAlmostEqual(read_float(value, normal_index + 28), NORMALS[2][0], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 32), NORMALS[2][1], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 36), NORMALS[2][2], places=1)

    self.assertAlmostEqual(read_float(value, normal_index + 40), NORMALS[3][0], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 44), NORMALS[3][1], places=1)
    self.assertAlmostEqual(read_float(value, normal_index + 48), NORMALS[3][2], places=1)



if __name__ == '__main__':
  unittest.main()
