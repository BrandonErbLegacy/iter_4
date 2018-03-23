class PromiseNotFoundException(Exception):
    pass

class InvalidPromiseEnvVariable(Exception):
    pass

class PromiseNamespaceTaken(Exception):
    pass

class PromiseModes:
    Client, Server, CommandLine = range(3)
    #This is so we can have enum like references (eg: PromiseModes.Client)

class PromiseDefinition:
    def __init__(self, promise_name, promise_manager_name="DEFAULT"):
        #This method registers the promise by default
        PromiseManager.static_register_promise(promise_manager_name, promise_name, self)

    def client_action(self, **kw):
        print("This is an undefined client_action")

    def server_action(self, **kw):
        print("This is an undefined server_action")

    def command_line_action(self, **kw):
        print("This is an undefined command_line_action")

class PromiseManager:
    TAKEN_NAMESPACES = []
    KNOWN_PROMISES = {}
    ENVIRONMENT_VARIABLES = {}
    def __init__(self, manager_name, mode=PromiseModes.Client):
        self.manager_name = manager_name
        if self.is_namespace_taken():
            raise PromiseNamespaceTaken()
        self.mode = mode

    def is_namespace_taken(self):
        return PromiseManager.static_is_namespace_taken(self.manager_name)

    def register_promise(self, name, promise_object):
        self.KNOWN_PROMISES[("%s:%s"%(self.manager_name, name))] = promise_object

    def set_environment_variable(self, name, value):
        self.ENVIRONMENT_VARIABLES[("%s:%s"%(self.manager_name, name))] = value

    def execute_promise(self, name, **kw):
        self._explicit_execute_promise(self.manager_name, name, **kw)

    def execute_external_promise(self, namespace, name, **kw):
        self._explicit_execute_promise(namespace, name, **kw)

    def get_environment_variable(self, name):
        return self._explicit_find_environment_variable(self.manager_name, name)

    def get_external_environment_variable(self, namespace, name):
        return self._explicit_find_environment_variable(namespace, name)

    def _explicit_execute_promise(self, namespace, name, **kw):
        promise = self._explicit_find_promise(namespace, name)
        if promise == None:
            raise PromiseNotFoundException()
        else:
            if self.mode == PromiseModes.Client:
                promise.client_action(**kw)
            elif self.mode == PromiseModes.Server:
                promise.server_action(**kw)
            elif self.mode == PromiseModes.CommandLine:
                promise.command_line_action(**kw)

    def _explicit_find_promise(self, namespace, name):
        namespace = "%s:%s"%(namespace, name)
        if namespace in self.KNOWN_PROMISES.keys():
            return self.KNOWN_PROMISES[namespace]
        else:
            return None

    def _explicit_find_environment_variable(self, namespace, name):
        namespace = "%s:%s"%(namespace, name)
        if namespace in self.ENVIRONMENT_VARIABLES.keys():
            return self.ENVIRONMENT_VARIABLES[namespace]
        else:
            return None

    @staticmethod
    def static_is_namespace_taken(manager_name):
        if manager_name in PromiseManager.TAKEN_NAMESPACES:
            return True
        else:
            return False

    @staticmethod
    def static_register_promise(manager_name, name, promise_object):
        PromiseManager.KNOWN_PROMISES[("%s:%s"%(manager_name, name))] = promise_object
