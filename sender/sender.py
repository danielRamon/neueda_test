import os
import socket
import pickle
import json
from dicttoxml import dicttoxml
from cryptography.fernet import Fernet

secret_key = "./secret.key"
json_file_path = "./json_file"
xml_file_path = "./xml_file"
xml_encrypted_path = "."


def send_xml(file_xml):
    """
    It sends a file to remote machine encrypting the title.
    :param file_xml: Path of file to send (absolute or relative)
    :type file_xml: str
    :return: None
    """
    buffer_size = 4096
    host = "receiver"
    port = 5000

    soc = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    soc.connect((host, port))
    print("[+] Connected.")
    if file_xml:
        soc.send(encrypt_message(str(file_xml).encode()))
        with open(file_xml, "rb") as f:
            while True:
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    print(f"[+] File {file_xml} sended.")
                    break
                soc.sendall(bytes_read)
                print(f"[+] Sending {file_xml}.")
    else:
        soc.sendall(b"")


def sync_receiver():
    global xml_file_path

    server_host = "0.0.0.0"
    server_port = 5001
    buffer_size = 4096

    soc = socket.socket()
    soc.bind((server_host, server_port))
    soc.listen(5)
    print(f"[*] Listening as {server_host}:{server_port}")
    client_socket, address = soc.accept()
    print(f"[+] {address} is connected.")
    receiver_file = pickle.loads(client_socket.recv(buffer_size))
    sender_file = os.listdir(xml_file_path)

    for file in sender_file:
        if file not in receiver_file and file.endswith(".xml"):
            return f"{xml_file_path}/{file}"
    return None


def xml_file_sync(folder_path):
    """
    It checks if there are JSON's files modified or added since last time in the indicated path.
    :param folder_path: Folder path to analyse (relative or absolute)
    :type folder_path: str
    :return: [json_file1, ..., json_fileN]
    """

    json_to_convert = []
    for file in os.listdir(folder_path):
        if file.replace(".json", ".xml") not in os.listdir() and os.path.splitext(file)[1] == ".json":
            json_to_convert.append(f"{folder_path}/{file}")
    return json_to_convert


def json_to_xml(json_file):
    """
    Convert a file with JSON format into XML.
    :param json_file: Path of JSON file (absolute or relative)
    :type json_file: str
    :return: None
    """
    with open(json_file) as json_text:
        try:
            json_dict = json.load(json_text)
            dict_xml = dicttoxml(json_dict)
            return dict_xml
        except json.decoder.JSONDecodeError:
            print("json_file is not correctly json formatted")


def encrypt_message(message):
    """
    It encrypts a message given using a secret key
    :param message: Message to encrypt
    :type message: bytes
    :return: bytes
    """
    global secret_key

    key = open(secret_key, "rb").read()
    f = Fernet(key)
    encrypted_message = f.encrypt(message)
    return encrypted_message


if __name__ == "__main__":
    while True:
        json_list = xml_file_sync(json_file_path)
        if json_list:
            for json_element in json_list:
                xml_conversion = json_to_xml(json_element)
                if xml_conversion:
                    xml_path = f"{xml_file_path}/{os.path.splitext(os.path.basename(json_element))[0]}.xml"
                    with open(xml_path, "wb") as xml_doc:
                        xml_doc.write(xml_conversion)
        send_xml(sync_receiver())

        #             xml_encrypt_path = f"{xml_encrypted_path}/{os.path.splitext(os.path.basename(json_element))[0]}.xml"
        #             with open(xml_encrypt_path, "wb") as xml_enc:
        #                 xml_enc.write(encrypt_message(xml_conversion))
        #                 print(f"{json_element} has been encrypted in {xml_encrypt_path}")
        #             send_xml(xml_encrypt_path)
        #             os.remove(xml_encrypt_path)
        # sync_receiver()
