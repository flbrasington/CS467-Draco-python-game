import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

options = {"build_exe": {"packages": ["pygame",
                                      "random",
                                      "random",
                                      "os",
                                      "collections",
                                      "math",
                                      "time"],
                         "include_files": ["constants.py",
                                           "player.py",
                                           "music.py",
                                           "sound_effects.py",
                                           "Menu.py",
                                           "Level.py",
                                           "enemies.py",
                                           "graphics.py",
                                           "health.py",
                                           "rope.py",
                                           "Graphics/",
                                           "Music/",
                                           "SoundEffects/",
                                           "room_templates/"]}}

cx_Freeze.setup(
    name="Draco Team Game",
    options=options,
    executables=executables
)
