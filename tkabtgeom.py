# **** BUGS ****
# get current virtual row -> win.rownum
# have ":" refer to virtual row container (perhaps)
# have a mean to create a frame and describe it
# same for notebooks, have a mean to describe its pages
# make radiobutton group
# make (perhaps) listbox
# implement a callback from parsedescription, such as the host can register
#   a function to create external widgets; for example, associate "cv" to
#   function that creates a Canvas; the library will insert that
# labels which change length in runtime should be managed better
# could use getter like ##    def __getitem__(self, name):


# ###################################### NOTEWORTHY
# for tk.Label, tk.Text, and tk.Entry widgets you can use widget.settext("...") and widget.gettext()
# read a cell from a tree selected row with treeview.getselcell(column)

# ###################################### GET START

##            import tkabtgeom as UI
##            ui=UI.abtgeom(11, "Sans")   # font and size optional, overriden optionally by command line
##
##            win=ui.MainWin("wdMain", "This is Window Title","""     # <- optional GUI description string
##                "Database:" |enInCsv-50=
##                ...
##                "A frame:"  |erFR>  !
##                """)

##    Then obtain the tkinter handle via win.child(name).widget

# ###################################### DESCRIPTION STRING
  # A series of lines containing widget identifiers
  # widget in general: opts+type&name+"optional_text"+width+opts
  # so like "enName", btDo"Click here", |enName-20
     # or complete example, >bt1"A button"-15=
  # leading | like "|bt1", aligned in several rows, aligns left the corresponding widgets
  # leading > like ">bt1" moves widget to the far right (all the following too)
  # trailing > like "enF1>" fills up, and moves to the right all the following elements
  # trailing = like "btPTH=" grows width proportionally to the resize of window
  # trailing ! like "btX1!" means expand vertically the widget
  # trailing ! (or =) LAST IN LINE (no names after) means expand row vertically

  # understood widgets in description:
##        labels lXXX or simply "..."
##        button btXXX, check button ckXXX, entry enXXX, text (multiline) mlXXX
##        frame exXXX or erXXX (bordered, "relief")
##        stringgrid sgXXX and notebook nbXXX - then use StringgridConfigure() or NotebookConfigure()
##        combobox cbXXX
##        spacer spXXX (important to set width)

import tkinter as tk
from tkinter import font
from tkinter import ttk

import sys

dbgopts = ""        # specify name of widget(s) to be logged while doing layout
                    # =name, <name (starts with), .name (contains), * (all)

VERSION = "0.71"

class abtwidget:
    x = 0
    y = 0

    def __init__(_, name, widget, xg="", yg=""):
        _.name = name
        _.widget = widget
        _.x = 0
        _.y = 0
        _.w = 0
        _.h = 0
        if _.widget:
            _.w=widget.winfo_reqwidth()
            _.h=widget.winfo_reqheight()
        _.ow = _.w
        _.oh = _.h
        if _.outdbg():
            print(f" init {_.name}: {_.getogeo()}")
        _.xg = xg	# things like LL"widget", WW"widget+10"
        _.yg = yg	# L.eft, R.right. W.idth, C.enter, M.iddle
        _.rowcont = None

    def getogeo(_):
        og = f"{_.ow}x{_.oh}"
        return f"{og:<9}"

    def getgeo(_):
        geom=f"{_.w}x{_.h}+{_.x}+{_.y}"
        return f"{geom:<16}"

    def outdbg(_):      # true if has to debug =name, <name (start), .name (contains), * (all)
        if dbgopts=="": return False
        if dbgopts[0]=="*": return true
        if dbgopts[0]=="=" and _.name != dbgopts[1:]: return False
        if dbgopts[0]=="<" and not _.name.startswith(dbgopts[1:]): return False
        if dbgopts[0]=="." and not dbgopts[1:] in _.name: return False
        return True

    def getdata(_,elab):
        # RL"widget"*8, or "Wnnn"
        psz = elab.find("+")
        if psz == -1: psz = elab.find("-")
        if psz == -1: psz = elab.find("/")
        if psz == -1: psz = elab.find("*")
        if psz > 0:
            widgname = elab[1:psz]
        else:
            widgname = elab[1:]
        if widgname == "": return 0
        if widgname[0] in "0123456789":
            vl = int(widgname[0:psz])
        else:
            whatget = widgname[0]
            thewid = widgname[1:]
            wdg = _.wlist[thewid]
            match whatget:
                case "L": vl = wdg.x
                case "R": vl = wdg.x + wdg.w
                case "C": vl = wdg.x + wdg.w // 2
                case "T": vl = wdg.y
                case "B": vl = wdg.y + wdg.h
                case "M": vl = wdg.y + wdg.h // 2
                case "W": vl = wdg.w
                case "H": vl = wdg.h
                case "w": vl = wdg.w - wdg.ow    # space added by user resizing
                case "h": vl = wdg.h - wdg.oh    # space added by user resizing

        if psz > 1:
            nums = elab[psz+1:]
            if nums=="M": num=_.wlist["."].xg  # hack: XG for a toplevel is margin
            else: num = int(nums)
            if elab[psz] == "+": vl += num
            if elab[psz] == "-": vl -= num
            if elab[psz] == "*": vl *= num
            if elab[psz] == "/": vl //= num or 1
        return vl

    def update(_,wlist):
        _.wlist = wlist
        dbg = _.outdbg()
        res = False		# return True if modified

        #################### X (horizontal) geometry
        newx = _.x
        neww = _.w
        if _.xg:
            # first do all Xs, than all Ws
            split = _.xg.split(",")
            conflict = ""			# QQ faster to use integers (not strings)
            for elab in split:
                if elab=="": continue
                num = _.getdata(elab)
                if num < 0: continue
                match elab[0]:
                    case 'L':
                        newx = num ;	conflict += 'L'
                    case 'l': # move x only if less
                        if num > newx or 'R' in conflict:
                            if 'L' in conflict:
                                newx = num
                                conflict += 'L'         #print(f"{_.name}: conflict xg: {_.xg}")
                            else:
                                if 'R' in conflict:
                                    neww = newx+neww - num  # if num<=newx:
                                    newx = num
                                    conflict += 'LW'
                                else:
                                    newx = num
                                    conflict += 'L'

                    case 'W':		neww = num ;	conflict += 'W'
##                    case 'C':
##                        if 'L' in conflict:		neww = num - neww // 2  ;	conflict += 'W'
##                        else:  					neww = (num-newx) * 2   ;	conflict += 'W'
##                    case 'R':
##                        if 'L' in conflict:		neww = num - newx		;	conflict += 'W'
##                        else: newx = num - neww		;	conflict += 'R'
                    case 'r': newx = num - neww    # align right
                    case 'w': neww = _.ow + num

            # second turn
            for elab in split:
                if elab=="": continue
                num = _.getdata(elab)
                if num < 0: continue
                match elab[0]:
                    case 'C':
                        if 'L' in conflict:        neww = num - neww // 2  ;    conflict += 'W'
                        else:                      neww = (num-newx) * 2   ;    conflict += 'W'
                    case 'R':
                        if 'L' in conflict:        neww = num - newx        ;    conflict += 'W'
                        else: newx = num - neww        ;    conflict += 'R'

            if newx != _.x or neww != _.w: res = True

        #################### now Y (vertical) geometry
        newy = _.y
        newh = _.h
        if _.yg:
            split = _.yg.split(",")
            for elab in split:
                if elab=="": continue
                num = _.getdata(elab)
                if num < 0: continue
                match elab[0]:
                    case 'T': newy = num
                    case 'H': newh = num
                    case 'M': newy = num - newh // 2
                    case 'h':
                        newh = _.oh + num
##                        if newh < _.oh:
##                            newh = _.oh
                    case 'B':
                        fnewh = num - newy      # QQ trying to read something NOT ready (oh=0/ow=0)
                        if fnewh > 0: newh=fnewh
            if newy != _.y or newh != _.h: res = True

        # update widget
        if _.name != ".":
            if _.widget:
                if res : _.widget.place(x=newx, y=newy, width=neww, height=newh)
        if dbg and res:
            print(f"abtupdate: {_.name}: {_.getgeo()}", end='')
        _.x = newx
        _.y = newy
        _.w = neww
        _.h = newh
        # global dbgopts
        if dbg and res:
            print(f" -->  {_.getgeo()}")

        return res

    def pack(_,tkwidg, side = tk.LEFT, expand = True, fill = "both"):
        """Packs a tkinter widget inside this"""
        tkwidg.pack(side=side, expand=expand, fill=fill)	# necessary
        tkwidg.update()	# to update its parent
        return tkwidg


optchars=">|=!"
  ## ^ anchor left to left of aligned item in previous rows
  # > expands the item
  # | anchor left/right to the bigger of previous or subsequent
numerals="1234567890"
alfanum=numerals+'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def pszisinquote(psz, line):
    cntq = 0
    psz -= 1
    while psz >= 0:
        if line[psz] == '"': cntq += 1
        psz -= 1
    return cntq % 2 != 0

def getaligneditems(lines, npos, numrow):
    # get previous item aligned like this
    res = []
    for i in range(len(lines)):
        if i == numrow: continue
        line = lines[i]
        psz = npos
        # print(line, psz)
        if psz >= len(line): continue
        if line[psz] == ' ' or pszisinquote(psz, line): continue
        if psz == 0 or line[psz-1] == ' ':
            nam = ""
            while psz < len(line) and line[psz] in optchars:
                # nam += line[psz]
                psz += 1
            while psz < len(line) and line[psz] in alfanum:
                nam += line[psz]
                psz += 1
            res.append(nam)
    #print(f"Anchor of {lines[numrow][npos:]} in {lines} -> {res}")
    return res


def parsedesc(pnt,dsc):
    # in general: opts+type&name+"optional_text"+width+opts
    # so like "edName", edName"type here", ^edName-20, edName-20^
    opt1=""
    name=""
    npos=-1
    text=""
    width=0
    opt2=""
    L = len(dsc)

    # skip spaces
    while pnt < L and (dsc[pnt] in ' \r\n\t'): pnt += 1
    if pnt >= L: return pnt, opt1, name, npos, text, width, opt2

    # opt1
    npos = pnt
    while pnt < L and (dsc[pnt] in optchars):
        opt1 += dsc[pnt]
        pnt += 1
    if pnt >= L: return pnt, opt1, name, npos, text, width, opt2

    # name. Labels have not to be declared
    if dsc[pnt] != '"':
        while pnt < L and (dsc[pnt] in alfanum):
            name += dsc[pnt]
            pnt += 1
        if pnt >= L: return pnt, opt1, name, npos, text, width, opt2

    # read text
    if dsc[pnt] == '"':
        if name == "": name = "l"
        pnt += 1    # skip quote
        while pnt < L and (dsc[pnt] != '"'):
            text += dsc[pnt]
            pnt += 1
        pnt += 1    # skip quote
        if pnt >= L: return pnt, opt1, name, npos, text, width, opt2

    # read width
    if dsc[pnt] == '-':
        pnt = org = pnt+1
        while pnt < L and (dsc[pnt] in numerals): pnt += 1
        width = int(dsc[org:pnt])

    # opt2
    while pnt < L and (dsc[pnt] in optchars):
        opt2 += dsc[pnt]
        pnt += 1

    return pnt, opt1, name, npos, text, width, opt2

class abtwin:
    def __init__(self, name, title):
        self.name=name
        self.title = title
        self.children = {}
        win = tk.Tk()
        win.title(title)
        self.children["."] = abtwidget(".", win)
        self.widget = win
        self.marg = 8
        self.first = None       # first widget in this line or previous (before a break)
        self.last  = None       # last widget inserted
        self.firstupdate = True

        # virtual row container
        self.rowcont = None
        self.rownum  = 0

    def parsedescription(self, description):
        if description == "": return
        numrow = 0
        numlabinrow = 0
        tlines = description.splitlines()
        lines = []
        for line in tlines:
            if line == "": continue
            sline = line.strip()
            if sline == "": continue
            lines.append(sline)

        leftpipes = []     # items to be aligned together (in whole description)
        rowexpand  = []    # widgets which will expand vertically
        for line in lines:
            if line.startswith("#"): continue
            pnt = 0
            excesswdg = []  # items which grow
            moderight = None    # if active, the new widget is aligned right
            while True:
                if pnt >= len(line): break
                pnt, opt1, name, npos, text, width, opt2 = parsedesc(pnt, line)
                if '#' in opt1: break
                if name=="":
                    # print("endline: %s" % opt1)
                    if opt1=="=" or opt1=="!": rowexpand.append("vr"+str(self.rownum))
                    break

                # adjust things
                if name == 'l':
                    name = 'l'+str(numlabinrow)+"r"+str(numrow)
                    numlabinrow += 1
                if name.startswith("bt"):
                    if text=="":
                        text = name[2:]

                # create widget
                # print(f"dsc: op1={opt1}, name={name}, txt={text}, w={width}, op2={opt2}")
                if name in self.children: print(f"Name {name} already present")
                if name.startswith("l"):  wdg = self.Label(name, text, width)
                if name.startswith("bt"):
                    wdg = self.Button(name, text, width=width)
##                    hand = name+"_click"
##                    import inspect
##                    cnt = 3
##                    for f in inspect.stack():
##                        cnt -= 1
##                        if cnt > 0: continue
##                        loc = f[0].f_locals
##                        if hand in loc:
##                          if loc[name+"_click"]:
##                            wdg.widget.configure(command=loc[name+"_click"])
##                        break

                if name.startswith("ck"): wdg = self.Checkbutton(name, text, width)
                if name.startswith("en"): wdg = self.Entry(name, text, width)
                if name.startswith("ex"): wdg = self.Exframe(name)
                if name.startswith("er"): wdg = self.Exframe(name, relief="ridge")
                if name.startswith("sg"): wdg = self.Stringgrid(name, [])
                if name.startswith("nb"): wdg = self.Notebook(name, [])
                if name.startswith("ml"): wdg = self.MultiLine(name, text, width)
                if name.startswith("cb"): wdg = self.Combobox(name, [], width)
                if name.startswith("sp"): wdg = self.Space(name, width)

                # manage "|" mark (normally "LR"+self.last.name+"+8")
                if '|' in opt1:
                    anc = getaligneditems(lines, npos, numrow)
                    for wdg2 in anc:
                        leftpipes.append((name, wdg2))

                if '=' in opt2:
                    excesswdg.append(wdg)

                if moderight:
                    # align right instead of left. If there is anchor to right of win, delete
                    wdg.xg = ',RW.-M'

                    xg = moderight.xg
                    #print(f'{moderight.name}: {xg}...')
                    psz = xg.find(',RW.')
                    if psz > 0: xg = xg[:psz]
                    moderight.xg = xg + ',RL'+wdg.name+'-M'
                    #print(f'   ...{wdg.xg}')
                    moderight = wdg

                if '>' in opt1:
                    wdg.xg = 'RW.-M'
                    moderight = wdg

                if '>' in opt2:
                    wdg.xg += ',RW.-M'
                    moderight = wdg

                if '!' in opt2:
                    # wdg.yg += ",BBvr"+str(numrow)	# +"-M"
                    row = "vr"+str(numrow)
                    wdg.yg = 'TT'+row+'+M,BB'+row

            #********************* end of a row
##            if moderight:
##                moderight.xg += ',RW.-M'
##                moderight = None

            numrow += 1
            numlabinrow = 0
            self.BreakLine()
            excwidth = len(excesswdg)
            for wdg in excesswdg:
                wdg.xg += ',ww./'+str(excwidth)

        # print(f"leftpipes: {leftpipes}")
        for apipe in leftpipes:
            # if there is a "L" or "l", it must be deleted...
            wdg = self.children[apipe[0]]
            xg = wdg.xg
##            if xg.startswith('L'):
##                psz = xg.find(",")
##                if psz<0: psz=len(xg)
##                xg = xg[psz+1:]
##            # self.children[apipe[0]].xg += ',lL'+apipe[1]
            if xg:
                self.children[apipe[0]].xg = xg + ',lL'+apipe[1]
            else: self.children[apipe[0]].xg = 'lL'+apipe[1]
##            if wdg.name=='btQuit':
##                wdg.xg = 'LRl0r1+M,lLbtLogin2,RLbtLogin-M'

        excesshheight = len(rowexpand)
        for low in rowexpand:
            wg = self.children[low]
            wg.yg += ",hh./"+str(excesshheight)    # adds excess
        # print(f"Row {numrow} max={maxh}")


    def prewidget(self, name, widget):
        while name in self.children:
            name += "_"     # we don't want duplicates

        # create a containerfor this row
        if self.rowcont == None:
            # if not (name.startswith("ex") or name.startswith("fr")):
            cn = "vr"+str(self.rownum)
            self.rowcont = abtwidget(cn, None)
            if self.rownum > 0: self.rowcont.yg = "TBvr"+str(self.rownum-1)
            self.children[cn] = self.rowcont

        if self.last == None:
            # start of a new row
            if self.first == None:
                wg = abtwidget(name, widget, "L0+M", "T0+M")
            else:
                # anchor to the top of current row
                wg = abtwidget(name, widget, "LL"+self.first.name, "TTvr"+str(self.rownum)+"+M")     # "TB"+self.prevlow+"+M")
            self.first = wg
        else:
            # anchor to center of previous widget, but not if virtual row
            # print(f"{name} to Mof of {self.last.name}")
            wg = abtwidget(name, widget, "LR"+self.last.name+"+M", "MM"+self.last.name)

        wg.rowcont = self.rowcont
        self.children[name] = wg
        self.last = wg
        return wg

    def prename(self, hint, name):
        if name != "": return name
        if hasattr(self, 'widgetcount'): self.widgetcount += 1
        else: self.widgetcount = 0
        return hint+"$"+str(self.widgetcount)

    def Space(self, name, width):
        name = self.prename("sp", name)
        wg = self.prewidget(name, None)
        wg.ow = wg.w = int(width*self.marg*1.2)
        wg.oh = wg.h = self.marg // 4+1
        return wg

    def Label(self, name, text, width=0, xg='', yg=''):
        name = self.prename("l", name)
        win = tk.Label(self.widget, text=text, width=width, anchor="w")
        # print(text, ": ", win.winfo_reqwidth(), "x", win.winfo_reqheight())
        wg = self.prewidget(name, win)
        if xg != '': wg.xg = xg
        if yg != '': wg.yg = yg
        return wg

    def Button(self, name, text, command=None, width=0):
        name = self.prename("bt", name)
        win = tk.Button(self.widget, text=text, width=width, command=command, takefocus=0)
        wg = self.prewidget(name, win)
        return wg

    def Checkbutton(self, name, text, width):
        name = self.prename("ck", name)
        win = tk.Checkbutton(self.widget, text=text, width=width, anchor="w")
        wg = self.prewidget(name, win)
        return wg

    def Entry(self, name, text="", width=0, fontname="", fontsize=0):
        name = self.prename("en", name)
        if width == 0: width = 8
        efont = self.fontname
        if fontname: efont = fontname
        if fontsize == 0:     fontsize = self.fontsize
        win = tk.Entry(self.widget, width=width, font=efont+" "+str(fontsize))
        win.settext(text)
        wg = self.prewidget(name, win)
        return wg

    def MultiLine(self, name, text="", width=0, height=0, fontname="", fontsize=0):
        name = self.prename("ml", name)
        if width == 0: width = 20
        if height == 0: height = 8
        efont = self.fontname
        if fontname: efont = fontname
        if fontsize == 0:     fontsize = self.fontsize
        win = tk.Text(self.widget, width=width, height=height, font=efont+" "+str(fontsize))
        win.settext(text)
##        win = tk.Text(self.widget, width=width, height=height)
##        win.configure(font=(efont, fontsize, ""))
        wg = self.prewidget(name, win)
        return wg

    def Exframe(self, name, relief="flat"):
        name = self.prename("ex", name)
        win = ttk.Frame(self.widget, relief=relief, borderwidth=1, height=5) # width/height
        wg = self.prewidget(name, win)
        return wg

    def StringgridConfigure(self, name, acoldesc):
        """AColdesc is a list of title strings whose format is ^Name|width where ^ is optional and centers text"""
        if not name in self.children: return
        wg = self.children[name]
        win = wg.widget
        win.configure(columns=acoldesc, show='headings')
        tot = 0
        for col in acoldesc:
            text=col
            mside="w"
            if col.startswith("^"):
                mside=tk.CENTER
                text=col[1:]
            psz=text.find("|")
            if psz >= 0:
                win.heading(col, text=text[0:psz])
                width = int(text[psz+1:])
                win.column(col, width=width, stretch=False, anchor=mside)
                tot += width+1
            else:
                win.heading(col, text=text)
                width = self.marg*len(col)
                win.column(col, width=width, stretch=False, anchor=mside)
                tot += width+1

        wg.ow = tot     # +len(acoldesc)
        wg.w = wg.ow


    def Stringgrid(self, name, coldesc, fontname="", fontsize=0):
        name = self.prename("sg", name)
        win = ttk.Treeview(self.widget, columns=coldesc, show='headings')
        wg = self.prewidget(name, win)
        self.StringgridConfigure(name, coldesc)

        # style
        if fontname=="": fontname = self.fontname
        if fontsize==0:  fontsize=self.fontsize
        style = ttk.Style(win)
        style.configure('Treeview.Heading', font=(fontname, fontsize-1))
        style.configure('Treeview', font=(fontname, fontsize-2))
        return wg

    def NotebookConfigure(self, name, apages, w=0, h=0):
        wdg = self.children[name]
        nb = wdg.widget
        if w or h:
            if w==0: w=2*h
            if h==0: h=w // 2
            # nb.configure(width=w, height=h)
            wdg.w = wdg.ow = w*self.marg
            wdg.h = wdg.oh = h*self.marg
        pagehandles = []
        for page in apages:
            frame1 = ttk.Frame(nb) #, width=400, height=280)
            # frame1.pack_propagate(0)
            frame1.pack(fill='both', expand=True)
            nb.add(frame1, text=" "+page+" ")
            pagehandles.append(frame1)
        wdg.pages = pagehandles
        return pagehandles


    def Notebook(self, name, apages, w=0, h=0):
        """Returns a list containing the notebook itself and the pages inside"""
        name = self.prename("nb", name)
        nb = ttk.Notebook(self.widget) # width/height
        style = ttk.Style(nb)   #self.topwindows[0]
        style.configure('TNotebook.Tab', font=(self.fontname, self.fontsize))
        # style.configure('TNotebook.Tab', foreground="red3")
        wg = self.prewidget(name, nb)
        if h==0: h=40
        if w==0: w=80
        w = w*self.marg
        h = h*self.marg
        wg.h = wg.oh = h
        wg.w = wg.ow = w

        self.NotebookConfigure(name, apages)
        return wg

    def Combobox(self, name, items, width, kind='readonly'):
        name = self.prename("cb", name)
        if width: nb = ttk.Combobox(self.widget, width=width) # readonly/normal
        else: nb = ttk.Combobox(self.widget) # readonly/normal
        nb['state'] = kind
        nb['values'] = items
        wg = self.prewidget(name, nb)
        return wg


    def addwidget(self, name, tkwidget):
        """adds a tkinter widget into this window"""
        wg = self.prewidget(name, tkwidget)
        return wg


    def BreakLine(self):
        if self.last:
            self.last = None
            self.rowcont = None
            self.rownum += 1

    def update(self):
        # lays down widgets and calculate window size
        ww = 0
        self.children["."].xg = self.marg   # hack, the xg contains horizontal margin

        # adjust virtual rows widths
        for nm,wg in self.children.items():
          if not nm.startswith('vr'): continue
          wg.w = 0
          wg.h = 0

        maxiter = len(self.children)
        while maxiter > 0:
            if maxiter+8 < len(self.children):
                print(f"        ---- Repack cycle {maxiter}")
            repeat = False
            prevcont = None
            for nm,wg in self.children.items():
                if nm == ".": continue          # QQ maybe a sublist is better?

                #if self.firstupdate:
                if wg.ow < 2:
                    if nm.startswith("exFR"): # or wg.name.startswith("vr"):
                        #print(f" prima x={wg.x}, w={wg.w}")
                        if wg.widget:
                            wg.w=wg.widget.winfo_reqwidth()
                            wg.h=wg.widget.winfo_reqheight()
                            # print(f"{wg.name} -> {wg.w}x{wg.h} (ww={ww})")
                            wg.ow = wg.w
                            wg.oh = wg.h
                            # print(f"owupdate: {wg.name}: {wg.w}x{wg.h}")

                if wg.widget:
                    prew = wg.x + wg.widget.winfo_reqwidth()
                    if ww < prew: ww = prew

                if wg.update(self.children):
                    # if maxiter+8 < len(self.children):
                    # print(f"restart for {wg.name}: {wg.w}x{wg.h}+{wg.x}+{wg.y}")
                    repeat = True

                # update window width
                if nm.startswith("vr"): continue          # don't count virtual rows

                neww = wg.x+wg.w
                if neww > ww:
                    ww = int(neww)

                # update virtual row and main window
                wgcont = wg.rowcont
                if wgcont:
                    if wgcont != prevcont:
                        # new row
                        if prevcont:
                            wgcont.y = prevcont.y + prevcont.h
                        prevcont = wgcont

                    if neww > wgcont.w: wgcont.w = neww
                    newbottom = wg.y+wg.h
                    if newbottom > wgcont.y + wgcont.h:
                        wgcont.h = newbottom - wgcont.y
                        # if wgcont.name=='vr1': print(f'vr1 newh={wgcont.h} (oh={wgcont.oh})')
                        # if wgcont.oh == 0: wgcont.oh = wgcont.h
                        if self.firstupdate: wgcont.oh = wgcont.h

            if not repeat: break
            maxiter -= 1


        if self.firstupdate:
            self.firstupdate = False
            if dbgopts: print("************** finished update")

            # get items aligned to right and sum those to the window and row size
            for nm,wg in self.children.items():
                if nm == ".": continue          # QQ maybe a sublist is better?
                if "RW.-M" == wg.xg:
                    # print("Suspect", nm)
                    # in this row, add the width of this widget
                    wg.rowcont.w += wg.w+self.marg
                    if wg.rowcont.w > ww: ww = wg.rowcont.w

            ww += self.marg
            wh = wgcont.y + wgcont.h + self.marg

            me = self.children["."]
            me.w = me.ow = ww
            me.h = me.oh = wh
            self.widget.minsize(width=ww, height=wh)
            self.update()   # last loop for window updated
            for nm,wg in self.children.items():
                wg.ow = wg.w
                wg.oh = wg.h

        # print(f"Calculated Win geom: {ww}x{wh}")
            self.widget.configure(width=ww, height=wh)

    def listwidgets(self):
        print("---------------------------------")
        for nm,wg in self.children.items():
            # og = f"{wg.ow}x{wg.oh}"
            og = wg.getogeo()
            if wg.widget:
                geom = f"{wg.widget.winfo_geometry():<16}"
            else: geom=wg.getgeo()  # f"{wg.w}x{wg.h}+{wg.x}+{wg.y}"
            print(f"{nm:<8} {og} {geom}  XG={wg.xg:<26}  YG={wg.yg}")

    def child(self, name):
        return self.children[name]

##
##    def __getitem__(self, name):
##        return self.children[name]

    def getwidget(self, name):
        return self.children[name].widget

    def btbind(self, wdg, command):
        self.children[wdg].widget.configure(command=command)

    def msgerror(self, msg):
        from tkinter.messagebox import showerror
        tk.messagebox.showerror(self.title, msg, master=self.widget)
        # vedi https://docs.python.org/3/library/tkinter.messagebox.html


    # *********************************************
    # ***               ABTGEOM                 ***
    # *********************************************

def _UIGetText(widget):
    if isinstance(widget, tk.Text):
        return widget.get("1.0", tk.END)

def _UISetText(widget, text):
    if isinstance(widget, tk.Label):
        widget.configure(text=text)
    elif isinstance(widget, tk.Entry):
        widget.delete(0, tk.END)
        widget.insert(0, text)
    elif isinstance(widget, tk.Text):
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)


def _UIGetTreeSelectedCell(tree, column):
        selected_item = tree.selection()
        if not selected_item: return ""

        item_values = tree.item(selected_item)
        # può essere int o string...
        mystr = item_values['values'][column]
        if type(mystr)==str:
            mystr = mystr.strip()
        return mystr


class abtgeom:
    def __init__(self, fontsize=11, fontname="Sans"):
        self.fontsize=fontsize
        self.fontname=fontname
        self.defaultFont = 0
        # self.commandline = sys.argv

        # override from command line
        for i in range(1, len(sys.argv)):
            arg = sys.argv[i]
            if arg=="-abt?":
                self.help()

            if arg.startswith("-abtfontsize="):
                self.fontsize = int(arg[13:])
            if arg.startswith("-abtfontname="):
                self.fontname= arg[13:]


        self.mainwindows = []
        self.hmargin = 4

        self.anchorWin = None
        self.anchorX = 4
        self.anchorY = 4

        # add methods for some widgets; setattr() could be used like # setattr(tk.Entry, 'settext', self.entrySettext)
        tk.Label.settext = _UISetText   ;   tk.Label.gettext = _UIGetText
        tk.Entry.settext = _UISetText   ;   tk.Entry.gettext = _UIGetText
        tk.Text.settext  = _UISetText   ;   tk.Text.gettext  = _UIGetText
        ttk.Treeview.getselcell = _UIGetTreeSelectedCell

    def help(self):
      print("ABT version", VERSION, """supported switches:
    -abtfontsize=nn         default font size in points
    -abtfontname=name       default font typeface""")

    def on_resize(self, event, data):
        if str(event.widget) != '.': return
        wg = data.children["."]
        if wg.w == event.width and wg.h == event.height: return
        wg.w = event.width
        wg.h = event.height
        data.update()
        #print(f"{data['name']} -> {event.width}x{event.height}") # event, data)
        # print(f"resize: {data.name} -> {event.width}x{event.height}") # event, data)


    def MainWin(self, name, title, description):
        wid = abtwin(name,title)
        wid.fontname = self.fontname
        wid.fontsize = self.fontsize
        self.mainwindows.append(wid)

        wid.widget.bind("<Configure>", lambda event: self.on_resize(event, wid))
        if self.defaultFont == 0:
            self.defaultFont = font.nametofont("TkDefaultFont")
            self.defaultFont.config(family=self.fontname, size=self.fontsize)
            self.hmargin = self.defaultFont.metrics("linespace")
            # print("margin = ", self.hmargin)
        wid.marg = self.hmargin // 3

        wid.widget.option_add("*Font", f"{self.fontname} {self.fontsize}")

        wid.parsedescription(description)
        return wid

    def msgerror(self, caption, msg):
        tk.messagebox.showerror(caption, msg)
        # vedi https://docs.python.org/3/library/tkinter.messagebox.html

    def mainloop(self):
        self.mainwindows[-1].update()
        self.mainwindows[-1].widget.mainloop()


    # *********************************************
    # ***           MAIN FOR TEST               ***
    # *********************************************


def main():
    ui=abtgeom(12, "Sans")

    win=ui.MainWin("wdMain", "Try descriptions","""
        "Write a window description, or load samples:" cbPresets
        ml1>! !
        btQuit "Debug:" enDebug "<- name + Enter" >btTest
        """)
    toplevels = [win]
    win.btbind("btQuit", win.widget.quit)
    ml1 = win.child('ml1').widget
    ml1.configure(font="courier "+str(ui.fontsize))
    enDbg = win.child("enDebug").widget
    def setdbg(event):
        global dbgopts
        # print(event.keysym)
        if event.keysym=="Return":
          dbgopts="=" + enDbg.get()
          #print("dbg=", dbgopts)
    enDbg.bind("<KeyPress>", setdbg)

    def dothetest():
        description = ml1.gettext()
        awin = ui.MainWin("", cbPresets.get(), description)
        toplevels.append(awin)
        awin.BreakLine()
        awin.Button("", "Close",lambda: awin.widget.destroy())
        awin.Button("", "Info",lambda: awin.listwidgets())
        awin.Label("", "<- click to obtain info in console")
        awin.update()

    win.btbind("btTest", dothetest)
    win.widget.bind("<F9>", lambda event: dothetest())

    # configure combobox
    def loadpreset(event):
        match cbPresets.get():
          case 'Simple': ml1.settext("""
"A simple label" btQuit2= btLogin2
"Another"                 |btQuit>  btLogin !""")
          case 'This main': ml1.settext("""
"Write a window description, or load samples:" cbPresets
ml1>! !     # notice that ml1 grows in x (>) and in y (!); the row too (last !)
btQuit >btTest btShow""")
          case 'Editor': ml1.settext("""
btL"Load..." sp1-30 btS"Save..." >btQuit
btF"Find..." enName-30
erF>
ml1>! !
""")
          case 'Complicated one': ml1.settext("""
"Descriptive label..." # (enlarge window to avoid word wrap)
"Filter 1 (type)"             |btX1"X" btR btC btCC btCP btD btLD btPRS        |enF1-30
"Filter 2 (value or C+code)"  |btX2"X"                                         |enF2-30
"Filter 3 (package)"          |btX3"X" btPTH btNPTH"!PTH" btSMD btNSMD"!SMD"   |enF3-30
sgMain>! !
lFound"Found 0 elements   " btReduce enCodC-24 btDigikey btMouser btFarnell""")

    cbPresets = win.child('cbPresets').widget
    cbPresets['values'] = ['Simple', 'This main', 'Editor', 'Complicated one']
    cbPresets.bind('<<ComboboxSelected>>', loadpreset)

    ui.mainloop()
    for w in toplevels:
        try:    # not all the windows are still there...
            w.widget.destroy()
        except:
            pass

if __name__ == '__main__':
    main()
