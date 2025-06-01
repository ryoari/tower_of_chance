@echo off
title Tower of Chance
color 0A
cls
echo.
echo  ╔════════════════════════════════════════════╗
echo  ║                                            ║
echo  ║           THE TOWER OF CHANCE              ║
echo  ║                                            ║
echo  ║      A Game of Luck, Skill & Destiny       ║
echo  ║                                            ║
echo  ╚════════════════════════════════════════════╝
echo.
echo  Starting the game...
echo.
timeout /t 2 >nul
python tower_of_chance.py
echo.
echo  Game has ended. Press any key to exit...
pause >nul
