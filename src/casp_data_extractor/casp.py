import enum


class Metrics(enum.IntEnum):
    """
    Enum for CASP metrics.
    """
    N1 = 0
    N2 = 1
    DIST = 2
    N = 3
    RMSD = 4
    GDT_TS = 5
    LGA_S3 = 6
    LGA_Q = 7


class Model:
  """Class for representing a CASP model."""
  def __init__(self, metrics: dict[Metrics, float]):
    self.metrics: dict[Metrics, float] = metrics


class Group:
  """Class for representing a CASP group."""
  def __init__(self, models: dict[str, list[Model]]):
    self.models: dict[str, list[Model]] = models


class Casp:
  """Class for representing a CASP dataset."""
  def __init__(self, name: str, data_url: str, targets: list[str], groups: dict[str, Group]):
    self.name: str = name
    self.data_url: str = data_url
    self.targets: list[str] = targets
    self.groups: dict[str, Group] = groups
    self.winner = None
    self.metric = [tmp_metric for tmp_metric in Metrics]

  def calculate_winner(self):
    raise NotImplementedError()
