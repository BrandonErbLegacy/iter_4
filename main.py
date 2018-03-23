from tkinter import Tk
from local_config.styling.dark import dark_theme

from local_api.ui.tk_refined import Window
from local_api.ui.styling_engine import Style

from views.essentials import LoginView

Style.static_set_default(dark_theme)

root = Tk()
root.withdraw()

w = LoginView()
w.bind("<<Close_Window>>", lambda v: root.quit())

root.mainloop()
