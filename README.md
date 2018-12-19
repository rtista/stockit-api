# Inventory Management API

This API is meant to supoort the Android application present in this repository by centralizing its users data.

## Deployment on Linux

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

## Deployment on Windows

### Database

The database is MySQL based, MariaDB, and may be installed under Linux OS as show below.

1) Download MariaDB installer from their website
    * 32-bit: <https://downloads.mariadb.org/interstitial/mariadb-10.3.11/win32-packages/mariadb-10.3.11-win32.msi/from/http%3A//mirrors.up.pt/pub/mariadb/>
    * 64-bit: <https://downloads.mariadb.org/interstitial/mariadb-10.3.11/winx64-packages/mariadb-10.3.11-winx64.msi/from/http%3A//mirrors.up.pt/pub/mariadb/>

2) Execute the installer as administrator and accept the HeidiSQL installation as it will help you with manual database operations.

3) Proceed along the setup and set a password for the 'root' user which you will remember.

4) You may need to grant access to a specific user and create a database if you do not change the configuration file.

The commands below should help you accomplish the access restrictions mentioned before. You can ue HeidiSQL client to execute the following commands after connecting to the MariaDB instance with the 'root' user and the password you previously set.

```sql
GRANT ALL PRIVILEGES ON  inventory_app.* to 'inventory_user'@'localhost' IDENTIFIED BY 'inventory_pass' WITH GRANT OPTION;

FLUSH PRIVILEGES;

CREATE DATABASE inventory_app;
```

### API

For the API you'll need to install Python 3.6:

1) Download Python 3.6 from the following URL:
    * 32-bit: <https://www.python.org/ftp/python/3.6.7/python-3.6.7.exe>
    * 64-bit: <https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe>

2) Execute the installer as Administrator and check the option 'Add python to PATH variable'

3) Finish the installation.

4) Download the following version of mysqlclient pip package from <https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient> and choose the option which fits your computer's architecture:
    * 32-bit: mysqlclient‑1.3.13‑cp36‑cp36m‑win32.whl
    * 64-bit: mysqlclient‑1.3.13‑cp36‑cp36m‑win_amd64.whl

The API is fairly easy to deploy, open up CMD and change into the projects api/ directory and install all the requirements in the requirements.txt file with the following command:

```shell
pip install -r requirements.txt
```

After this, execute the API with the following command:

```shell
python3 run.py
```