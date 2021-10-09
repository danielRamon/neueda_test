import os
import time
import socket
import json
from dicttoxml import dicttoxml
from cryptography.fernet import Fernet

secret_key = "/var/key/secret.key"
json_file_path = "./json_file"
xml_file_path = "./xml_file"
xml_encrypted_path = "/tmp/encryption"


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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        print(f"[+] Connecting to {host}:{port}")
        try:
            soc.connect((host, port))
            print("[+] Connected.")
            if file_xml:
                soc.send(encrypt_message(str(file_xml).encode()))
                with open(file_xml, "rb") as f:
                    while True:
                        bytes_read = f.read(buffer_size)
                        if not bytes_read:
                            print(f"[+] File {file_xml} sent.")
                            break
                        soc.sendall(bytes_read)
                        data = soc.recv(buffer_size)
                        print(f"[*] Sending {len(bytes_read)} bytes of {file_xml}.")
            else:
                print("[+] Nothing to send.")
                return False
        except:
            print("[-] ERROR: Connection failed.")
            return False
    return True


def create_encryption(file_name):
    '''
    It take a XML file and encrypt it in the global xml_encrypted_path.
    :param file_name: File XML to encrypt
    :type file_name: str
    :return: str (the encrypted file path)
    '''
    global xml_encrypted_path
    encryption = ""
    with open(file_name, "rb") as file_to_encrypt:
        encryption = encrypt_message(file_to_encrypt.read())
    encrypted_path = f"{xml_encrypted_path}/{os.path.basename(file_name)}"
    with open(encrypted_path, "wb") as file_encrypted:
        file_encrypted.write(encryption)
    return encrypted_path


def xml_file_sync():
    """
    It compare the JSON's files with the XML file and return a list of JSON's file added or modified.
    :param folder_path: Folder path to analyse (relative or absolute)
    :type folder_path: str
    :return: [json_file1, ..., json_fileN]
    """
    global xml_file_path
    global json_file_path

    for file in os.listdir(json_file_path):
        json_to_convert = False
        json_path = f"{json_file_path}/{file}"
        if file.replace(".json", ".xml") not in os.listdir(xml_file_path) or file[0] == ".":
            if os.path.splitext(file)[1] == ".json":
                json_to_convert = True
                # json_to_convert.append(f"{json_file_path}/{file}")
        elif os.path.getmtime(json_path) != os.path.getmtime(f"{xml_file_path}/{file}".replace(".json", ".xml")):
            json_to_convert = True
            # json_to_convert.append(f"{json_file_path}/{file}")
        if json_to_convert:
            xml_conversion = json_to_xml(json_path)
            if xml_conversion:
                xml_path = f"{xml_file_path}/{os.path.splitext(file)[0]}.xml"
                with open(xml_path, "wb") as xml_doc:
                    xml_doc.write(xml_conversion)
                    print(f"[+] {file} has been transform to XML in {xml_path} ")
                os.utime(xml_path, (time.time(), os.path.getmtime(json_path)))
                encrypted_path = create_encryption(xml_path)
                print(f"[+] {xml_path} has been encrypted in {encrypted_path} ")
                while not send_xml(encrypted_path):
                    pass
                print(f"[+] {encrypted_path} has been sent. ")


def json_to_xml(json_file):
    """
    Convert a file with JSON format into XML. If any JSON are incorrectly formated add a ".BadFormat" in the end of the
    file.
    :param json_file: Path of JSON file (absolute or relative)
    :type json_file: str
    :return: None
    """
    try:
        with open(json_file) as json_text:
            json_dict = json.load(json_text)
            dict_xml = dicttoxml(json_dict)
            return dict_xml
    except PermissionError:
        print(f"Something was wrong during open JSON {json_file}")
    except json.decoder.JSONDecodeError:
        print(f"{json_file} is not correctly json formatted")
        os.rename(json_file, f"{json_file}.BadFormat")


def encrypt_message(message):
    """
    It encrypts a message given using a secret key from global secret_key.
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
        xml_file_sync()
