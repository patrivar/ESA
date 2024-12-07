import random
from flask import Flask, Response, request, jsonify
import json
from flask_cors import CORS
import story
from geopy import distance
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame_1',
    user='root',
    password='K4rhuKu0l131l3n',
    autocommit=True,
    collation='utf8mb4_general_ci'
)

points = 20000
money = 3000
player_range = 2500
attempts = 3
game_over = False
win = False
icao_list = []
letters_found = []
goal_letters = []
goal_word = ""
letter_display = []
word_display = ""


@app.route('/getAirports')
def get_airports():
    sql = """SELECT name, ident, type, iso_country, longitude_deg, latitude_deg 
           FROM airport 
           WHERE continent = 'EU'
           AND type = 'large_airport'
           ORDER BY RAND() LIMIT 22;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def word(missing_letters, goal_word):
    sql = """SELECT word FROM word_list ORDER BY RAND() LIMIT 1;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    rows = cursor.fetchone()
    missing_letters = []
    goal_word = rows['word']
    for i in rows['word']:
        missing_letters.append(i)
    return missing_letters, goal_word


def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


def get_airport_info(icao):
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
                FROM airport
                WHERE ident = %s"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


@app.route('/newGame/<player_name>')
def create_game(player_name):
    all_airports = get_airports()
    start_airport = all_airports[0]['ident']
    current_airport = start_airport

    sql = """INSERT INTO game (money, location, screen_name, points, player_range)
           VALUES (%s,%s,%s,%s,%s);"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (money, current_airport, player_name, points, player_range))
    game_id = cursor.lastrowid

    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    goal_port = all_airports[1:].copy()
    random.shuffle(goal_port)

    for i, goal_id in enumerate(goal_list):
        sql = """INSERT INTO ports(game, airport, goal) 
                VALUES (%s, %s, %s);"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (game_id, goal_port[i]['ident'], goal_id))

    status = 200
    result = {
        "status": status,
        "game_id": game_id,
        "airports": all_airports,
        "current": current_airport,
        "letter": "l"
    }
    json_result = json.dumps(result)
    return Response(json_result, status=status, mimetype='application/json')


@app.route('/flyto')
def flyto():
    args = request.args
    game_id = args.get("game")
    dest = args.get("dest")

    print(f"Received flyto request: Game ID={game_id}, Destination={dest}")

    # Fetch the current game state
    sql = """SELECT * FROM game WHERE id = %s"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (game_id,))
    game_state = cursor.fetchone()
    print(f"Current game state: {game_state}")

    # Update the player's location
    sql = """UPDATE game SET location = %s WHERE id = %s"""
    cursor.execute(sql, (dest, game_id))

    # Fetch the updated game state
    sql = """SELECT * FROM game WHERE id = %s"""
    cursor.execute(sql, (game_id,))
    updated_game_state = cursor.fetchone()
    print(f"Updated game state: {updated_game_state}")

    # Fetch the updated list of airports
    all_airports = get_airports().json

    # Calculate distances and set in_range field
    current_airport = get_airport_info(dest)
    for airport in all_airports:
        dist = calculate_distance(current_airport, airport)
        if dist <= game_state['player_range']:
            airport['in_range'] = True
        else:
            airport['in_range'] = False

    return jsonify({'game_state': updated_game_state, 'all_airports': all_airports})


if __name__ == "__main__":
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
