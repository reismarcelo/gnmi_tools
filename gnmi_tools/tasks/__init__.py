import pkgutil

__all__ = []
for loader, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name.startswith('task_'):
        __all__.append(module_name)
        _module = loader.find_module(module_name).load_module(module_name)
        globals()[module_name] = _module
