import sys
sys.path.append('/Users/azis/pyctm')
import unittest
import StringIO
import struct

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



  def testWriteHeader(self):
    m = mesh.Mesh(VERTICES, INDEXES, UV, ATTRIBUTES)
    out = StringIO.StringIO()
    w = mesh_writer.MeshWriter(m, out)

    w.write_header()
    value = out.getvalue()
    out.close()

    self.assertEqual(len(value), 36)
    self.assertEqual(value[:4], 'OCTM')
    self.assertEqual(read_int(value, 4), 5)
    self.assertEqual(read_int(value, 8), 0x00574152)
    self.assertEqual(read_int(value, 12), 4)
    self.assertEqual(read_int(value, 16), 2)
    self.assertEqual(read_int(value, 20), 4)
    self.assertEqual(read_int(value, 24), 1)
    self.assertEqual(read_int(value, 28), 0)
    self.assertEqual(read_int(value, 32), 0)

  def testWriteHeaderMissingOptionalFields(self):
    m = mesh.Mesh(VERTICES, INDEXES)
    out = StringIO.StringIO()
    w = mesh_writer.MeshWriter(m, out)

    w.write_header()
    value = out.getvalue()
    out.close()

    self.assertEqual(len(value), 36)
    self.assertEqual(value[:4], 'OCTM')
    self.assertEqual(read_int(value, 4), 5)
    self.assertEqual(read_int(value, 8), 0x00574152)
    self.assertEqual(read_int(value, 12), 4)
    self.assertEqual(read_int(value, 16), 2)
    self.assertEqual(read_int(value, 20), 0)
    self.assertEqual(read_int(value, 24), 0)
    self.assertEqual(read_int(value, 28), 0)
    self.assertEqual(read_int(value, 32), 0)

  def testWriteBody(self):
    m = mesh.Mesh(VERTICES, INDEXES, UV, ATTRIBUTES)
    out = StringIO.StringIO()
    w = mesh_writer.MeshWriter(m, out)

    w.write_body()
    value = out.getvalue()
    out.close()

    self.assertEqual(value[0:4], 'INDX')
    self.assertEqual(read_int(value, 4), 0)
    self.assertEqual(read_int(value, 8), 1)
    self.assertEqual(read_int(value, 12), 2)
    self.assertEqual(read_int(value, 16), 1)
    self.assertEqual(read_int(value, 20), 2)
    self.assertEqual(read_int(value, 24), 3)

    self.assertEqual(value[28:32], 'VERT')
    self.assertAlmostEquals(read_float(value, 32), 0.0, places=1)
    self.assertAlmostEquals(read_float(value, 36), 0.1, places=1)
    self.assertAlmostEquals(read_float(value, 40), 0.2, places=1)

    self.assertAlmostEquals(read_float(value, 44), 1.1, places=1)
    self.assertAlmostEquals(read_float(value, 48), 1.2, places=1)
    self.assertAlmostEquals(read_float(value, 52), 1.3, places=1)

    self.assertAlmostEquals(read_float(value, 56), 2.2, places=1)
    self.assertAlmostEquals(read_float(value, 60), 2.3, places=1)
    self.assertAlmostEquals(read_float(value, 64), 2.4, places=1)

    self.assertAlmostEquals(read_float(value, 68), 3.3, places=1)
    self.assertAlmostEquals(read_float(value, 72), 3.4, places=1)
    self.assertAlmostEquals(read_float(value, 76), 3.5, places=1)

    self.assertIsNotNone(value)


if __name__ == '__main__':
  unittest.main()
