# -*- coding: utf-8 -*-
__title__ = "InPlace-Hunter"
__doc__     = """Version = 1.0
Date    = 16.02.2026
________________________________________________________________
Description:
find all In-Place Elements in the project and create an interactive report to easily Select 

________________________________________________________________
How-To:
1. Step 1 = just click on the InPlace-Hunter button

________________________________________________________________
Last Updates:
- [01.01.2026] v1.0 Change Description
- [01.01.2026] v0.5 Change Description
- [01.01.2026] v0.1 Change Description 
________________________________________________________________
Author: Aurélien Orgeur tutored by Erik Frits (from LearnRevitAPI.com)"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
from Autodesk.Revit.DB import *

#pyRevit
from pyrevit import forms, script

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# 👉 Get pyRevit Output
from pyrevit import script
output = script.get_output()

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
doc    = __revit__.ActiveUIDocument.Document #type:Document
uidoc  = __revit__.ActiveUIDocument          # __revit__ is internal variable in pyRevit
app    = __revit__.Application
output = script.get_output()                 # pyRevit Output Menu


# FONCTION
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
#👉 Create the fonction to get all elements and filter by in place (créer la fonction permettant de sélectionner tout les éléments et filtrer ceux modélisés in situ)
def get_in_elements():
    #👉 Get All Elements (récupérer tout les éléments)
    elements = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()

    #👉 Get inPlace Elements (filtrer les éléments placés)
    in_place_elems = []
    for elem in elements:
        #🚨 Try/except to handle Elements without types/families
        try:
            elem_type_id = elem.GetTypeId()             # Get Type Id (Universal)
            elem_type    = doc.GetElement(elem_type_id) # Convert ElementId to Element
            elem_family  = elem_type.Family             # Get Family
            if elem_family.IsInPlace:               # Check IsInPlace Property
                # print('InPlace Element;', elem.Id)
                in_place_elems.append(elem)
        except:
            pass

    # 🚨 Check is Inplace in the project
    if not in_place_elems:
        forms.alert("No In-Place Elements found.Good job!!\n"
                    "Pas de modèle In Situ dans la maquette, Bravo, Beau travail !!!!", exitscript=True)
    return in_place_elems

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
#👉 Get in place elements
in_place_elems = get_in_elements()


#👉 Create a report of elements in place (créer un rapport listant les idientifiants des éléments en place)
output.print_md('## In-Place Elements Report:\nÉléments modélisés In-Situ dans le modèle:')
output.print_md('---')

for elem in in_place_elems:
    cat_name = 'Category ' + elem.Category.Name
    link = output.linkify(elem.Id, cat_name)  # Create Linkify (can be list of elem_ids too)
    print(link)

print('Execution is finished/ Analyse terminée')
print('There are {} In-Place Elements in the project / {} modèle(s) In-Situ trouvé(s) dans la maquette'.format(len(in_place_elems), len(in_place_elems)))


#███████████████████████████████████████████████████████████████████████████
# Thank you Erik
