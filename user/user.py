import pygame
import socket
import threading

WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pilih Batu Gunting Kertas")
font = pygame.font.Font(None, 36)

# Load images
batu = pygame.image.load("image/batu.png")
gunting = pygame.image.load("image/gunting.png")
kertas = pygame.image.load("image/kertas.png")

batu = pygame.transform.scale(batu, (100, 100))
gunting = pygame.transform.scale(gunting, (100, 100))
kertas = pygame.transform.scale(kertas, (100, 100))

# Position
rects = {
    "Batu": screen.blit(batu, (80, 150)),
    "Gunting": screen.blit(gunting, (250, 150)),
    "Kertas": screen.blit(kertas, (420, 150))
}

# Socket Setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.106.78", 5000))  # Ganti dengan IP laptop

player_id = None
result = ""

def receive_thread():
    global player_id, result
    while True:
        try:
            data = client.recv(1024).decode()
            if data.startswith("ID:"):
                player_id = int(data.split(":")[1])
            elif data.startswith("Hasil:"):
                result = data[6:]
        except:
            break

threading.Thread(target=receive_thread, daemon=True).start()

def draw_interface():
    screen.fill(WHITE)
    screen.blit(batu, (80, 150))
    screen.blit(gunting, (250, 150))
    screen.blit(kertas, (420, 150))

    if player_id:
        info_text = f"Anda Pemain {player_id}"
    else:
        info_text = "Menghubungkan ke server..."

    text = font.render(info_text, True, BLACK)
    screen.blit(text, (20, 20))

    if result:
        hasil_text = font.render(result, True, BLACK)
        screen.blit(hasil_text, (20, 70))

    pygame.display.flip()

running = True
while running:
    draw_interface()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 80 < x < 180 and 150 < y < 250:
                client.send("Batu".encode())
            elif 250 < x < 350 and 150 < y < 250:
                client.send("Gunting".encode())
            elif 420 < x < 520 and 150 < y < 250:
                client.send("Kertas".encode())

pygame.quit()
client.close()
