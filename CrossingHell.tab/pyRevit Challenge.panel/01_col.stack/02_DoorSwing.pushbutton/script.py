# -*- coding: utf-8 -*-
__title__   = "02 - Door Swing"
__doc__     = """Version = 1.0
Date    = 19.02.2026
________________________________________________________________
Description:
 Searchs Doors and write if it's mirrored or not in one of parameters.

________________________________________________________________
How-To:
1. Step 1...
2. Step 2...
3. Step 3...

________________________________________________________________
To-Do:
[FEATURE] - Describe Your Feature...
[BUG]     - Describe Your BUG...

________________________________________________________________
Last Updates:
- [01.01.2026] v1.0 Change Description
- [01.01.2026] v0.5 Change Description
- [01.01.2026] v0.1 Change Description 
________________________________________________________________
Author: Erik Frits (from LearnRevitAPI.com)"""

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


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
doc    = __revit__.ActiveUIDocument.Document #type:Document
uidoc  = __revit__.ActiveUIDocument          # __revit__ is internal variable in pyRevit
app    = __revit__.Application
output = script.get_output()                 # pyRevit Output Menu

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
#🤖 Automate Your Boring Work Here


# #0️⃣ Pick Single Object / first we test with only one door
# from Autodesk.Revit.UI.Selection import ObjectType
# ref  = uidoc.Selection.PickObject(ObjectType.Element)
# door = doc.GetElement(ref)

#1️⃣ select all doors in the model
all_doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

for doors in all_doors:
     #2️⃣get doors swing (mirrored or not)
    print(door.Mirrored)
    value = 'Mirrored' if door.Mirrored else 'Regular'

    #🔓 Allow Changes with Revit API
    t = Transaction(doc, 'Door Swing')
    t.Start()   #🔓 Allow Changes

    #3️⃣write the parameter value to comment's parameter
    # Get Built-In Parameter
    param = door.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
    param.Set(value)

    t.Commit()  #🔒 Confirm Changes



#███████████████████████████████████████████████████████████████████████████
# Happy Coding!
