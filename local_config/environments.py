from local_api.config_manager import Environment

envMgr = Environment()
envMgr.add_key("ip", "localhost")
envMgr.add_key("port", 50008)
envMgr.add_key("logging_level", "ALL")
envMgr.add_key()

#DEV is implicitly created via defaults
envMgr["PROD"]["ip"] = "192.168.1.1"
envMgr["PROD"]["logging_level"] = "ERRORS"
