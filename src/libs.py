import ctypes
from pathlib import Path

LIBS_NAME = ["calculation"]

def _load_library(lib):
    lib_name = f"lib{lib}.so"

    root_dir = Path(__file__).parent.parent
    lib_path = root_dir/"lib"/lib_name

    if not lib_path.exists():
        raise FileNotFoundError(
            "run 'pip install -e .'"
        )
    return ctypes.CDLL(str(lib_path))

libs = {}

for lib_name in LIBS_NAME:
    libs[lib_name] = _load_library(lib_name)

# calc_lib = libs[LIBS_NAME[0]] # calculation
# test_get_num = calc_lib.test_get_num
# test_get_num.argtypes = [ctypes.c_int]
# test_get_num.restype = ctypes.c_int

