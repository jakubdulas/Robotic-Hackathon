import socket
from pynput import keyboard


def send_command(command, client_socket):
    client_socket.send((command).encode())
    print("Command sent:", command + "\n")


# Funkcja obsługi klawiszy
def on_press(key, client_socket):
    try:
        # Sprawdź, czy dany klawisz został wciśnięty
        if key.char == "w":
            send_command("w", client_socket)
        elif key.char == "s":
            send_command("s", client_socket)
        elif key.char == "a":
            send_command("a", client_socket)
        elif key.char == "d":
            send_command("d", client_socket)
        elif key.char == "q":
            send_command("q", client_socket)
        elif key.char == "e":
            send_command("e", client_socket)
        elif key.char == "z":
            send_command("z", client_socket)
    except AttributeError:
        pass


if __name__ == "__main__":
    # Ustaw adres IP ESP8266 i port, na którym działa serwer (zdefiniowany w Arduino)
    esp_ip = "192.168.0.115"
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
