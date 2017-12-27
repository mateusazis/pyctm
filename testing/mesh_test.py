import unittest
import StringIO
import struct

from pyctm import mesh
from pyctm import mesh_writer

def unpack_one(format, string):
  return struct.unpack(format, string)[0]

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

  def testWriteBody(self):
    m = mesh.Mesh(VERTICES, INDEXES, UV, ATTRIBUTES)
    out = StringIO.StringIO()
    w = mesh_writer.MeshWriter(m, out)

    w.write_body()
    value = out.getvalue()
    out.close()

    self.assertEqual(value[0:4], 'INDX')
    self.assertEqual(unpack_one('I', value[4:8]), 0)
    self.assertEqual(unpack_one('I', value[8:12]), 1)
    self.assertEqual(unpack_one('I', value[12:16]), 2)
    self.assertEqual(unpack_one('I', value[16:20]), 1)
    self.assertEqual(unpack_one('I', value[20:24]), 2)
    self.assertEqual(unpack_one('I', value[24:28]), 3)

    self.assertEqual(value[28:32], 'VERT')
    self.assertAlmostEquals(unpack_one('f', value[32:36]), 0.0, places=1)
    self.assertAlmostEquals(unpack_one('f', value[36:40]), 0.1, places=1)
    self.assertAlmostEquals(unpack_one('f', value[40:44]), 0.2, places=1)

    self.assertAlmostEquals(unpack_one('f', value[44:48]), 1.1, places=1)
    self.assertAlmostEquals(unpack_one('f', value[48:52]), 1.2, places=1)
    self.assertAlmostEquals(unpack_one('f', value[52:56]), 1.3, places=1)

    self.assertAlmostEquals(unpack_one('f', value[56:60]), 2.2, places=1)
    self.assertAlmostEquals(unpack_one('f', value[60:64]), 2.3, places=1)
    self.assertAlmostEquals(unpack_one('f', value[64:68]), 2.4, places=1)

    self.assertAlmostEquals(unpack_one('f', value[68:72]), 3.3, places=1)
    self.assertAlmostEquals(unpack_one('f', value[72:76]), 3.4, places=1)
    self.assertAlmostEquals(unpack_one('f', value[76:80]), 3.5, places=1)

    self.assertIsNotNone(value)



if __name__ == '__main__':
  unittest.main()
