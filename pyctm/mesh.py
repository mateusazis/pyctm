class Mesh(object):
  def __init__(self, vertices, indexes, normals=[], uv_maps=[], attributes=[]):
    self.vertices = tuple(vertices)
    self.indexes = tuple(indexes)
    self.normals = tuple(normals)
    self.uv_maps = tuple(uv_maps)
    self.attributes = tuple(attributes)
    self.comments = ''
