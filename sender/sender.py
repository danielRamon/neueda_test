import os
import socket
import time
import json
from dicttoxml import dicttoxml
from cryptography.fernet import Fernet

last_modification = 0

secret_key = "./secret.key"
json_file_path = "./json_file"
xml_file_path = "./xml_file"
xml_encrypted_path = "/temp/xml_encrypted/"


def send_xml(file_xml):
    """
    It sends a file to remote machine encrypting the title.
    :param file_xml: Path of file to send (absolute or relative)
    :type file_xml: str
    :return: None
    """
    buffer_size = 4096
    host = "neuedascript-receiver-1"
    port = 5000

    soc = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    soc.connect((host, port))
    print("[+] Connected.")
    soc.send(encrypt_message(str(file_xml).encode()))
    with open(file_xml, "rb") as f:
        while True:
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                break
            soc.sendall(bytes_read)


def reading_new_json(folder_path):
    """
    It checks if there are JSON's files modified or added since last time in the indicated path.
    :param folder_path: Folder path to analyse (relative or absolute)
    :type folder_path: str
    :return: [json_file1, ..., json_fileN]
    """
    global last_modification

    newest_modification = 0

    json_to_convert = []
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            path_json = f"{folder_path}/{file}"
            if last_modification < os.stat(path_json).st_mtime:
                json_to_convert.append(path_json)
                newest_modification = max(newest_modification, os.stat(path_json).st_mtime)
    last_modification = newest_modification if newest_modification != 0 else last_modification
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
    print(type(encrypted_message))
    return encrypted_message


if __name__ == "__main__":
    while True:
        json_list = reading_new_json(json_file_path)
        if json_list:
            for json_element in json_list:
                xml_conversion = json_to_xml(json_element)
                if xml_conversion:
                    xml_path = f"{xml_file_path}/{os.path.splitext(os.path.basename(json_element))[0]}.xml"
                    with open(xml_path, "wb") as xml_doc:
                        xml_doc.write(xml_conversion)
                    xml_encrypt_path = f"{xml_encrypted_path}/{os.path.splitext(os.path.basename(json_element))[0]}.xml"
                    with open(xml_encrypt_path, "wb") as xml_enc:
                        xml_enc.write(encrypt_message(xml_conversion))
                        print(f"{json_element} has been encrypted in {xml_encrypt_path}")
                    send_xml(xml_encrypt_path)
