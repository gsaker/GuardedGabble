from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

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

def encryptMessage(message, recipientPublicKeyPEM):
    # Load the public key from the PEM file
    recipientPublicKey = serialization.load_pem_public_key(
        recipientPublicKeyPEM,
        backend=default_backend()
    )
    # Encrypt the message using the public key
    encrypted = recipientPublicKey.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def signMessage(message, senderPrivateKeyPEM):
    # Load the private key from the PEM file
    senderPrivateKey = serialization.load_pem_private_key(
        senderPrivateKeyPEM,
        password=None,
        backend=default_backend()
    )
    # Sign the message using the private key
    signature = senderPrivateKey.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
def decryptMessage(encryptedMessage, recipientPrivateKeyPEM):
    # Load the private key from the PEM file
    recipientPrivateKey = serialization.load_pem_private_key(
        recipientPrivateKeyPEM,
        password=None,
        backend=default_backend()
    )
    # Decrypt the message using the private key
    return recipientPrivateKey.decrypt(
        encryptedMessage,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
def verifySignature(message, signature, senderPublicKeyPEM):
    try:
        # Load the public key from the PEM file
        senderPublicKey = serialization.load_pem_public_key(senderPublicKeyPEM)
        # Verify the signature using the public key
        senderPublicKey.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # If the signature is valid, return True
        return True
    # If the signature is invalid, return False
    except InvalidSignature:
        return False