class PluginModes:
    Client, Server, CommandLine = range(3)
    #This is so we can have enum like references (eg: PluginModes.Client)

class Plugin:
    def __init__(self):
        pass

    def on_install(self):
        pass

    def on_load(self):
        pass

    def on_run(self):
        pass

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass
