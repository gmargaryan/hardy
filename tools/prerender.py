import re
import sys

'''
The structure of the YAML file used for creation of yaml_data is

sections:
- section: ""
  descriptions:
  - description: ""

The example of description is 
"1.1.1 Ensure Logon Password is set (Scored)"

The idea is to take the description, and
1. If Scored, then score = 1
   If No Scored, then score = 0
2. Remove "(Scored)" or "(No Scored)" from the description
3. Create new key "name" with value created from the description with:
   - length <76
   - without \s
   - without numbers in the beginning
   if the description is 
     "1.1.1 Ensure Logon Password is set (Scored)"
   the name will be:
     "Ensure_Logon_Password_is_set"

  names should be unique. If we have a few same names we add _i in the end to make it unique.

'''

def name_score(yaml_data):

# This list is used to verify the uniqueness of the name.
  names_exist = []

  # Extract descriptions
  for sect_dict in yaml_data["sections"]:
    for descript in sect_dict["descriptions"]:
      description = descript['description']
      
      # Find numbers in the beginning, main part (used for the names creation) and scores
      match = re.search("^([0-9\.]+) (.+)\s+\((.*Scored)\)$", description)
      if match:
        
        # rule number 

        rule = match.group(1)        

        # score 

        score_ = match.group(3)

        if re.match("Not Scored", score_):
          score = 0
        elif re.match("Scored", score_): 
          score = 1
        else:
          print ("incorrect score value!")
          exit()

        # name

        string = match.group(2)
        # " " -> "_"
        name  = string.replace(" ", "_")
        # We want to restrict the length of the names (<76)
        name_short = name[:75] if len(name) > 75 else name
        # names whould be unique
        if name_short in names_exist:
          for i in range(1,10):
            name_short = (name_short + "_" + str()) if len(name) < 74 else (name_short[:73] + "_" + str(i))
            if name_short in names_exist:
              pass
            else:
              names_exist.append(name_short)
              i = 0
              break
          if (i == 10): 
            print ("There are too many same names (>10)!!")
            exit()
        else:
          names_exist.append(name_short)

        descript['name'] = name_short
        descript['score'] = score
        descript['rule'] = rule
        descript['description'] = match.group(1) + " " + string
      else:
        pass
  return (yaml_data)
