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
      Employer: str
      CustomBadge: str

class StaffMember():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.doses = []
    

class LoadedData():
        def __init__(self, file):
            self.data = pd.read_excel(file)
            self.staff = {}

            # Iterate over each row in the DataFrame
            for index, row in self.data.iterrows():

                  name = row.get("First name", "None") + " " + row.get("Surname", "None")  
                  email = row.get("Email address of staff member", None)  
                  if name and email:
                        if email not in self.staff:
                              self.staff[email] = StaffMember(name, email)
                  try:
                        #Get all the doses and add them in for this entry.
                        WholeBodyBadge = row.get("Is a whole body/chest dosimeter worn?", "No")
                        if WholeBodyBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date", None)
                              EndDate = row.get("Enter dosimeter end date", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response", None)
                              Employer = row.get("Enter employer where this dose was received", None)

                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None):
                                    raise Exception("Missing data for Whole Body Badge Fields")
                              Dose = float(Dose)
                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Chest, Dose, Employer,None)
                              self.staff[email].doses.append(DoseRecord)
                        
                        CollarBadge = row.get("Is a collar dosimeter worn?", "No")
                        if CollarBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date1", None)
                              EndDate = row.get("Enter dosimeter end date1", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response1", None)
                              Employer = row.get("Enter employer where this dose was received1", None)
                              
                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None):
                                    raise Exception("Missing data for Collar Badge Fields")
                              Dose = float(Dose)
                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Collar, Dose, Employer,None)
                              self.staff[email].doses.append(DoseRecord)
                  
                        EyeBadge = row.get("Is a eye badge worn?", "No")
                        if EyeBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date2", None)
                              EndDate = row.get("Enter dosimeter end date2", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response2", None)
                              Employer = row.get("Enter employer where this dose was received2", None)

                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None):
                                    raise Exception("Missing data for Eye Badge Fields")
                              Dose = float(Dose)
                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Eye, Dose, Employer,None)
                              self.staff[email].doses.append(DoseRecord)
                        
                        LeftExtremBadge = row.get("Is a left extremity dosimeter worn?", "No")
                        if LeftExtremBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date3", None)
                              EndDate = row.get("Enter dosimeter end date3", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response3", None)
                              Employer = row.get("Enter employer where this dose was received3", None)

                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None):
                                    raise Exception("Missing data for Left Extremity Badge Fields")
                              Dose = float(Dose)
                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.LeftExtremity, Dose, Employer,None)
                              self.staff[email].doses.append(DoseRecord)

                        RightExtremBadge = row.get("Is a right extremity dosimeter worn?", "No")
                        if RightExtremBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date4", None)
                              EndDate = row.get("Enter dosimeter end date4", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response4", None)
                              Employer = row.get("Enter employer where this dose was received4", None)

                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None):
                                    raise Exception("Missing data for Right Extremity Badge Fields")
                              Dose = float(Dose)
                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.RightExtremity, Dose, Employer,None)
                              self.staff[email].doses.append(DoseRecord)

                        OtherBadge = row.get("Are any other dosimeter types not already mentioned worn?", "No")
                        if OtherBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date5", None)
                              EndDate = row.get("Enter dosimeter end date5", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response5", None)
                              Employer = row.get("Enter employer where this dose was received5", None)
                              Custom_Badge = row.get("Please provide the dosimeter wear location", None)
                              Dose = float(Dose)
                              if (StartDate == None) or (EndDate == None) or (Dose == None) or (Employer == None) or (Custom_Badge == None):
                                    raise Exception("Missing data for Other Badge Fields")

                              DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.OtherType, Dose, Employer,Custom_Badge)
                              self.staff[email].doses.append(DoseRecord)
                  except Exception as e:
                        print(str(e))
                        raise Exception(f"Error processing row {index+1} {e}")
                  
                  break
