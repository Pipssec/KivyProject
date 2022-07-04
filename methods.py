import json
import websockets

url = "ws://localhost:8765"


async def myprofile(name):
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "myprofile",
            "name": name
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def listorders():
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "listorders"
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def registration(login, name_sto, oblast, town_STO, phone_number, passw, passw2):
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "registration",
            "login": login,
            "passw": passw,
            "passw2": passw2,
            "name_sto": name_sto,
            "oblast": oblast,
            "town_STO": town_STO,
            "phone_number": phone_number
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def liststo():
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "liststo"
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def fullinformation(name_order):
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "fullinformation",
            "name": name_order
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def authorization(name, passw):
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "authorization",
            "name": name,
            "passw": passw
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result


async def createorder(name_ord, text_order, order_town, order_obl, order_car, order_car_model, order_car_year,
                      order_car_fuel, order_username, order_phone):
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "createorder",
            "name_ord": name_ord,
            "text_order": text_order,
            "order_town": order_town,
            "order_obl": order_obl,
            "order_car": order_car,
            "order_car_model": order_car_model,
            "order_car_year": order_car_year,
            "order_car_fuel": order_car_fuel,
            "order_username": order_username,
            "order_phone": order_phone
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result

async def loadmenu():
    async with websockets.connect(url) as websocket:
        dict = {
            "method": "loadmenu"
        }
        name_json = json.dumps(dict)
        await websocket.send(name_json)
        result = await websocket.recv()
        return result
