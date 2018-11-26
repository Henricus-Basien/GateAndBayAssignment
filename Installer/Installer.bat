@echo off

color 09
REM --- Install required Modules ---
pip install -r requirements.txt
REM --- SETX Environment Variable ---
SET GABA=%~dp0\..
pushd %GABA%
SET GABA=%CD%& popd
SETX GABA "%GABA%"

pause