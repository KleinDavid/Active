SET expectedNodeVersion=v18.10.0

cd /d %~dp0
cd frontend

FOR /F %%F IN ('node.exe --version') DO SET nodeVersion=%%F

IF EXIST "temp.txt" ECHO found
IF NOT %nodeVersion%==%expectedNodeVersion% nvm use 18.10

npm start

pause