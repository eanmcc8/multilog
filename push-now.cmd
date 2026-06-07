@echo off
setlocal
set GIT_EXE=C:\Users\Administrator\AppData\Local\GitHubDesktop\app-3.5.12\resources\app\git\mingw64\libexec\git-core\git.exe
set GIT_BIN=C:\Users\Administrator\AppData\Local\GitHubDesktop\app-3.5.12\resources\app\git\mingw64\bin
set PATH=%GIT_BIN%;%PATH%
cd /d "c:\Users\Administrator\Documents\GitHub\multilogin-automation"

echo === PUSH %date% %time% === > push-result.txt

echo --- status --- >> push-result.txt
"%GIT_EXE%" status -sb >> push-result.txt 2>&1

echo --- add all --- >> push-result.txt
"%GIT_EXE%" add -A >> push-result.txt 2>&1

echo --- commit --- >> push-result.txt
"%GIT_EXE%" commit -m "chore: sync latest changes" >> push-result.txt 2>&1

echo --- push --- >> push-result.txt
"%GIT_EXE%" push origin main >> push-result.txt 2>&1

echo --- log --- >> push-result.txt
"%GIT_EXE%" log -1 --oneline >> push-result.txt 2>&1

echo --- status after --- >> push-result.txt
"%GIT_EXE%" status -sb >> push-result.txt 2>&1

echo === DONE === >> push-result.txt
