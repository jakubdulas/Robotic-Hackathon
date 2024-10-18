import socket
from pynput import keyboard


def send_command(command, client_socket):
    client_socket.send((command).encode())
    print("Command sent:", command + "\n")


# Funkcja obsługi klawiszy
def on_press(key, client_socket):
    try:
        send_command(key.char, client_socket)
    except AttributeError:
        pass


if __name__ == "__main__":
    # Ustaw adres IP ESP8266 i port, na którym działa serwer (zdefiniowany w Arduino)
    esp_ip = "192.168.0.119"
    port = 80

    # Utwórz połączenie socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((esp_ip, port))

    print("Connected to ESP8266. Press 'q' to quit.")

    with keyboard.Listener(on_press=lambda x: on_press(x, client_socket)) as listener:
        listener.join()

    # Zamknięcie połączenia
    client_socket.close()
    print("Connection closed.")
