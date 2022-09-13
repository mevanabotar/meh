from importlib import reload
from types import ModuleType
import sys
import os

def rreload(module, paths=None, mdict=None, base_module=None, blacklist=None, reloaded_modules=None):
    """Recursively reload modules."""
    if paths is None:
        paths = [""]
    if mdict is None:
        mdict = {}
    if module not in mdict:
        # modules reloaded from this module
        mdict[module] = []
    if base_module is None:
        base_module = module
    if blacklist is None:
        blacklist = ["importlib", "typing"]
    if reloaded_modules is None:
        reloaded_modules = []
    reload(module)
    reloaded_modules.append(module.__name__)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType and attribute.__name__ not in blacklist:
            if attribute not in mdict[module]:
                if attribute.__name__ not in sys.builtin_module_names:
                    if os.path.dirname(attribute.__file__) in paths:
                        mdict[module].append(attribute)
                        reloaded_modules = rreload(attribute, paths, mdict, base_module, blacklist, reloaded_modules)
        elif callable(attribute) and attribute.__module__ not in blacklist:
            if attribute.__module__ not in sys.builtin_module_names and f"_{attribute.__module__}" not in sys.builtin_module_names:
                if sys.modules[attribute.__module__] != base_module:
                    if sys.modules[attribute.__module__] not in mdict:
                        mdict[sys.modules[attribute.__module__]] = [attribute]
                        reloaded_modules = rreload(sys.modules[attribute.__module__], paths, mdict, base_module, blacklist, reloaded_modules)
    reload(module)
    return reloaded_modules
