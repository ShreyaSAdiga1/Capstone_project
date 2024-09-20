import os

SECRET_KEY = os.urandom(24)
DB_CONFIG={
        'host':"localhost",
        'port':3306,
        'user':'root',
        'password':"SHREYASQL",
        'database':"capstone_lilly"   
}