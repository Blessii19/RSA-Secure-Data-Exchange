import socket

from rsa_crypto import generate_keys, decrypt_message


# ============================================================
# SERVER CONFIGURATION
# ============================================================

HOST = "0.0.0.0"
PORT = 5000


# ============================================================
# RSA SECURE DATA EXCHANGE - SERVER
# ============================================================

print("=" * 60)
print("          RSA SECURE DATA EXCHANGE - SERVER")
print("=" * 60)
print()

# Generate RSA keys
private_key, public_key = generate_keys()

print("RSA keys generated successfully.")
print("Server is ready.")
print()

# ============================================================
# CREATE SERVER SOCKET
# ============================================================

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server_socket.bind(
    (HOST, PORT)
)

server_socket.listen(5)

print("Server is listening on port:", PORT)
print("Server IP: All available network interfaces")
print()
print("Waiting for client connection...")
print()


# ============================================================
# ACCEPT CLIENT
# ============================================================

try:

    while True:

        connection = None

        try:

            connection, address = server_socket.accept()

            client_ip = address[0]
            client_port = address[1]

            print("Client connected!")
            print("Client IP   :", client_ip)
            print("Client Port :", client_port)
            print()

            # ------------------------------------------------
            # SEND PUBLIC KEY
            # ------------------------------------------------

            connection.sendall(
                public_key
            )

            print("Public key sent to client.")
            print("Waiting for encrypted messages...")
            print()

            # ------------------------------------------------
            # RECEIVE MESSAGES
            # ------------------------------------------------

            while True:

                try:

                    encrypted_data = connection.recv(
                        4096
                    )

                except ConnectionResetError:

                    print()
                    print("Client closed the connection.")
                    print("Connection ended safely.")
                    print()

                    break

                if not encrypted_data:

                    print()
                    print("Client disconnected.")
                    print()

                    break

                encrypted_text = encrypted_data.decode()

                # ------------------------------------------------
                # EXIT COMMAND
                # ------------------------------------------------

                if encrypted_text == "EXIT":

                    print()
                    print("Client requested to close the connection.")
                    print()

                    break

                # ------------------------------------------------
                # DISPLAY ENCRYPTED DATA
                # ------------------------------------------------

                print("Encrypted data received:")
                print(encrypted_text)
                print()

                # ------------------------------------------------
                # RSA DECRYPTION
                # ------------------------------------------------

                try:

                    decrypted_message = decrypt_message(
                        encrypted_text,
                        private_key
                    )

                    print("Decrypted message:")
                    print(decrypted_message)
                    print()

                    # ------------------------------------------------
                    # SEND RESPONSE
                    # ------------------------------------------------

                    response = (
                        "Message received and decrypted successfully."
                    )

                    connection.sendall(
                        response.encode()
                    )

                    print("Waiting for next message...")
                    print()

                except Exception as error:

                    print("Decryption failed:")
                    print(error)
                    print()

                    try:

                        connection.sendall(
                            b"Message decryption failed."
                        )

                    except Exception:

                        pass

                    break

        except ConnectionResetError:

            print()
            print("Client connection was closed.")
            print()

        except Exception as error:

            print()
            print("Connection error:")
            print(error)
            print()

        finally:

            if connection is not None:

                try:
                    connection.close()
                except Exception:
                    pass

            print("Waiting for client connection...")
            print()

except KeyboardInterrupt:

    print()
    print("Server stopped by user.")

finally:

    try:
        server_socket.close()
    except Exception:
        pass

    print("Server socket closed.")
