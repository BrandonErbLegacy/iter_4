from local_api.ui.styling_engine import Style

dark_theme = Style("dark_theme")

DEFAULT_FONT = ("Consolas", 10)

dark_theme["Window"]["bg"] = "#111111"

dark_theme["Label"]["bg"] = "#111111"
dark_theme["Label"]["fg"] = "#CCCCCC"

dark_theme["Button"]["bg"] = "#333333"
dark_theme["Button"]["fg"] = "#CCCCCC"
dark_theme["Button"]["activebackground"] = "#222222"
dark_theme["Button"]["activeforeground"] = "#CCCCCC"
dark_theme["Button"]["borderwidth"] = 0
dark_theme["Button"]["relief"] = "flat"

dark_theme["Frame"]["bg"] = "#111111"

dark_theme["Entry"]["bg"] = "#222222"
dark_theme["Entry"]["fg"] = "#CCCCCC"
dark_theme["Entry"]["relief"] = "flat"

#dark_theme["Label"]["font"] = DEFAULT_FONT

dark_theme["Login_View_Header"]["bg"] = "#3a5775"
dark_theme["Login_View_Header.Label"]["bg"] = "#3a5775"
