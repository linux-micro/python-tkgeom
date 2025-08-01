# get current virtual row -> win.rownum
# have ":" refer to virtual row container
# have a mean to create a frame and describe it
# same for notebooks, have a mean to describe its pages
# make radiobutton group
# make combobox, listbox
# implement a callback from parsedescription, such as the host can register
# a function to create external widgets; for example, associate "cv" to
# function that creates a Canvas; the library will insert that

import tkinter as tk

import sys, os

import tkabtgeom as UI


for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg.endswith("?"):
        UI.abtgeom.help(UI.abtgeom)
        exit()

# UI.dbgopts = "=exFR"
ui=UI.abtgeom(11, "Sans")

win=ui.MainWin("wdMain", "This is Window Title","""
    "Database:" |enInCsv-50=
    "Output:"   |enOuCsv-50
    "Filter 1"          |btX1"X"-10 btR! btC btD enF1> !
    "Filter 2 (value)"  |btX2"X" sp-4 ck1"A check"
    "Filter 3"          |btX3"X"-200 btPTH= >enF3-40
    "A frame:"          |erFR>
    sg1=! !
    nb1=! !
    """)

  # in general: opts+type&name+"optional_text"+width+opts
  # so like "enName", btDo"Click here", |enName-20
  # leading | like "|bt1" aligns left of several widget
  # leading > like ">bt1" moves widget to the far right (all the following too)
  # trailing > like "enF1>" grows and align to left of following element
  # trailing = like "btPTH=" grows width proportionally to the growth of window
  # trailing ! like "btX1!" means expand vertically the widget
  # trailing ! (or !) LAST IN LINE (with no names) means expand row vertically

fr = win.child("erFR")
fr.pack(tk.Checkbutton(fr.widget, text="A checkbox"))
fr.yg = f"TT{fr.rowcont.name}+M,BB{fr.rowcont.name}"


# reconfigure sg
win.StringgridConfigure("sg1", ['Item ID|80', 'Description|280','Designators|280','Qty|60','Oth1', 'Oth2'])
# win.child("sg1").yg += ",BBvr6"
# win.child("sg1").yg += ",hh."
for i in range(10):
  win.child("sg1").widget.insert('', tk.END, values=("Val"+str(i), "2nd Column", "List of designators (col3)"))

# configure notebook
nbpags = win.NotebookConfigure("nb1", ["First tab", "Another tab", "Third tab"])
nbpags[0].configure(relief="sunken")
nbpags[1].configure(relief="ridge")

# win.children["enInCsv"].xg += ",RW.-M"          # aligns right to right.margin (or -number)
win.children["enOuCsv"].xg += ",RRenInCsv"      # aligns right to right of enInCsv

# win.children["btPTH"].xg += ",WW./2"          # width is half of window width
#win.children["btPTH"].xg += ",ww."              # adds to base width the growth of window (same as trailing >)

#win.children["btPTH"].xg += ",RLenF3-M"        # fills remaining space in row (same as trailing >)

#win.children["enF1"].xg += ",ww./2"            # adds to base width half the growth of window
#win.children["enF3"].xg = "rW.-M"              # align right in the window (same as leading >)

#lb = win.Label('l1r1', 'A label')
##lb2 = win.Label('lb2', "Another label", "", "MMbt1")
##win.BreakLine()
##lb3 = win.Label("lb3", "Label under")
##lb4 = win.Label("lb4", "More rightside")
##lb4.xg = "LRlb3+40,W180"

win.BreakLine()
win.Label("", "Database:")
win.Entry("enOne", "", 50, "courier")

# win.children["enOne"].xg += ",RW.-M"
win.child("enOne").xg += ",RW.-M"

############################ NOTEBOOK
# win.BreakLine()
# nb = win.Notebook("nb1", ["Page 1", "Page 2", "Page 3"])
# win.child("nb1").xg = "RR.-M"

############################ LAST ROW (BUTTONS)
win.BreakLine()
bt = win.Button('btInfo', 'Info', lambda: [win.listwidgets(), print(f"frame={myex.getgeo()}")])
win.Button("btUpd", "Update", win.update)

myex = win.Exframe("exFR2", relief="sunken")

# print(f"exFR2.vg: {myex.yg}")

myexw = win.child("exFR2")
myexww = myexw.widget
# win.child("exFR2").xg +=",RW.-M"
win.child("exFR2").xg +=",ww.+M"

#lab = tk.Label(myexww, text="Hello")
#lab.pack()	# already ok
#lab.update()	# to update its frame
lab = myex.pack(tk.Label(myexww, text="Hello"))

achk = myex.pack(tk.Checkbutton(myexww, text="Confirm"))

ck2 = win.addwidget("ck2", tk.Checkbutton(win.widget, text="Confirmation 2"))

#print(f"frame={myexww.winfo_reqwidth()}, lab={lab.winfo_reqwidth()}")

ui.mainloop()

