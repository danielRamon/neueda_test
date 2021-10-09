import os
import socket
from cryptography.fernet import Fernet, InvalidToken

secret_key = "/var/key/secret.key"


def receiving_xml():
    """
    It receive a file via socket, decrypt and save it.
    :return: None
    """
    server_host = "0.0.0.0"
    server_port = 5000
    buffer_size = 4096

    message_complete = b""

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.bind((server_host, server_port))
        soc.listen(5)
        print(f"[*] Listening as {server_host}:{server_port}")
        client_socket, address = soc.accept()
        with client_socket:
            print(f"[+] {address} is connected.")
            filename = client_socket.recv(buffer_size)
            print("[*]Filename received: " + filename)
            filename = os.path.basename(decrypt_message(filename).decode())
            print("[+]Filename decrypted: " + filename)
            while True:
                bytes_read = client_socket.recv(buffer_size)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
                print(f"[*] Receiving {len(bytes_read)} bytes of {filename}")
                message_complete += bytes_read
    with open(f"./xml_file/{filename}", "wb") as f:
        try:
            print("[*]Content received: " + filename)
            f.write(decrypt_message(message_complete))
            print("[+]Content decrypted: " + filename)
        except TypeError:
            print("WARNING: Something was wrong with the message")


def decrypt_message(encrypted_message):
    """
    It decrypt a message given using a secret key from global secret_key.
    :param encrypted_message: Message to decrypt
    :type encrypted_message: bytes
    :return: None
    """
    global secret_key
    try:
        key = open(secret_key, "rb").read()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)

        return decrypted_message
    except InvalidToken:
        print("WARNING: Something went wrong with token")
        return None


if __name__ == "__main__":
    while True:
        receiving_xml()
