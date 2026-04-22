REM To launch all my DevOps setups
set GIT_BASH=C:\Program Files\Git\git-bash.exe
set DOCKER=C:\Program Files\Docker\Docker\Docker Desktop.exe
set DOCKER_LAUNCH_WAIT=10
set KUBE_LAUNCH_WAIT=20
set JENKINS_URL=http://localhost:9090

REM -----------------------------------
start "" "%GIT_BASH%" -c "eval $(ssh-agent -s)"

REM -----------------------------------
start "" "%DOCKER%"
TIMEOUT /T %DOCKER_LAUNCH_WAIT%

REM -----------------------------------
start "Minikube" cmd /k "minikube start"
TIMEOUT /T %KUBE_LAUNCH_WAIT%

REM -----------------------------------
start chrome %JENKINS_URL%

echo Closing now
TIMEOUT /T 10