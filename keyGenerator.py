from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("sender/secret.key", "wb") as key_sender:
        key_sender.write(key)
    with open("receiver/secret.key", "wb") as key_receiver:
        key_receiver.write(key)

if __name__ == "__main__":
    generate_key()