from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["requests", "colorama"],
    "include_files": ["url.txt"],
}

setup(
    name="BDIX-TESTER",
    version="0.2.1",
    description="BDIX‑TESTER v0.2.1 (Experimental)",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None)],
)
