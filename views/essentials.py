from local_api.ui.tk_refined import Window, Button, Label, Frame, DefaultedEntry

class LoginView(Window):
    def __init__(self):
        Window.__init__(self)
        self.class_name = "Window"

        header_frame = Frame(self)
        header_frame.class_name = "Login_View_Header"
        header_frame.pack(fill="both", padx=15, pady=10)

        middle_frame = Frame(self)
        middle_frame.pack(fill="both", padx=15, pady=10, anchor="center")

        bottom_frame = Frame(self)
        bottom_frame.pack(fill="both", padx=15, pady=10, side="bottom")

        header_label = Label(header_frame, text="ITER 4", anchor="center", font=("Verdana", 50))
        header_label.class_name = "Login_View_Header.Label"
        header_label.pack(fill="both", expand=True)

        username_entry = DefaultedEntry(middle_frame, font=("Consolas", 20))
        username_entry.set_default_text("Username")
        username_entry.pack(fill="x", padx=5, pady=5)

        password_entry = DefaultedEntry(middle_frame, font=("Consolas", 20), show="*")
        password_entry.set_default_text("Password")
        password_entry.pack(fill="x", padx=5, pady=5)

        login_button = Button(bottom_frame, text="Login", font=("Verdana", 10))
        login_button.pack(fill="x", padx=5, pady=5, ipady=5, side="left", expand=True)

        setting_button = Button(bottom_frame, text="Settings", font=("Verdana", 10))
        setting_button.pack(fill="x", padx=5, pady=5, ipady=5, side="right", expand=True)

        self.center()
        #self.geometry("325x400")
