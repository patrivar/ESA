import random
import story
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='flight_game',
    password='flight_game',
    autocommit=True,
    collation='utf8mb4_general_ci'
)