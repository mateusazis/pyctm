class UvMap(object):
  def __init__(self, coords=[], texture_file_name='', name=''):
    self.coords = tuple(coords)
    self.texture_file_name = texture_file_name
    self.name = name
