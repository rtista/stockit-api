GRANT ALL PRIVILEGES ON  inventory_app.* to 'inventory_user'@'localhost' IDENTIFIED BY 'inventory_pass' WITH GRANT OPTION; 

FLUSH PRIVILEGES;

CREATE DATABASE inventory_app;