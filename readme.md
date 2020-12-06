# MyCart

MyCart is a basic e-commerce app.

## Database Setup

MySQL database has been used in this project.
If you do not have MySQL installed.
Please click [here](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) to install it.

After successfully installing it.

#### Follow these steps

```
$ sudo mysql
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
mysql > CREATE DATABASE temp_db;

mysql > USE temp_db;
```

## Python setup

Installation instruction [click here](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu)

For virtual environment [click here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


## Project setup

```
$ pip3 install -r requirements.txt
```

## Run app
```
$ python3 task.py
```
This will create all tables, if not existed. But inorder to use app we must create two types of user one is admin and other is customer.

## Create admin and customer user 

###### Now reconnect database using newly created user
```
$ mysql -u test-user -p
```
then enter the password as 12345678

```
mysql > USE temp_db;

-- 
mysql > INSERT INTO User (user_name, user_email, password, is_admin) VALUES ('admin', 'admin@gmail.com', '123456', True);

mysql > INSERT INTO User (user_name, user_email, password, is_admin) VALUES ('shahrukh', 'shoaibtayyab121@gmail.com', '123456', False);
```

## Re-run app:
```
$ python3 task.py
```
Now the app is ready to use.

###### Hope you like it.
