from cx_Freeze import setup, Executable

# Dependências adicionais podem ser adicionadas aqui se necessário
build_exe_options = {"packages": ["os", "subprocess", "time", "platform", "datetime", "tkinter", "threading"], "include_files": []}

# Definindo o executável
executables = [Executable("ping_monitor_gui.py", base="Win32GUI", target_name="pingger.exe")]

setup(
    name="Ping Monitor",
    version="1.0",
    description="Monitor de Perda de Pacotes",
    options={"build_exe": build_exe_options},
    executables=executables
)
