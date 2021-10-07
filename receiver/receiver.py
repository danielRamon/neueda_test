import os
import socket
from cryptography.fernet import Fernet

secret_key = "./secret.key"


def receiving_xml():
    """
    It receive a file via socket, decrypt and save it.
    :return: None
    """
    server_host = "0.0.0.0"
    server_port = 5000
    buffer_size = 4096

    soc = socket.socket()
    soc.bind((server_host, server_port))
    soc.listen(5)
    print(f"[*] Listening as {server_host}:{server_port}")
    client_socket, address = soc.accept()
    print(f"[+] {address} is connected.")
    filename = client_socket.recv(buffer_size)
    filename = os.path.basename(decrypt_message(filename).decode())

    message_complete = b""
    try:
        while True:
            bytes_read = client_socket.recv(buffer_size)
            if not bytes_read:
                break
            message_complete += bytes_read
    finally:
        client_socket.close()

    with open(f"./xml_file/{filename}", "wb") as f:
        f.write(decrypt_message(message_complete))
        print(f"{filename} has been received")


def decrypt_message(encrypted_message):
    """
    It decrypt a message using a secret key.
    :param encrypted_message: Message to decrypt
    :type encrypted_message: bytes
    :return:
    """
    global secret_key
    key = open(secret_key, "rb").read()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)

    return decrypted_message


if __name__ == "__main__":
    while True:
        receiving_xml()
