class Mesh(object):
  def __init__(self, vertices, indexes, normals=[], uv=[], attributes=[]):
    self.vertices = tuple(vertices)
    self.indexes = tuple(indexes)
    self.normals = tuple(normals)
    self.uv = tuple(uv)
    self.attributes = tuple(attributes)
    self.comments = ''
