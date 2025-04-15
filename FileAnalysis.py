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
      DoseBelowDetection: bool = False

class StaffMember():
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.doses = []



class LoadedData():
      def __init__(self, file):
            self.data = pd.read_excel(file)
            self.staff = {}
            self.warningMessages = []
            # Iterate over each row in the DataFrame
            for index, row in self.data.iterrows():
                  if row.isnull().all():
                        self.warningMessages.append(f"Skipping empty row {index + 2}")
                        continue
                  
                  FirstName = row.get("First name", None)
                  SurName = row.get("Surname", None)  
                  email = row.get("Email address of staff member", None)  

                  if pd.isna(FirstName):
                        self.warningMessages.append(f"First name is missing in row {index + 2}, Skipping entire data row")
                        continue
                  if pd.isna(SurName):
                        self.warningMessages.append(f"Surname is missing in row {index + 2}, Skipping entire data row")
                        continue
                  if pd.isna(email):
                        self.warningMessages.append(f"Email is missing in row {index + 2}, Skipping entire data row")
                        continue

                  name = FirstName + " " + SurName
                  if email not in self.staff:
                        self.staff[email] = StaffMember(name, email)
                  try:

                        def ConvertDose(Dose):
                              if Dose == "M":
                                    return 0,True
                              else:      
                                    return float(Dose),False

                        #Get all the doses and add them in for this entry.
                        WholeBodyBadge = row.get("Is a whole body/chest dosimeter worn?", "No")
                        if WholeBodyBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date", None)
                              EndDate = row.get("Enter dosimeter end date", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response", None)
                              Employer = row.get("Enter employer where this dose was received", None)
                              
                              NaNFound = self.CheckForNaN(index,"whole body",StartDate, EndDate, Dose, Employer,"")
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Chest, Dose, Employer,None,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)
                        
                        CollarBadge = row.get("Is a collar dosimeter worn?", "No")
                        if CollarBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date1", None)
                              EndDate = row.get("Enter dosimeter end date1", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response1", None)
                              Employer = row.get("Enter employer where this dose was received1", None)
                              
                              NaNFound = self.CheckForNaN(index,"collar badge",StartDate, EndDate, Dose, Employer,"")
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Collar, Dose, Employer,None,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)

                  
                        EyeBadge = row.get("Is a eye badge worn?", "No")
                        if EyeBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date2", None)
                              EndDate = row.get("Enter dosimeter end date2", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response2", None)
                              Employer = row.get("Enter employer where this dose was received2", None)

                              NaNFound = self.CheckForNaN(index,"eye badge",StartDate, EndDate, Dose, Employer,"")
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.Eye, Dose, Employer,None,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)
                        
                        LeftExtremBadge = row.get("Is a left extremity dosimeter worn?", "No")
                        if LeftExtremBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date3", None)
                              EndDate = row.get("Enter dosimeter end date3", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response3", None)
                              Employer = row.get("Enter employer where this dose was received3", None)

                              NaNFound = self.CheckForNaN(index,"left extremity badge",StartDate, EndDate, Dose, Employer,"")
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.LeftExtremity, Dose, Employer,None,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)

                        RightExtremBadge = row.get("Is a right extremity dosimeter worn?", "No")
                        if RightExtremBadge =="Yes":
                              StartDate = row.get("Enter dosimeter start date4", None)
                              EndDate = row.get("Enter dosimeter end date4", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response4", None)
                              Employer = row.get("Enter employer where this dose was received4", None)

                              NaNFound = self.CheckForNaN(index,"right extremity badge",StartDate, EndDate, Dose, Employer,"")
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.RightExtremity, Dose, Employer,None,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)

                        OtherBadge = row.get("Are any other dosimeter types not already mentioned worn?", "No")
                        if OtherBadge =="Yes":

                              StartDate = row.get("Enter dosimeter start date5", None)
                              EndDate = row.get("Enter dosimeter end date5", None)
                              Dose = row.get("Enter dose measured (in mSv) Note: Units do not have to provided in the response5", None)
                              Employer = row.get("Enter employer where this dose was received5", None)
                              Custom_Badge = row.get("Please provide the dosimeter wear location", None)

                              NaNFound = self.CheckForNaN(index,"other badge",StartDate, EndDate, Dose, Employer,Custom_Badge)
                              if NaNFound==False:
                                    Dose, IsItM = ConvertDose(Dose)
                                    DoseRecord = RecordedDose(StartDate, EndDate, BadgeType.OtherType, Dose, Employer,Custom_Badge,DoseBelowDetection=IsItM)
                                    self.staff[email].doses.append(DoseRecord)
                  except Exception as e:
                        print(str(e))
                        raise Exception(f"Error processing row {index+2} {e}")
                  
            #Check for when there is no dose recorded
            KeysToRemove = []
            for staff in self.staff.values():
                  if len(staff.doses) == 0:
                        self.warningMessages.append(f"No doses recorded for {staff.name} ({staff.email}), removing data entry")
                        KeysToRemove.append(staff.email)
            self.staff = {key: value for key, value in self.staff.items() if key not in KeysToRemove}
                  
                  
                  
            
      def CheckForNaN(self, index, BadgeType, StartDate, EndDate, Dose, Employer, Custom_Badge):
            NaNData = False
            if pd.isna(StartDate):
                  self.warningMessages.append(f"Start date for "+BadgeType+" is missing in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True
            if pd.isna(EndDate):
                  self.warningMessages.append(f"End date for "+BadgeType+" is missing in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True
            if pd.isna(Dose):
                  self.warningMessages.append(f"Dose for "+BadgeType+" is missing in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True
            if pd.isna(Employer):   
                  self.warningMessages.append(f"Employer for "+BadgeType+" is missing in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True
            if pd.isna(Custom_Badge):     
                  self.warningMessages.append(f"Custom badge location is missing in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True

            #Detects Incompatible Dates
            if not isinstance(StartDate, datetime.datetime):
                  self.warningMessages.append(f"Start date for "+BadgeType+" is not a valid date in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True
            if not isinstance(EndDate, datetime.datetime):
                  self.warningMessages.append(f"End date for "+BadgeType+" is not a valid date in row "+str(index + 2)+", Skipping data entry")
                  NaNData=True


            KnownLetters = ["U", "O", "A","u", "o", "a"]
            for letter in KnownLetters:
                  if Dose == letter:
                        self.warningMessages.append(f"Dose for "+BadgeType+" is set as "+letter+" in row "+str(index + 2)+", Skipping data entry")
                        NaNData=True

            return NaNData