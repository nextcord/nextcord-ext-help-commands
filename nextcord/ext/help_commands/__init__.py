from .embedded import EmbeddedHelpCommand
from .errors import MissingDependencyError
from .paginated import PaginatedHelpCommand
from .slash import MinimalSlashHelpCommand, SlashHelpCommand

# Needed for the setup.py script
__version__ = "0.0.1"

__all__ = (
    "EmbeddedHelpCommand",
    "MinimalSlashHelpCommand",
    "MissingDependencyError",
    "PaginatedHelpCommand",
    "SlashHelpCommand",
)
