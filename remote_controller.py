import socket
from pynput import keyboard

# Ustaw adres IP ESP8266 i port, na którym działa serwer (zdefiniowany w Arduino)
esp_ip = "192.168.0.115"
port = 80

# Utwórz połączenie socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((esp_ip, port))

print("Connected to ESP8266. Press 'q' to quit.")


def send_command(command):
    client_socket.send((command).encode())
    print("Command sent:", command + "\n")


# Funkcja obsługi klawiszy
def on_press(key):
    try:
        # Sprawdź, czy dany klawisz został wciśnięty
        if key.char == "w":
            send_command("w")
        elif key.char == "s":
            send_command("s")
        elif key.char == "a":
            send_command("a")
        elif key.char == "d":
            send_command("d")
        elif key.char == "q":
            send_command("q")
        elif key.char == "e":
            send_command("e")
        elif key.char == "z":
            send_command("z")
    except AttributeError:
        pass


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Zamknięcie połączenia
client_socket.close()
print("Connection closed.")
