from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def generate_keys():
    """
    Generate a 2048-bit RSA public and private key.
    """

    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return private_key, public_key


def encrypt_message(message, public_key):
    """
    Encrypt a message using the receiver's public key.
    """

    key = RSA.import_key(public_key)

    cipher = PKCS1_OAEP.new(key)

    encrypted_data = cipher.encrypt(
        message.encode("utf-8")
    )

    encrypted_message = base64.b64encode(
        encrypted_data
    ).decode("utf-8")

    return encrypted_message


def decrypt_message(encrypted_message, private_key):
    """
    Decrypt a message using the receiver's private key.
    """

    key = RSA.import_key(private_key)

    cipher = PKCS1_OAEP.new(key)

    encrypted_data = base64.b64decode(
        encrypted_message.encode("utf-8")
    )

    decrypted_data = cipher.decrypt(
        encrypted_data
    )

    return decrypted_data.decode("utf-8")


def test_rsa():
    """
    Test RSA encryption and decryption.
    """

    print("=" * 60)
    print("              RSA ENCRYPTION TEST")
    print("=" * 60)

    print("\nGenerating RSA keys...")

    private_key, public_key = generate_keys()

    print("RSA keys generated successfully.")

    message = input(
        "\nEnter a message to encrypt: "
    )

    encrypted_message = encrypt_message(
        message,
        public_key
    )

    print("\nEncrypted Message:")
    print(encrypted_message)

    decrypted_message = decrypt_message(
        encrypted_message,
        private_key
    )

    print("\nDecrypted Message:")
    print(decrypted_message)

    if message == decrypted_message:
        print("\n✓ RSA encryption and decryption successful!")
    else:
        print("\n✗ RSA encryption and decryption failed!")


if __name__ == "__main__":
    test_rsa()
