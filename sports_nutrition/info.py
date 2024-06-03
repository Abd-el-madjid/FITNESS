# info.py

from cryptography.fernet import Fernet
import os

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'assurini.noreply@gmail.com'
EMAIL_HOST_PASSWORD = 'jdjhtgvcxwfvlgBHBiyyi-tt_gihbddzldizi_çojoi'
EMAIL_PORT = 587



# Generate a Fernet key
SECRET_KEY = Fernet.generate_key()

# Initialize the cipher suite with the secret key
cipher_suite = Fernet(SECRET_KEY)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data
