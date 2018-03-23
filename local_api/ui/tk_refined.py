from local_api.ui.styling_engine import StyleLinker

from tkinter import Toplevel
from tkinter import Frame as tkFrame
from tkinter import Label as tkLabel
from tkinter import Text as tkText
from tkinter import Entry as tkEntry
from tkinter import Button as tkButton
from tkinter import Checkbutton as tkCheckbutton
from tkinter import Canvas as tkCanvas
from tkinter import Listbox as tkListbox
from tkinter import Scrollbar
from tkinter import PanedWindow as tkPaned

from tkinter import IntVar

class Window(Toplevel):
	def __init__(self, **kw):
		Toplevel.__init__(self, **kw)
		self.__isMain__ = False
		self.protocol("WM_DELETE_WINDOW", self.closeWindow)
		self.__IsShown__ = True
		StyleLinker(self)

		#self.menu = Menu(self)
		#self.menu.pack(fill=X)
		self.focus()

	def center(self):
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()
		my_height = self.winfo_reqheight()
		my_width = self.winfo_reqwidth()
		newX = (screen_width/2) - (my_width/2)
		newY = (screen_height/2) - (my_height/2)
		self.geometry("+%i+%i"%(newX, newY))

	def destroyWindow(self, e=None):
		self.destroy()

	def toggleHide(self):
		if self.__IsShown__:
			self.hideWindow()
		else:
			self.showWindow()

	def hideWindow(self):
		self.__IsShown__ = False
		self.withdraw()

	def showWindow(self):
		self.__IsShown__ = True
		self.deiconify()

	def hideMenu(self):
		pass
		#self.menu.forget()

	def closeWindow(self):
		self.event_generate("<<Close_Window>>")

class Frame(tkFrame):
	def __init__(self, master, **kw):
		tkFrame.__init__(self, master, **kw)
		StyleLinker(self)

class PanedWindow(tkPaned):
	def __init__(self, master, **kw):
		tkPaned.__init__(self, master, **kw)
		StyleLinker(self)

class Label(tkLabel):
	def __init__(self, master, **kw):
		tkLabel.__init__(self, master, **kw)
		StyleLinker(self)

class Text(tkText):
	def __init__(self, master, **kw):
		tkText.__init__(self, master, **kw)
		StyleLinker(self)
	def get(self, *args, **kw):
		#Strip new line added at end by default
		return tkText.get(self, *args, **kw)[:-1]

class Entry(tkEntry):
	def __init__(self, master, **kw):
		tkEntry.__init__(self, master, **kw)
		StyleLinker(self)

class Button(tkButton):
	def __init__(self, master, **kw):
		tkButton.__init__(self, master, **kw)
		StyleLinker(self)

class Listbox(tkListbox):
	def __init__(self, master, **kw):
		tkListbox.__init__(self, master, **kw)
		StyleLinker(self)

class Canvas(tkCanvas):
	def __init__(self, master, **kw):
		tkCanvas.__init__(self, master, **kw)
		StyleLinker(self)

class Checkbox(tkCheckbutton):
	def __init__(self, master, **kw):
		self.variable = IntVar()

		kw["variable"] = self.variable

		tkCheckbutton.__init__(self, master, **kw)
		StyleLinker(self)

	def setValue(self, val):
		self.variable.set(val)

	def isChecked(self):
		return self.variable.get()

class SizedButton(Button):
	def __init__(self, master, **kw):
		newKw = {}
		if "width" in kw.keys():
			newKw["width"] = kw["width"]
		if "height" in kw.keys():
			newKw["height"] = kw["height"]
		del kw["height"]
		del kw["width"]
		self._host = Frame(master, **newKw)
		Button.__init__(self, self._host, **kw)
	def pack(self, **kw):
		self._host.pack_propagate(False)
		self._host.pack(**kw)
		Button.pack(self, fill="both", expand=True)

class HighlightableButton(Button):
	def __init__(self, master, **kw):
		Button.__init__(self, master, **kw)

		self.className = "HighlightableButton.Normal"

		self.bind("<Enter>", self.highlight)
		self.bind("<Leave>", self.unhighlight)

	def highlight(self, e):
		self.className = "HighlightableButton.Active"

	def unhighlight(self, e):
		self.className = "HighlightableButton.Normal"

class TitledFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)

		self.title = Label(self)
		self.title.className = "TitledFrame.Title"
		self.title.pack(fill="x", anchor="center")

	def setTitle(self, text):
		self.title["text"] = text

class HighlightableLabel(Label):
	def __init__(self, master, **kw):
		Label.__init__(self, master, **kw)

		self.className = "HighlightableLabel.Normal"

		self.bind("<Enter>", self.highlight)
		self.bind("<Leave>", self.unhighlight)

	def highlight(self, e):
		self.className = "HighlightableLabel.Active"

	def unhighlight(self, e):
		self.className = "HighlightableLabel.Normal"

class Tabber(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.tabs = {}

		self.tabBar = Frame(self, height=33)
		self.tabBar.pack(fill=X, side=TOP, anchor=N)
		self.tabBar.className = "Tabber_TabBar"

		self.selectedTab = None

		self.selectedUuid = None

	def createNewTab(self, frame, text):
		t = Tab(self.tabBar)
		uuid = t.uuid
		t.updateText(text)
		t.frame = frame
		t.pack(anchor=W, fill=Y, side=LEFT, padx=1, pady=1)

		t.textW.bind("<Button-1>", lambda e: self.swapTabByUuid(uuid))
		t.bind("<Button-1>", lambda e: self.swapTabByUuid(uuid))

		t.closeButton["command"] = lambda: self.deleteTabByUuid(uuid)

		self.tabs[uuid] = t
		return uuid

	def swapTabByUuid(self, uuid):
		tab = self.tabs[uuid]
		if self.selectedTab != None:
			self.selectedTab.forget()
			currentTab = self.tabs[self.selectedUuid]
			currentTab.className = "Tab"
			currentTab.textW.className = "Tabber_TabTitle"
			currentTab.status = "Inactive"
			currentTab.closeButton.className = "Tabber_TabCloseButton_Inactive"
			#print(self.getActiveFrame().IDE_GET_OPENED_FILE())
		self.selectedTab = tab.frame
		self.selectedUuid = uuid
		tab.frame.pack(fill=BOTH, expand=True, ipadx=5, ipady=5)
		tab.textW.className = "Tabber_TabTitle_Active"
		tab.status = "Active"
		tab.closeButton.className = "Tabber_TabCloseButton_Active"
		tab.className = "Tab_Active"

	def deleteTabByUuid(self, uuid):
		tab = self.tabs[uuid]
		del self.tabs[uuid]
		if self.selectedUuid == uuid:
			self.selectedUuid = None
			self.selectedTab.forget()
			self.selectedTab = None
		tab.forget()

	def getActiveTabUuid(self):
		return self.selectedUuid

	def getActiveFrame(self):
		return self.selectedTab

class Tab(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.uuid = uuid4()
		self.frame = None
		self.text = "New Tab"

		self.status = "Inactive"

		self.textW = Label(self, text=self.text)
		self.textW.className = "Tabber_TabTitle"
		self.textW.pack(fill=BOTH, padx=5, pady=5, side=LEFT)

		self.closeButton = Button(self, text="x")
		self.closeButton.pack(side=RIGHT, anchor=CENTER)
		self.closeButton.className = "Tabber_TabCloseButton_Inactive"

		self.closeButton.bind("<Enter>", self.closeButtonOnHover)
		self.closeButton.bind("<Leave>", self.closeButtonOnUnhover)

	def closeButtonOnHover(self, e):
		self.closeButton.className = "Tabber_TabCloseButton_Hover"

	def closeButtonOnUnhover(self, e):
		self.closeButton.className = "Tabber_TabCloseButton_%s"%self.status

	def updateText(self, text):
		self.textW["text"] = text
		self.text = text

class ScrollableFrame(Frame):
	def __init__(self, master, **kw):
		Frame.__init__(self, master, **kw)
		self.canvas = Canvas(self)
		self.canvas.pack(side="left", fill="both", expand=True)
		self.scroll = Scrollbar(self)
		#self.scroll.pack(side="right", fill="y")

		self.canvas["yscrollcommand"] = self.scroll.set
		self.scroll["command"] = self.canvas.yview

		self.innerFrame = Frame(self.canvas)
		self.canvas_frame = self.canvas.create_window((0,0), window=self.innerFrame, anchor="nw")

		self.innerFrame.bind("<Configure>", self.frameConfig)
		self.canvas.bind('<Configure>', self.frameWidth)
		#self.bind_all("<MouseWheel>", self.innerScroll)

	def showScrollbar(self, t):
		if t == False:
			self.scroll.forget()
		else:
			self.scroll.pack(side="right", fill="y")

	def frameWidth(self, event):
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

	def frameConfig(self, event):
		self.canvas["scrollregion"] = self.canvas.bbox("all")
		for item in self.innerFrame.winfo_children():
			item.bind("<MouseWheel>", self.innerScroll)

	def configureScroll(self):
		for item in self.innerFrame.winfo_children():
			item.bind("<MouseWheel>", self.innerScroll)

	def innerScroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/40)), "units")

	def getInner(self):
		return self.innerFrame

class Menu(Frame):
	def __init__(self, master, *args, **kw):
		self.frames = {}
		self.master = master
		try:
			super().__init__(master, *args, **kw)
		except:
			Frame.__init__(self, master, *args, **kw)
		self.openMenu = None
		self.min_width = 100
		self.min_height = None

	def setMinWidth(self, minw):
		self.min_width = minw

	def setMinHeight(self, minh):
		self.min_height = minh

	def addMainMenu(self, name):
		newButton = HighlightableButton(self, text=name)
		newButton.pack(anchor="w", side="left")
		#newButton.className = "Menu_Main"

		newButton.bind("<Button>", self.createDropdown)
		newButton.bind("<Enter>", self.switchDropdown)

		f = Frame(self.master)
		self.frames[name] = f

	def switchDropdown(self, event):
		if self.openMenu == None:
			return
		else:
			self.createDropdown(event)

	def createDropdown(self, event):
		parent = self.nametowidget(event.widget)
		frame = self.frames[parent.cget("text")]
		frame.className = "MenuBorder"
		if self.openMenu != None:
			if self.openMenu != frame:
				self.hideOpenDropdown()
			else:
				self.hideOpenDropdown()
				return
		hostWindow = self.nametowidget(self.nametowidget(parent.winfo_parent()).winfo_parent())
		xOffset = abs(hostWindow.winfo_rootx() - parent.winfo_rootx())
		yOffset = abs(hostWindow.winfo_rooty() - parent.winfo_rooty())
		x = xOffset
		y = yOffset+25
		frame.place(x=x, y=y)
		frame.tkraise()
		if self.min_width:
			if frame.winfo_reqwidth() < self.min_width:
				frame.pack_propagate(0)
				frame["width"] = self.min_width
		else:
			frame["width"] = 300
		if self.min_height:
			if frame.winfo_reqheight() < self.min_height:
				frame.pack_propagate(0)
				frame["height"] = self.min_height
		else:
			frame["height"] = len(frame.winfo_children())*30

		self.openMenu = frame

	def hideOpenDropdown(self, event=None):
		self.openMenu.place_forget()
		self.openMenu = None

	def addSubMenu(self, main, sub, func):
		parent = self.frames[main]
		newButton = HighlightableButton(parent, text=sub, command=lambda: self.interceptCommand(func))
		newButton.pack(anchor="w", fill="x", padx=1, pady=1)

	def interceptCommand(self, command):
		self.hideOpenDropdown()
		command()

class DefaultedEntry(tkEntry):
    def __init__(self, master, **kw):
        self._default_text = None
        self._initial_show_state = ""
        if "show" in kw.keys():
            self._initial_show_state = kw["show"]
        Entry.__init__(self, master, **kw)
        self.bind("<FocusIn>", self.clear_text)
        self.bind("<FocusOut>", self.check_text)

    def set_default_text(self, text):
        self._default_text = text
        self.insert(0, text)
        self["show"] = ""

    def clear_text(self, event):
        if self.get() == self._default_text:
            self.delete(0, "end")
            self["show"] = self._initial_show_state

    def check_text(self, event):
        if self.get() == "":
            self.set_default_text(self._default_text)

## Templates for commonly done things ##

class LoginTemplate(Window):
	def __init__(self, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"
		self.geometry("300x120")

		self.userFrame = Frame(self)
		self.passFrame = Frame(self)
		self.buttFrame = Frame(self)
		self.extraFrame = Frame(self)

		self.userFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.passFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.buttFrame.pack(fill="x", expand=True, pady=5, padx=5)
		self.extraFrame.pack(fill="x", expand=True, pady=5, padx=5)

		self.userLabel = Label(self.userFrame, text="Username: ", width=12)
		self.userLabel.pack(side="left")
		self.userEntry = Entry(self.userFrame)
		self.userEntry.pack(side="right", fill="x", expand=True, ipadx=5, ipady=3)

		self.passLabel = Label(self.passFrame, text="Password: ", width=12)
		self.passLabel.pack(side="left")
		self.passEntry = Entry(self.passFrame, show="*")
		self.passEntry.pack(side="right", fill="x", expand=True, ipadx=5, ipady=3)

		self.okButton = Button(self.buttFrame, text="Go", command=lambda: self.event_generate("<<Login>>"))
		self.okButton.pack(side="left", fill="x", expand=True, padx=5)
		self.cancelButton = Button(self.buttFrame, text="Cancel", command=lambda: self.event_generate("<<Cancel>>"))
		self.cancelButton.pack(side="right", fill="x", expand=True, padx=5)


		self.userEntry.bind("<Return>", lambda e: self.event_generate("<<Login>>"))
		self.passEntry.bind("<Return>", lambda e: self.event_generate("<<Login>>"))

	def getUsername(self):
		return self.userEntry.get()

	def getPassword(self):
		return self.passEntry.get()

class OkDialog(Window):
	def __init__(self, message, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"
		self.geometry("300x100")

		self.label = Label(self, text=message)
		self.label.pack(fill="x", expand=True, anchor="w")

		self.okButton = Button(self, text="Ok", command=self.destroyWindow)
		self.okButton.pack(fill="x", expand=True, padx=5, pady=5)

		self.geometry("300x100")
		self.center()
		self.focus()

	def setOkText(self, text):
		self.okButton["text"] = text

	def setOkAction(self, callback):
		self.okButton["command"] = callback

class OkCancelDialog(Window):
	def __init__(self, message, **kw):
		Window.__init__(self, **kw)
		self.bind("<<Close_Window>>", self.destroyWindow)
		self.className = "Window"

		self.label = Label(self, text=message)
		self.label.pack(fill="x", expand=True, anchor="w")

		self.buttonFrame = Frame(self)
		self.buttonFrame.pack(fill="x", expand=True)

		self.okButton = Button(self.buttonFrame, text="Ok")
		self.okButton.pack(side="left", fill="x", expand=True, padx=5, pady=5)

		self.cancelButton = Button(self.buttonFrame, text="Cancel")
		self.cancelButton.pack(side="right", fill="x", expand=True, padx=5, pady=5)

		self.geometry("300x100")
		self.center()
		self.focus()

	def setOkText(self, text):
		self.okButton["text"] = text

	def setCancelText(self, text):
		self.cancelButton["text"] = text

	def setOkAction(self, callback):
		self.okButton["command"] = callback

	def setCancelAction(self, callback):
		self.cancelButton["command"] = callback
