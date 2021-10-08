import os
import socket
import pickle
from cryptography.fernet import Fernet, InvalidToken

secret_key = "./secret.key"


def receiving_xml():
    """
    It receive a file via socket, decrypt and save it.
    :return: None
    """
    server_host = "0.0.0.0"
    server_port = 5000
    buffer_size = 4096

    message_complete = b""

    with socket.socket() as soc:
        soc.bind((server_host, server_port))
        soc.listen(5)
        print(f"[*] Listening as {server_host}:{server_port}")
        client_socket, address = soc.accept()
        print(f"[+] {address} is connected.")
        filename = client_socket.recv(buffer_size)
        if filename != b"None":
            filename = os.path.basename(decrypt_message(filename).decode())
            print("[+]File received: " + filename)
            while True:
                bytes_read = client_socket.recv(buffer_size)
                if len(bytes_read) < buffer_size:
                    break
                message_complete += bytes_read
            with open(f"./xml_file/{filename}", "wb") as f:
                try:
                    f.write(decrypt_message(message_complete))
                    print("[+]Content received: " + filename)
                except TypeError:
                    print("WARNING: Something was wrong with the message")

        with open("./list_of_xml", "wb") as list_file:
            list_file.write(pickle.dumps(os.listdir("./xml_file")))
        with open("./list_of_xml", "rb") as list_file:
            while True:
                bytes_read = list_file.read(buffer_size)
                if not bytes_read:
                    print(f"[+] File list of xml sended.")
                    break
                client_socket.sendall(bytes_read)
                print(f"[+] Sending list of xml.")
        os.remove("./list_of_xml")


# def sync_sender():
#
#     buffer_size = 4096
#     host = "sender"
#     port = 5001
#
#     with socket.socket() as soc:
#         print(f"[+] Connecting to {host}:{port}")
#         soc.connect((host, port))
#         print("[+] Connected.")
#         soc.sendall(pickle.dumps(os.listdir("./xml_file")))


def decrypt_message(encrypted_message):
    """
    It decrypt a message using a secret key.
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
