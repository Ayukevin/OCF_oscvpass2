docker container run -p 127.0.0.1:3307:3306 --name test -d --env-file .env mysql:latest
#docker exec -it test bash
#mysql -h localhost -u root -p; 
#CREATE DATABASES login_db;
#USE login_db;
#CREATE TABLE login(
#created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#id INT AUTO_INCREMENT PRIMARY KEY,
#name VARCHAR(100),
#email VARCHAR(100)
#);



#docker run -it --rm --link test -v $(pwd):/app mysql:latest sh
