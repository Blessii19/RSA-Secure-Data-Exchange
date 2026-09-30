import socket
from rsa_crypto import encrypt_message


# Server computer IPv4 address
HOST = "10.119.72.231"

# Server port
PORT = 5000


print("=" * 60)
print("          RSA SECURE DATA EXCHANGE - CLIENT")
print("=" * 60)

print("\nServer IP   :", HOST)
print("Server Port :", PORT)

# Create TCP socket
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

print("\nConnecting to server...")

try:

    # Connect to server
    client_socket.connect((HOST, PORT))

    print("Connected to server successfully.")

    # Receive public key from server
    public_key = client_socket.recv(4096)

    print("\nPublic key received from server.")

    print("\nYou can send multiple messages.")
    print("Type 'exit' to close the connection.")

    while True:

        message = input("\nEnter message: ")

        # Exit the communication
        if message.lower() == "exit":

            client_socket.sendall(
                b"EXIT"
            )

            break

        # Encrypt message using server public key
        encrypted_message = encrypt_message(
            message,
            public_key
        )

        print("\nEncrypted message:")
        print(encrypted_message)

        # Send encrypted message
        client_socket.sendall(
            encrypted_message.encode()
        )

        print("\nEncrypted message sent securely.")

        # Receive confirmation from server
        response = client_socket.recv(4096).decode()

        print("\nServer response:")
        print(response)

except ConnectionRefusedError:

    print("\nERROR: Connection refused.")

    print("\nCheck:")
    print("1. Server is running.")
    print("2. Server IP is correct.")
    print("3. Port 5000 is allowed through Windows Firewall.")
    print("4. Both computers are connected to the same network.")

except TimeoutError:

    print("\nERROR: Connection timed out.")

except Exception as error:

    print("\nERROR:")
    print(error)

finally:

    client_socket.close()

    print("\nConnection closed.")
    print("Client stopped.")
