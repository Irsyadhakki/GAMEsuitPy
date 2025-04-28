import socket
import threading

players = {}
choices = {}
lock = threading.Lock()

def handle_client(conn, addr, player_id):
    print(f"Pemain {player_id} terhubung dari {addr}")
    conn.send(f"ID:{player_id}".encode())

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            with lock:
                choices[player_id] = data
                if len(choices) == 2:
                    p1 = choices[1]
                    p2 = choices[2]
                    if p1 == p2:
                        result1 = result2 = "Seri!"
                    elif (p1 == 'Batu' and p2 == 'Gunting') or \
                         (p1 == 'Gunting' and p2 == 'Kertas') or \
                         (p1 == 'Kertas' and p2 == 'Batu'):
                        result1 = "Kamu Menang!"
                        result2 = "Kamu Kalah!"
                    else:
                        result1 = "Kamu Kalah!"
                        result2 = "Kamu Menang!"
                    
                    players[1].send(f"Hasil:{p1} vs {p2} => {result1}".encode())
                    players[2].send(f"Hasil:{p2} vs {p1} => {result2}".encode())
                    choices.clear()
        except:
            break

    conn.close()
    print(f"Pemain {player_id} terputus.")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(2)
    print("Server berjalan di port 5000, menunggu pemain...")

    player_id = 1
    while player_id <= 2:
        conn, addr = server.accept()
        players[player_id] = conn
        threading.Thread(target=handle_client, args=(conn, addr, player_id)).start()
        player_id += 1

start_server()
