@echo off
echo Set objShell = CreateObject("Shell.Application") > "%temp%\run.vbs"
echo objShell.ShellExecute "python.exe", "%~dp0文件夹结构获取.py", "", "runas" >> "%temp%\run.vbs"
cscript //nologo "%temp%\run.vbs"
del "%temp%\run.vbs"
