# python-tkgeom
GUI layout manager for quick development of GUI programs

You can `import` this libray in your source, and have then a simplified way to construct basic GUIs with little effort. The underlying widget set is *tkinter*.
This library has the following noteworthy concepts (not in order of importance):
1. dimensions expressed in pixels are stupid. This library uses dimensions relative to the base font. The base font is "Sans 11", but can be overriden in code or via command line. A given font should be rendered in a uniform way on any system.
2. Less typing means less errors. This library tries to shorten the code needed to build a GUI. In fact, a single multi-line string is used to define the appearance of a window.
3. The geometry manager is based on *anchors*. You don't place, grid or pack anything. The geometry tells where the edges of a widget should stay: if the geometry says that a widget has *left* side anchored to the left (of the window), and *right* side to the right of the window, the widget will follow its window geometry. For simple layouts there are *NO* containers at all, all the widget inside a window are a flat list.
4. The library is not well tested; the anchor-based geometry manager works quite well, but its concepts must be fully analyzed (by me too). And I am new to python.

Let's start with a simple example. The following program, using the traditional way (*not abtgeom*), makes a simple window:

    from tkinter import *
    
    window = Tk()
    window.title("Welcome to example app")
    window.geometry('350x200')
    
    lbl = Label(window, text="Hello")
    lbl.grid(column=0, row=0)
    txt = Entry(window,width=10)
    txt.grid(column=1, row=0)
    
    def clicked():
        lbl.configure(text="Button was clicked !!")
    
    btn = Button(window, text="Click Me", command=clicked)
    btn.grid(column=2, row=0)
    
    window.mainloop()

...and see what are the problems of this approach:
* windows.geometry() says 350x200 pixels. Are they reasonable on the current system? On my PC they are too much, the window is almost empty.
* there is a lot of code for 3 widgets: the words *window*, *grid*, *column*, *row* are repeated [too] many times.
* to have an idea of what the result will be, one must read carefully the source.

The result on my PC is the following:

![output of traditional tkinter](/doc-assets/example1-result.png)

**Now see the same thing using this library:**

    import tkabtgeom as UI
    
    ui=UI.abtgeom()     # 11, "Sans"
    win=ui.MainWin("wdMain", "Welcome to abtgeom","""
        l1"Hello"    enTry-10    bt1"Click me"
        """)
    
    def clicked():
        win.child("l1").widget.settext("Button was clicked !")
    win.btbind("bt1", clicked)
    
    ui.mainloop()

... and see how different is:
**the window is created by a single function that specifies the title, no geometry, and looking lazily at the source you have an idea of what the layout is.** The result is:

![abtgeom result for the same thing](/doc-assets/example1-abtresult.png)

Note that:
- the window is smaller: it adapts to the contained widgets (and yes, the title does not fit...). BTW, the window will not stretch more than this.
- The widgets are bigger, because the default font is larger. But it should look very similar in every system

<div style="text-align: center;">
But now, let see another difference, after the button has been clicked:

![tkinter, label resizes](/doc-assets/example1-resultafterclick.png) &nbsp; ![abtgeom instead](/doc-assets/example1-abtafterclick.png)
</div>

It seems that tkinter is better because it resizes the label. But that also moves all the other widgets to the right, and this is less pleasant.
At the moment, abtgeom (this library) does not support auto-sizing labels. One should make them larger in advance, or anchor them in a way they are expanded.

Finally, to make long-story short, you can launch the file tkabtgeom.py (it has a main() with some example) and see a quite complicated GUI:

    "Descriptive label..." # (enlarge window to avoid word wrap)
    "Filter 1 (type)"             |btX1"X" btR btC btCC btCP btD btLD btPRS        |enF1-30
    "Filter 2 (value or C+code)"  |btX2"X"                                         |enF2-30
    "Filter 3 (package)"          |btX3"X" btPTH btNPTH"!PTH" btSMD btNSMD"!SMD"   |enF3-30
    sgMain>! !
    lFound"Found 0 elements   " btReduce enCodC-24 btDigikey btMouser btFarnell

The above *window description* generates the following (and imagine how much typing would be required if not using abtgeom!):

![abtgeom complicated example](/doc-assets/complicated.png)

*(The bottom row with Close, Info, etc... is added by tkabtgeom.py when used interactively as a program)*.

## Documentation
Will be prepared. For now, some explanation is in the source files:
- tkabtgeom.py is the library, but it contains also a main for interactive mode
- tkabtgeom-test.py is an example program that imports the library. It is crowded with used and commented-out code, but shows quite a few things.

## See also
[FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGUI) has similar aims, is much more complete and powerful, of course with the cost of more complexity.



