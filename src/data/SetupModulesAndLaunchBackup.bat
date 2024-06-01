pip install tkcalendar
pip install tkscrolledframe

pip install matplotlib
pip install numpy
pip install datetime

pip install bcrypt
pip install scipy

echo ^@echo off > GrassMan.bat
echo python ./src/main.py >> GrassMan.bat

python ./src/main.py

(goto) 2>nul & del "%~f0"
