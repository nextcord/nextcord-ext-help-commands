from typing import Optional


class MissingDependencyError(Exception):
    def __init__(self, class_name: str, dependency: str, extra_group: Optional[str] = None):
        self.class_name = class_name
        self.dependency = dependency
        self.extra_group = extra_group
        message = f"{dependency} is a required dependency for {class_name}."
        if extra_group:
            message += f' You can install it by running `pip install "nextcord-ext-help-commands[{extra_group}]"`.'
        super().__init__(message)
