# Foobar

Foobar is a Python library for dealing with word pluralization.

## Database Setup

MySQL database has been used in this project.
If you do not have MySQL installed.
Please click [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) to install it.

After successfully installing it.

#### Follow these steps

```
sudo mysql
```
##### 1. Create a new user

```
mysql > CREATE USER 'test-user'@'localhost' IDENTIFIED BY '12345678';

mysql > GRANT ALL PRIVILEGES ON *.* TO 'test-user'@'localhost' WITH GRANT OPTION;

mysql > FLUSH PRIVILEGES;

mysql > quit
```

##### 2. Create a new database
###### Now reconnect database using newly created user
```
$ mysql -u test-user -p
```
then enter the password as 12345678

```
CREATE DATABASE temp_db;

USE temp_db;
```

## Python setup

Installation instruction [click here](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu)

For virtual environment [click here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


## Project setup

```
pip3 install -r requirements.txt
```
