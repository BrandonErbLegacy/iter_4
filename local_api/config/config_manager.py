class ConfigManager:
	def __init__(self):
		pass

class Environment:
	KEYS = {}
	ENVIRONMENTS = {}

	def add_key(self, key, default_val=None):
		if key not in self.KEYS.keys():
			self.KEYS[key] = default_val
		else:
			self.KEYS[key] = default_val
			print("ENVIRONMENT: %s key exists already. Did you mean to overwrite it?"%key)

	def remove_key(self, key):
		if key in self.KEYS.keys():
			del self.KEYS[key]
		else:
			print("ENVIRONMENT: %s does not exist"%key)

	def __getitem__(self, key):
		if key in self.ENVIRONMENTS.keys():
			return_val = {}
			for item in self.KEYS.keys():
				return_val[item] = self.KEYS[item]
			for item in self.ENVIRONMENTS[key].keys():
				return_val[item] = self.ENVIRONMENTS[key][item]
			return return_val
		else:
			self.ENVIRONMENTS[key] = {}
			return self.ENVIRONMENTS[key]

if __name__ == "__main__":
	envMgr = Environment()
	envMgr.add_key("ip", "localhost")
	envMgr.add_key("port", 50008)
	envMgr["PROD"]["ip"] = "192.168.1.1"
	print(envMgr["PROD"])
