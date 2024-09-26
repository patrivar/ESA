import random
#import story
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame_1',
    user='root',
    password='moonS20-un14',
    autocommit=True,
    collation='utf8mb4_general_ci'
)

