import os
import sys
import customtkinter as ctk
from PIL import Image


def base_path():
    """
    Retorna a base path para:
    - PyInstaller (onefile e onedir)
    - Inno Setup
    - Desenvolvimento normal
    """
    if getattr(sys, 'frozen', False):

        if hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS  # type: ignore
        return os.path.dirname(sys.argv[0])

    return os.path.dirname(os.path.abspath(sys.argv[0]))


ASSETS_DIR = os.path.join(base_path(), "assets")


def asset_path(*paths):
    return os.path.join(ASSETS_DIR, *paths)


def load_icon(filename):
    path = asset_path("imgs", filename)
    return ctk.CTkImage(
        light_image=Image.open(path),
        size=(35, 35))
