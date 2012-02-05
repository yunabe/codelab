class Time(object):
  def __init__(self, hour, minute, second):
    self.__second = hour * 3600 + minute * 60 + second

  @property
  def hour(self):
    return self.__second / (60 * 60)

  @property
  def minute(self):
    return (self.__second / 60) % 60

  @property
  def second(self):
    return self.__second % 60

  def __str__(self):
    return '%02d:%02d:%02d' % (self.hour, self.minute, self.second)
