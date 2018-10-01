class Mesh(object):
  def __init__(self, vertices, indexes, normals=[], uv_maps=[], attribute_maps=[]):
    self.vertices = tuple(vertices)
    self.indexes = tuple(indexes)
    self.normals = tuple(normals)
    self.uv_maps = tuple(uv_maps)
    self.attribute_maps = tuple(attribute_maps)
    self.comments = ''
