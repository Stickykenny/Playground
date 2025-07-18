
set SPRING_DIR=./Relaytd
set ANGULAR_DIR=./Overlaytd

start "Angular App" cmd /k "cd /d %ANGULAR_DIR% && ng serve"


Start "Spring Boot App" cmd /k "cd /d %SPRING_DIR% && mvn spring-boot:run --define spring-boot.run.arguments="--spring.profiles.active=dev""
echo Both applications launched in separate terminals

echo Starting Chrome
REM waiting for ng serve to launch
TIMEOUT /T 10 
start chrome http://localhost:4200/login

echo Closing now
TIMEOUT /T 10