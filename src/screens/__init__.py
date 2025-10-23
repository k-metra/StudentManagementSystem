import pkgutil as package_utils
import importlib 

__all__ = []


# Import all modules in the screens package dynamically
# Won't have to change this file ever anymore
for _, module_name, _ in package_utils.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")


    # If the module has a specific attribute (e.g. function) named exactly after it,
    # import that attribute directly for easier access
    if hasattr(module, module_name):
        globals()[module_name] = getattr(module, module_name)
    else:
        globals()[module_name] = module 

    __all__.append(module_name)