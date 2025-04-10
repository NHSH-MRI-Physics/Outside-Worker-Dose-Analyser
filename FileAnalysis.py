import pandas as pd
from dataclasses import dataclass
import datetime
from enum import Enum

class BadgeType(Enum):
      Chest=1
      Collar=2
      Eye=3
      LeftExtremity=4
      RightExtremity=5
      OtherType=6

@dataclass
class RecordedDose:
      StartDate: datetime
      EndDate: datetime
      Badge: BadgeType
      Dose: float

class StaffMember():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.doses = []
    

class LoadedData():
        def __init__(self, file):
            self.data = pd.read_excel(file)
            self.staff = {}