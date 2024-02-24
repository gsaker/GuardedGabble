from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generateKeys():
    # Generate private and public keys
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Get the public key from the private key
    publicKey = privateKey.public_key()
    # Serialize the private and public keys to PEM format
    # This is so they can be saved to a file
    pemPrivate = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    pemPublic = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Return the private and public keys
    return pemPrivate, pemPublic
generateKeys()