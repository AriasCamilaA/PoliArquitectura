# Aquí definimos "almacenes" en memoria para demo:
clients = {}
rooms = {}
reservations = {}
invoices = {}

# Contadores simples para IDs
_client_id_seq = 1
_room_id_seq = 1
_reservation_id_seq = 1
_invoice_id_seq = 1

def next_client_id():
    global _client_id_seq
    val = _client_id_seq
    _client_id_seq += 1
    return val

def next_room_id():
    global _room_id_seq
    val = _room_id_seq
    _room_id_seq += 1
    return val

def next_reservation_id():
    global _reservation_id_seq
    val = _reservation_id_seq
    _reservation_id_seq += 1
    return val

def next_invoice_id():
    global _invoice_id_seq
    val = _invoice_id_seq
    _invoice_id_seq += 1
    return val

# Pre-cargar algunas habitaciones para demo
def seed_rooms():
    if len(rooms)==0:
        for num, t, p in [("101","single",50.0),("102","double",80.0),("201","suite",150.0)]:
            rid = next_room_id()
            rooms[rid] = {"id": rid, "number": num, "type": t, "price": p, "available": True}

seed_rooms()
