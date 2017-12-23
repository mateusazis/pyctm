class Mesh(object):
  def __init__(self, vertices, indexes, uv=None, attributes=[]):
    self.vertices = vertices
    self.indexes = indexes
    self.uv = uv
    self.attributes = attributes
    self.comments = ''
