from django.contrib.admin.sites import AlreadyRegistered


class PluginDirectory(object):
    def __init__(self):
        self._registry = {}

    def register(self, service, plugin, version=1):
        if plugin in self._registry:
            raise AlreadyRegistered('The class %s is already registered' % plugin.__name__)
        self._registry[u"%s v%s" % (service, version)] = {
            'service': service,
            'plugin': plugin,
            'version': version
        }

    def get_plugin_class(self, title):
        return self._registry[title]['plugin']

    def get_plugin_class_from_params(self, service, version):
        return self._registry[u"%s v%s" % (service, version)]['plugin']

    def get_dict(self, title):
        return self._registry[title]

    def get_all_plugin_dicts(self):
        return self._registry.values()

    @property
    def choices(self):
        return [[title, title] for title, data_dict in self._registry.items()]

pool = PluginDirectory()