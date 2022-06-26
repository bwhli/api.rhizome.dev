import os

from fastapi.templating import Jinja2Templates

__version__ = "0.1.0"

template_folder = f"{os.path.dirname(__file__)}/app/templates"
templates = Jinja2Templates(directory=template_folder)
