# Inventory Management API

This API is meant to supoort the Android application present in this repository by centralizing its users data.

## Deployment

### Database

The database is MySQL based, MariaDB, and may be installed under Linux OS as show below.

* Yum/Dnf Based

    ```shell
    dnf install mariadb mariadb-server
    ```
    
* Debian Based

    ```shell
    apt-get install mariadb mariadb-server
    ```

You may need to grant access to a specific user and create a database if you do not change the configuration file.

The commands below should help you accomplish the access restrictions mentioned before.

```sql
GRANT ALL PRIVILEGES ON  inventory_app.* to 'inventory_user'@'localhost' IDENTIFIED BY 'inventory_pass' WITH GRANT OPTION;

FLUSH PRIVILEGES;

CREATE DATABASE inventory_app;
```

### API

The API is fairly easy to deploy, just change into the projects api/ directory and install all the requirements in the requirements.txt file with the follwoing command:

```shell
pip install -r requirements.txt
```

The API is executed with the following command:

```shell
python3 run.py
```
