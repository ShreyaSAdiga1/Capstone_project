import os

SECRET_KEY = os.urandom(24)
DB_CONFIG={
        'host':"10.10.1.185",
        'port':3306,
        'user':'root',
        'password':"root",
        'database':"capstone_lilly"   
}
# DB_CONFIG={
#         'host':"localhost",
#         'port':3306,
#         'user':'root',
#         'password':"SHREYASQL",
#         'database':"capstone_lilly"   
# }