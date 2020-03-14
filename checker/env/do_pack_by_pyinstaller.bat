pyinstaller.exe pyinstaller_pack_f.spec
copy .\dist\MCUX-SDK-CodingStyleChecker.exe ..\bin
rd /q /s .\build
rd /q /s .\dist