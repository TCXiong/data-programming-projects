race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

import json
import zipfile
import csv
import io # input/output

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
            
            
    def __repr__(self):
        info = list(self.race)
        return f"Applicant('{self.age}', {info})"
    
    def lower_age(self): 
        if("<" in self.age):
            return int(self.age.replace("<", "").split("-")[0])
        elif(">" in self.age):
            return int(self.age.replace(">", "").split("-")[0])
        else:
            return int(self.age.split("-")[0])
                 
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
    
class Loan:
    def __init__(self, fields):                                                 
        self.loan_amount = -1 if fields["loan_amount"] == "NA" or fields["loan_amount"] =="Exempt" else float(fields["loan_amount"])
        self.property_value = -1 if fields["property_value"] == "NA" or fields["property_value"] == "Exempt" else float(fields["property_value"])
        self.interest_rate = -1 if fields["interest_rate"] == "NA" or fields["interest_rate"] == "Exempt" else float(fields["interest_rate"])
        self.applicants = []
        # for applicant 1
        li = []
        for i in fields:
            if i[:-2]=="applicant_race":
                li.append(fields[i])                 
        self.applicants.append(Applicant(fields["applicant_age"],li))
        # for applicant 2
        li2 = []
        if fields["co-applicant_age"] != "9999":
            for i in fields:
                if i[:-2]=="co-applicant_race":
                    li2.append(fields[i])
            self.applicants.append(Applicant(fields["co-applicant_age"],li2)) 
            
    def __str__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {len(self.applicants)} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        # TODO: assert interest and amount are positive
        rate = self.interest_rate        
        amt = self.loan_amount

        while amt > 0:
            yield amt
            # TODO: add interest rate multiplied by amt to amt
            amt += amt*(rate/100)
            # TODO: subtract yearly payment from amt
            amt -= yearly_payment
                        
          
        
class Bank:
    def __init__(self, name):
        self.name = name
        self.lei = None
        self.LoanObj = list()
        self.values = None
        nameList = [];
        
        with open("banks.json") as f:
            data = json.load(f)
            for i in data:
                nameList.append(i.get("name"))                
            if self.name not in nameList:
                print("Data not exist!")
            self.lei = data[nameList.index(self.name)].get("lei")    
        #read csv from zip    
        zf = zipfile.ZipFile("wi.zip")
        f = zf.open("wi.csv") # ZipFile.open gives bytes
        reader = csv.DictReader(io.TextIOWrapper(f)) # DictReader wants strings
        values = dict()             
        for row in reader:           
            if self.lei == row["lei"]:
                values["loan_amount"]= row["loan_amount"]
                values["property_value"] = row["property_value"]
                values["interest_rate"] = row["interest_rate"]
                values["applicant_age"] = row["applicant_age"]                 
                for i in range(1,5):
                    values[f"applicant_race-{i}"] = row[f"applicant_race-{i}"]
                values["co-applicant_age"] = row["co-applicant_age"]
                for j in range(1, 5):
                    values[f"co-applicant_race-{j}"] = row[f"co-applicant_race-{j}"]                
                self.LoanObj.append(Loan(values))
            values = {}    
        f.close()
        zf.close()  
        
    #special methods
    def __getitem__(self, items):
        return self.LoanObj[items]
        
    def __len__(self):
        return len(self.LoanObj)
            
        # add lines here    
      