class Style:
	_STYLES = {}
	_ACTIVE_STYLE = None
	def __init__(self, style_name, inherits_from=None):
		self._attributes = {}
		self._parents = []
		self._style_name = style_name
		if inherits_from != None:
			if type(inherits_from) is Style:
				inherit_list = inherits_from.get_attributes()
				for v in inherit_list.keys():
					self._attributes[v] = inherit_list[v]
			else:
				#TODO: Add static tree structure to look up styles through
				raise NotImplemented("String inheritance has yet to be implemented")
		self._STYLES[style_name] = self

	def set_default(self):
		self._ACTIVE_STYLE = self

	def get_default(self):
		return self._ACTIVE_STYLE

	@staticmethod
	def static_set_default(style):
		Style._ACTIVE_STYLE = style

	@staticmethod
	def static_get_default():
		return Style._ACTIVE_STYLE

	def keys(self):
		return self._attributes.keys()

	def __setitem__(self, key, item):
		self._attributes[key] = item

	def __getitem__(self, key):
		if key in self._attributes.keys():
			return self._attributes[key]
		else:
			self._attributes[key] = Descriptor()
			return self._attributes[key]

	def __delitem__(self, key):
		if key in self._attributes.keys():
			del self._attributes[key]

	def __len__(self):
		return len(self._attributes.keys())

	def __repr__(self):
		return ("Style %s object, with %i descriptors"%(self._style_name, len(self)))

	def __str__(self):
		return ("Style %s object, with %i descriptors"%(self._style_name, len(self)))

class Descriptor:
	def __init__(self):
		self._attributes = {}

	def keys(self):
		return self._attributes.keys()

	def __getitem__(self, key):
		return self._attributes[key]

	def __setitem__(self, key, value):
		self._attributes[key] = value

	def __len__(self):
		return len(self._attributes.keys())

	def __repr__(self):
		return ("Style descriptor, with %i attributes"%(len(self)))

	def __iter__(self):
		return self._attributes.__iter__()

class StyleLinker:
	def __init__(self, widget):
		self.bind_class_name(widget)
		self.apply_current_styles(widget)

	def bind_class_name(self, widget):
		#This code adds a property named className to
		#When className is updated to a different one, it triggers
		#the style changes to be made
		#http://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work
		#http://stackoverflow.com/questions/1325673/how-to-add-property-to-a-class-dynamically
		def getter(instance):
			return instance._class_name
		def setter(instance, val):
			instance._class_name = val
			self.apply_current_styles(instance)
		def deleter(instance):
			del instance._class_name

		widget.__class__.class_name = property(getter, setter, deleter)

	def apply_current_styles(self, widget):
		try:
			class_name = widget.class_name
			init = False
		except:
			init = True
			class_name = widget.__class__.__name__

		active_style = Style.static_get_default()
		if active_style != None:
			if class_name in active_style.keys():
				for item in active_style[class_name]:
					try:
						widget[item] = active_style[class_name][item]
					except:
						print("Error applying %s to widget %s"%(item, widget))
		if init:
			widget._class_name = class_name
