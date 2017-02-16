import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

options = {"build_exe": {"packages": ["pygame",
                                      "random",
                                      "constants",
                                      "player",
                                      "music",
                                      "sound_effects",
                                      "Menu",
                                      "Level",
                                      "enemies",
                                      "graphics",
                                      "health",
                                      "rope",
                                      "random",
                                      "os",
                                      "collections",
                                      "math",
                                      "time"]}}

cx_Freeze.setup(
    name="Draco Team Game",
    options=options,
    executables=executables
)
