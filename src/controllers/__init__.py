import pkgutil as package_utils
import importlib 

__all__ = []

for _, module_name, _ in package_utils.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")

    # Normalize class names from snake case to Pascal Case (e.g., my_class -> MyClass)
    class_name = ''.join(part.capitalize() for part in module_name.split("_"))
    if hasattr(module, class_name):
        globals()[class_name] = getattr(module, class_name)
    elif hasattr(module, module_name):
        globals()[module_name] = getattr(module, module_name)
    else:
        globals()[module_name] = module
    
    __all__.append(class_name if class_name in globals() else module_name)