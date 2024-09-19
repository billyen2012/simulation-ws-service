import csv
from typing import TypedDict

class ECG_ROW(TypedDict):
    c1: float
    c2: float
    c3: float
    c4: float
    c5: float
    c6: float
    c7: float
    c8: float
    c9: float
    c10: float
    c11: float
    c12: float
    c13: float
    c14: float
    c15: float
    c16: float
    c17: float
    c18: float
    c19: float

_data = None
def get_data()->list[ECG_ROW]:
  global _data
  if _data is not None:
    return _data
  with open('data.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      data = list()
      for row in reader:
        for key in row:
          row[key] = float(row[key])
        data.append(row)
      _data = data
      return _data