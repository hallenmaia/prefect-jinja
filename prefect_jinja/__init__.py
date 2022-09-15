from . import _version
from .blocks import JinjaEnvironmentBlock
from .tasks import jinja_render_from_template, jinja_render_from_string

__version__ = _version.get_versions()["version"]

