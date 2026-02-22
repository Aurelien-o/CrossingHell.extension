# -*- coding: utf-8 -*-
__title__   = "03 - Name Swapper"
__doc__     = """Version = 1.0
Date    = 22.02.2026
________________________________________________________________
Description:
rename view

________________________________________________________________
How-To:
1. Select the view(s) you want to rename
2. Fill the prefix, find and replace, suffix you want to use

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


# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
doc    = __revit__.ActiveUIDocument.Document #type:Document
uidoc  = __revit__.ActiveUIDocument          # __revit__ is internal variable in pyRevit
app    = __revit__.Application
output = script.get_output()                 # pyRevit Output Menu

# ╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔
# ╠╣ ║ ║║║║║   ║ ║║ ║║║║
# ╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

def get_user_input():
    #function to get input's user with rpw.ui.forms.FlexForm
    from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox,
                              Separator, Button, CheckBox)
    components = [
        Label('Prefix:'), TextBox('prefix'),
        Label('Find:'), TextBox('find'),
        Label('Replace:'), TextBox('replace'),
        Label('Suffix:'), TextBox('suffix'),
        Separator(),
        Button('Select')]
    form = FlexForm('Name Swapper', components)
    form.show()

    return form.values


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

#1️⃣ select views in the model
from pyrevit import forms
selected_views = forms.select_views()

#🚨 Ensure user has selected view(s)
if not selected_views:
    forms.alert('No selected views, please try again', exitscript=True)

#2️⃣ Define naming rules
user_input = get_user_input()

#🚨 Ensure user input
if not user_input:
    forms.alert('No input to rename the views, please try again', exitscript=True)

PREFIX     =  user_input['prefix']
FIND       =  user_input['find']
REPLACE    =  user_input['replace']
SUFFIX     =  user_input['suffix']
# 🚨 Ensure user do not use forbidden_symbols
forbidden_symbols = "\:{}[]|; <>?`~"
for sym in forbidden_symbols:
    if sym in PREFIX or sym in FIND or sym in SUFFIX or sym in REPLACE:
        forms.alert('this characters are forbidden:"\:{}[]|; <>?`~ , please try again', exitscript=True)
#3️⃣ rename views
# 🔓 Allow Changes with Revit API
t = Transaction(doc, '03 - Name Swapper')
t.Start()  # 🔓 Allow Changes



print('Renaming views / vue(s) renommé(es)')
print('-'*50)
for view in selected_views:
    old_name = view.Name
    new_name = PREFIX + old_name.replace(FIND, REPLACE) + SUFFIX

    #🚨 Ensure to use unique view name
    if new_name != old_name:
        for i in range(20):
            try:
                view.Name = new_name
                break
            except:
                new_name += '*'

    view.Name = new_name
    #4️⃣ list and show the changes
    # Create Linkify Button
    link_new_name = output.linkify(view.Id, view.Name)
    print ('{} ➡ {}'.format(old_name, link_new_name))

t.Commit()  #🔒 Confirm Changes

# #███████████████████████████████████████████████████████████████████████████
# # Thanks Erik
