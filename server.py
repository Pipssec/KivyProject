import asyncio
import psycopg2
import websockets
import json
import hashlib


def connectdb():
    conn = psycopg2.connect(user="postgres",
                            password="qwerty",
                            host="127.0.0.1",
                            port="5432",
                            database='main')
    return conn


async def myprofile(websocket, name):
    connection = connectdb()
    cursor = connection.cursor()
    cursor.execute(f'SELECT name_STO, town_STO, phone_number FROM users WHERE login LIKE %s',
                   (name,))
    name_sto = cursor.fetchone()
    dict = {
        'sto_name': name_sto[0],
        'sto_town': name_sto[1],
        'sto_phone': name_sto[2]
    }
    result = json.dumps(dict)
    connection.close()
    await websocket.send(result)


async def listorders(websocket):
    jsons = []
    try:
        connection = connectdb()
        cursor = connection.cursor()
        cursor.execute('SELECT name_order FROM orders')
        orders = cursor.fetchall()
        cursor.execute('SELECT order_town FROM orders')
        towns = cursor.fetchall()
        for order, town in zip(orders, towns):
            jsons.append(
                {
                    'order_name': order[0],
                    'town_name': town[0]
                }
            )
        result = json.dumps(jsons)
        connection.close()
        await websocket.send(result)
    except:
        result = json.dumps(jsons)
        await websocket.send(result)


async def fullinformation(websocket, name_order):
    connection = connectdb()
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM orders WHERE name_order LIKE %s', (name_order,))
    information = cursor.fetchone()
    dict = {
        "name_order": information[0],
        "town": information[2],
        "full_text": information[1],
        "order_obl": information[3],
        "order_car": information[4],
        "order_car_model": information[5],
        "order_car_year": information[6],
        "order_car_fuel": information[7],
        "order_car_username": information[8],
        "order_phone": information[9]
    }
    result = json.dumps(dict)
    connection.close()
    await websocket.send(result)


async def liststo(websocket):
    jsons = []
    try:
        connection = connectdb()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT name_STO FROM users')
            name_STO = cursor.fetchall()
            cursor.execute('SELECT town_STO FROM users')
            town_STO = cursor.fetchall()
            cursor.execute('SELECT phone_number FROM users')
            phone_number = cursor.fetchall()
            if len(name_STO) != 0:
                for i in range(len(name_STO)):
                    name_ST = name_STO[i]
                    town_ST = town_STO[i]
                    phone = phone_number[i]
                    jsons.append({"text": f'{name_ST[0]} {town_ST[0]} {phone[0]}'})
            else:
                pass
        except:
            pass
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()
    except:
        pass


async def registration(websocket, login, passw, passw2, name_STO, oblast, town_STO, phone_number):
    jsons = []
    connection = connectdb()
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users(login text, password text, name_STO text, oblast_STO text, town_STO text, phone_number text );')
    user = [0]
    login = login
    try:
        cursor.execute("SELECT COUNT(login) FROM users WHERE login LIKE %s", (login,))
        user = cursor.fetchone()
    except:
        pass
    name_sto = name_STO
    oblast = oblast
    town_STO = town_STO
    """cursor.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (oblast,))
    obl = cursor.fetchone()
    cursor.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (town_STO,))
    town = cursor.fetchone()"""
    phone_number = phone_number
    if """obl[0] != 0""" and len(name_sto) != 0 and """town[0] != 0""" and len(phone_number) != 0:
        if user[0] != 1:
            if passw == passw2:
                hash_pwd = hashlib.sha224((passw).encode('utf-8')).hexdigest()
                cursor.execute(
                    "INSERT INTO users(login, password, name_STO, oblast_STO, town_STO, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                    [login, hash_pwd, name_sto, oblast, town_STO, phone_number])
                connection.commit()
                jsons.append(
                    {
                        "answer": 'reggood'
                    }
                )
                result = json.dumps(jsons)
                await websocket.send(result)
                connection.close()
            else:
                jsons.append(
                    {
                        "answer": 'regbad'
                    }
                )
                result = json.dumps(jsons)
                await websocket.send(result)
                connection.close()
        else:
            jsons.append(
                {
                    "answer": 'badlog'
                }
            )
            result = json.dumps(jsons)
            await websocket.send(result)
            connection.close()
    else:
        jsons.append(
            {
                "answer": 'badobltown'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()


async def authorization(websocket, name, passw):
    jsons = []
    auth_pass = passw
    auth_name = name
    connection = connectdb()
    cursor = connection.cursor()
    user = 0
    try:
        cursor.execute("SELECT COUNT(login) FROM users WHERE login LIKE %s", (auth_name,))
        user = cursor.fetchone()
    except:
        pass
    cursor.execute(f'SELECT "password" FROM users WHERE login LIKE %s ', (auth_name,))
    hash_pwd = cursor.fetchone()
    if user[0] == 1:
        if auth_pass == hash_pwd[0]:
            jsons.append(
                {
                    "answer": 'authgood'
                }
            )
            result = json.dumps(jsons)
            await websocket.send(result)
            connection.close()
        else:
            jsons.append(
                {
                    "answer": 'authbad'
                }
            )
            result = json.dumps(jsons)
            await websocket.send(result)
            connection.close()
    else:
        jsons.append(
            {
                "answer": 'authbad'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()


async def createorder(websocket, name_ord, text_order, order_town, order_obl, order_car, order_car_model,
                      order_car_year, order_car_fuel, order_username, order_phone):
    jsons = []
    name_ord = name_ord
    text_order = text_order
    order_town = order_town
    order_obl = order_obl
    order_car = order_car
    order_car_model = order_car_model
    order_car_year = order_car_year
    order_car_fuel = order_car_fuel
    order_username = order_username
    order_phone = order_phone
    connection = connectdb()
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS orders(name_order text, text_order text, order_town text, order_oblast text, order_car text, order_car_model text, order_car_year text, order_car_fuel text, order_username text, order_phone text );')
    try:
        cursor.execute('SELECT "name_order" from orders')
        numb = cursor.fetchall()
        number = len(numb) + 1
    except:
        number = 0
    name_order = f'{number}. {name_ord}'
    """cursor.execute("SELECT COUNT(oblast) FROM country WHERE country.oblast=?", (order_obl,))
    obl = cursor.fetchone()
    cursor.execute("SELECT COUNT(town) FROM country WHERE country.town=?", (order_town,))
    town = cursor.fetchone()"""
    if len(name_order) != 0 and len(text_order) != 0 and """obl[0] != 0 and town[0] != 0""" and len(
            order_car) != 0 and len(order_car_model) != 0 and len(order_car_year) != 0 and len(
        order_car_fuel) != 0 and len(order_username) != 0 and len(order_phone) != 0:
        cursor.execute(
            "INSERT INTO orders(name_order, text_order, order_town, order_oblast, order_car, order_car_model,order_car_year, order_car_fuel, order_username, order_phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [name_order, text_order, order_town, order_obl, order_car, order_car_model, order_car_year,
             order_car_fuel, order_username, order_phone])
        connection.commit()
        jsons.append(
            {
                "answer": 'ordergood'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()
    else:
        jsons.append(
            {
                "answer": 'badobltown2'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()


async def loadmenu(websocket):
    jsons = []
    try:
        connection = connectdb()
        jsons.append(
            {
                "answer": 'ok'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)
        connection.close()
    except:
        jsons.append(
            {
                "answer": 'bad'
            }
        )
        result = json.dumps(jsons)
        await websocket.send(result)


async def echo(websocket):
    async for message in websocket:
        parsed = json.loads(message)
        if parsed["method"] == "myprofile":
            await myprofile(websocket, parsed["name"])
        if parsed["method"] == "listorders":
            await listorders(websocket)
        if parsed["method"] == "fullinformation":
            await fullinformation(websocket, parsed["name"])
        if parsed["method"] == "liststo":
            await liststo(websocket)
        if parsed["method"] == "registration":
            await registration(websocket, parsed["login"], parsed["passw"], parsed["passw2"], parsed["name_sto"],
                               parsed["oblast"], parsed["town_STO"], parsed["phone_number"])
        if parsed["method"] == "authorization":
            await authorization(websocket, parsed["name"], parsed["passw"])
        if parsed["method"] == "createorder":
            await createorder(websocket, parsed["name_ord"], parsed["text_order"], parsed["order_town"],
                              parsed["order_obl"], parsed["order_car"], parsed["order_car_model"],
                              parsed["order_car_year"], parsed["order_car_fuel"], parsed["order_username"],
                              parsed["order_phone"])
        if parsed["method"] == "loadmenu":
            await loadmenu(websocket)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())
