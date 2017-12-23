import unittest
import StringIO
import struct

from pyctm import mesh
from pyctm import mesh_writer

def unpack_one(format, string):
  return struct.unpack(format, string)[0]

VERTICES = [
  [0, 0, 0],
  [1, 1, 1],
  [2, 2, 2],
  [3, 3, 3],
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
    self.assertEqual(unpack_one('i', value[4:8]), 5)
    self.assertEqual(unpack_one('i', value[8:12]), 0x00574152)
    self.assertEqual(unpack_one('i', value[12:16]), 4)
    self.assertEqual(unpack_one('i', value[16:20]), 2)
    self.assertEqual(unpack_one('i', value[20:24]), 4)
    self.assertEqual(unpack_one('i', value[24:28]), 1)
    self.assertEqual(unpack_one('i', value[28:32]), 0)
    self.assertEqual(unpack_one('i', value[32:36]), 0)

  def testWriteHeaderMissingOptionalFields(self):

    m = mesh.Mesh(VERTICES, INDEXES)
    out = StringIO.StringIO()
    w = mesh_writer.MeshWriter(m, out)

    w.write_header()
    value = out.getvalue()
    out.close()

    self.assertEqual(len(value), 36)
    self.assertEqual(value[:4], 'OCTM')
    self.assertEqual(unpack_one('i', value[4:8]), 5)
    self.assertEqual(unpack_one('i', value[8:12]), 0x00574152)
    self.assertEqual(unpack_one('i', value[12:16]), 4)
    self.assertEqual(unpack_one('i', value[16:20]), 2)
    self.assertEqual(unpack_one('i', value[20:24]), 0)
    self.assertEqual(unpack_one('i', value[24:28]), 0)
    self.assertEqual(unpack_one('i', value[28:32]), 0)
    self.assertEqual(unpack_one('i', value[32:36]), 0)



if __name__ == '__main__':
  unittest.main()
