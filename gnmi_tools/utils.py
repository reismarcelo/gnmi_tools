"""
 gnmi_tools - Basic GNMI operations on a device
 gnmi_tools.utils
"""
import argparse
import os


class EnvVar(argparse.Action):
    def __init__(self, envvar=None, required=True, default=None, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")

        default = default or os.environ.get(envvar)
        required = not required or default is None
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class TaskOptions:
    _task_options = {}

    @classmethod
    def task(cls, task_name):
        task_fn = cls._task_options.get(task_name)
        if task_fn is None:
            raise argparse.ArgumentTypeError('Invalid task. Options are: {ops}.'.format(ops=cls.options()))
        return task_fn

    @classmethod
    def options(cls):
        return ', '.join(cls._task_options)

    @classmethod
    def register(cls, task_name):
        """
        Decorator used for registering tasks.
        The class being decorated needs to be a subclass of Task.
        :param task_name: String presented to the user in order to select a task
        :return: decorator
        """
        def decorator(task_fn):
            if not callable(task_fn):
                raise GnmiPlayException(
                    'Invalid task registration, task must be callable: {name}'.format(name=task_fn.__name__))
            if task_name in cls._task_options:
                raise GnmiPlayException(
                    'Invalid task registration, task name already registered: {name}'.format(name=task_name))

            cls._task_options[task_name] = task_fn
            return task_fn

        return decorator


class GnmiPlayException(Exception):
    """ Exception for main app errors """
    pass
