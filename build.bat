pyinstaller -F --clean --noupx --icon %~dp0\RHODES_ISLAND_ICON.ico %~dp0\Arknights_enemy_database.py --distpath %~dp0\

rmdir /s /q %~dp0\__pycache__ %~dp0\build

del %~dp0\Arknights_enemy_database.spec