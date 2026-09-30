import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

from rsa_crypto import generate_keys, decrypt_message


# ============================================================
# SERVER CONFIGURATION
# ============================================================

HOST = "0.0.0.0"
PORT = 5000


# ============================================================
# SERVER GUI
# ============================================================

class RSAServerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "RSA Secure Data Exchange - Server"
        )

        self.root.geometry(
            "950x750"
        )

        self.root.minsize(
            750,
            600
        )

        self.root.configure(
            bg="#eef2f7"
        )

        self.server_socket = None
        self.client_socket = None

        self.private_key = None
        self.public_key = None

        self.server_running = False
        self.client_connected = False

        # ====================================================
        # SCROLLABLE WINDOW
        # ====================================================

        self.canvas = tk.Canvas(
            self.root,
            bg="#eef2f7",
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_frame = tk.Frame(
            self.canvas,
            bg="#eef2f7"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        # ====================================================
        # TITLE
        # ====================================================

        title_frame = tk.Frame(
            self.main_frame,
            bg="#1f3c88",
            height=105
        )

        title_frame.pack(
            fill="x"
        )

        title_label = tk.Label(
            title_frame,
            text="RSA SECURE DATA EXCHANGE",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#1f3c88"
        )

        title_label.pack(
            pady=(18, 2)
        )

        subtitle_label = tk.Label(
            title_frame,
            text="Computer Networks Mini Project - Server",
            font=("Arial", 11),
            fg="white",
            bg="#1f3c88"
        )

        subtitle_label.pack(
            pady=(0, 15)
        )

        # ====================================================
        # SERVER STATUS
        # ====================================================

        status_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        status_frame.pack(
            padx=25,
            pady=20,
            fill="x"
        )

        status_title = tk.Label(
            status_frame,
            text="Server Status",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        status_title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=15,
            pady=12,
            sticky="w"
        )

        # Server IP

        ip_label = tk.Label(
            status_frame,
            text="Server IP:",
            font=("Arial", 11),
            bg="white"
        )

        ip_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=8,
            sticky="w"
        )

        self.ip_value = tk.Label(
            status_frame,
            text="Detecting...",
            font=("Arial", 11, "bold"),
            bg="white"
        )

        self.ip_value.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # Port

        port_label = tk.Label(
            status_frame,
            text="Port:",
            font=("Arial", 11),
            bg="white"
        )

        port_label.grid(
            row=1,
            column=2,
            padx=10,
            pady=8
        )

        self.port_value = tk.Label(
            status_frame,
            text=str(PORT),
            font=("Arial", 11, "bold"),
            bg="white"
        )

        self.port_value.grid(
            row=1,
            column=3,
            padx=10,
            pady=8,
            sticky="w"
        )

        # Status

        self.status_label = tk.Label(
            status_frame,
            text="● Server Starting...",
            font=("Arial", 11, "bold"),
            fg="#f57c00",
            bg="white"
        )

        self.status_label.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=15,
            pady=(5, 15),
            sticky="w"
        )

        # ====================================================
        # CLIENT CONNECTION
        # ====================================================

        client_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        client_frame.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        client_title = tk.Label(
            client_frame,
            text="Client Connection",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        client_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        self.client_status_label = tk.Label(
            client_frame,
            text="● Waiting for client...",
            font=("Arial", 11, "bold"),
            fg="#f57c00",
            bg="white"
        )

        self.client_status_label.pack(
            anchor="w",
            padx=15,
            pady=(0, 15)
        )

        # ====================================================
        # ENCRYPTED DATA
        # ====================================================

        encrypted_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        encrypted_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        encrypted_title = tk.Label(
            encrypted_frame,
            text="Received Encrypted Data",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        encrypted_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.encrypted_text = scrolledtext.ScrolledText(
            encrypted_frame,
            height=7,
            font=("Consolas", 9),
            wrap=tk.WORD
        )

        self.encrypted_text.pack(
            padx=15,
            pady=(0, 15),
            fill="x"
        )

        # ====================================================
        # DECRYPTED MESSAGE
        # ====================================================

        decrypted_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        decrypted_frame.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        decrypted_title = tk.Label(
            decrypted_frame,
            text="Decrypted Message",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        decrypted_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.decrypted_label = tk.Label(
            decrypted_frame,
            text="No message received.",
            font=("Arial", 11),
            bg="white",
            anchor="w",
            justify="left",
            wraplength=850
        )

        self.decrypted_label.pack(
            padx=15,
            pady=(5, 15),
            anchor="w"
        )

        # ====================================================
        # SECURITY INFORMATION
        # ====================================================

        security_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        security_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        security_title = tk.Label(
            security_frame,
            text="Security Information",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        security_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.security_label = tk.Label(
            security_frame,
            text=(
                "RSA Public Key: Generated\n"
                "RSA Private Key: Stored securely on server\n"
                "Encryption: RSA-OAEP\n"
                "Transport Protocol: TCP/IP"
            ),
            font=("Arial", 10),
            bg="white",
            justify="left",
            anchor="w"
        )

        self.security_label.pack(
            padx=15,
            pady=(5, 15),
            anchor="w"
        )

        # ====================================================
        # COMMUNICATION LOG
        # ====================================================

        log_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        log_frame.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        log_title = tk.Label(
            log_frame,
            text="Communication Log",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        log_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=9,
            font=("Consolas", 9),
            state="disabled",
            wrap=tk.WORD
        )

        self.log_text.pack(
            padx=15,
            pady=(0, 15),
            fill="x"
        )

        # ====================================================
        # FOOTER
        # ====================================================

        footer = tk.Label(
            self.main_frame,
            text=(
                "RSA Encryption | RSA Decryption | TCP/IP "
                "| Secure Data Exchange"
            ),
            font=("Arial", 9),
            bg="#eef2f7",
            fg="#555555"
        )

        footer.pack(
            pady=15
        )

        # ====================================================
        # START SERVER
        # ====================================================

        self.add_log(
            "Server application started."
        )

        self.generate_server_keys()

        self.start_server()

        # ====================================================
        # CLOSE EVENT
        # ====================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ========================================================
    # SCROLL FUNCTIONS
    # ========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def update_canvas_width(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ========================================================
    # LOG FUNCTION
    # ========================================================

    def add_log(self, message):

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.log_text.config(
            state="normal"
        )

        self.log_text.insert(
            tk.END,
            f"[{current_time}] {message}\n"
        )

        self.log_text.see(
            tk.END
        )

        self.log_text.config(
            state="disabled"
        )

    # ========================================================
    # GENERATE RSA KEYS
    # ========================================================

    def generate_server_keys(self):

        try:

            self.private_key, self.public_key = (
                generate_keys()
            )

            self.add_log(
                "RSA public/private key pair generated."
            )

            self.status_label.config(
                text="● Server Ready",
                fg="green"
            )

        except Exception as error:

            self.status_label.config(
                text="● Key Generation Failed",
                fg="red"
            )

            self.add_log(
                f"RSA key generation error: {error}"
            )

    # ========================================================
    # START TCP SERVER
    # ========================================================

    def start_server(self):

        try:

            self.server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.server_socket.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            self.server_socket.bind(
                (HOST, PORT)
            )

            self.server_socket.listen(5)

            self.server_running = True

            self.add_log(
                f"TCP server listening on port {PORT}."
            )

            # Start accepting clients in background
            server_thread = threading.Thread(
                target=self.accept_client,
                daemon=True
            )

            server_thread.start()

        except Exception as error:

            self.status_label.config(
                text="● Server Failed",
                fg="red"
            )

            self.add_log(
                f"Server error: {error}"
            )

    # ========================================================
    # ACCEPT CLIENT
    # ========================================================

    def accept_client(self):

        try:

            self.client_socket, address = (
                self.server_socket.accept()
            )

            self.client_connected = True

            client_ip = address[0]
            client_port = address[1]

            self.root.after(
                0,
                lambda: self.client_connected_ui(
                    client_ip,
                    client_port
                )
            )

            # Send public key
            self.client_socket.sendall(
                self.public_key
            )

            self.root.after(
                0,
                lambda: self.add_log(
                    "RSA public key sent to client."
                )
            )

            # Receive messages
            receive_thread = threading.Thread(
                target=self.receive_messages,
                daemon=True
            )

            receive_thread.start()

        except Exception as error:

            if self.server_running:

                self.root.after(
                    0,
                    lambda: self.add_log(
                        f"Client connection error: {error}"
                    )
                )

    # ========================================================
    # CLIENT CONNECTED UI
    # ========================================================

    def client_connected_ui(
        self,
        client_ip,
        client_port
    ):

        self.client_status_label.config(
            text=(
                f"● Client Connected - "
                f"{client_ip}:{client_port}"
            ),
            fg="green"
        )

        self.status_label.config(
            text="● Server Running",
            fg="green"
        )

        self.add_log(
            f"Client connected: "
            f"{client_ip}:{client_port}"
        )

    # ========================================================
    # RECEIVE ENCRYPTED MESSAGE
    # ========================================================

    def receive_messages(self):

        while self.client_connected:

            try:

                encrypted_data = (
                    self.client_socket.recv(4096)
                )

                if not encrypted_data:

                    break

                encrypted_text = (
                    encrypted_data.decode()
                )

                # Exit command
                if encrypted_text == "EXIT":

                    break

                # Display encrypted data
                self.root.after(
                    0,
                    lambda data=encrypted_text:
                    self.display_encrypted_data(data)
                )

                # Decrypt message
                decrypted_message = decrypt_message(
                    encrypted_text,
                    self.private_key
                )

                # Display decrypted message
                self.root.after(
                    0,
                    lambda message=decrypted_message:
                    self.display_decrypted_message(message)
                )

                # Send confirmation
                self.client_socket.sendall(
                    b"Message received and decrypted successfully."
                )

                self.root.after(
                    0,
                    lambda: self.add_log(
                        "Decrypted message successfully."
                    )
                )

            except Exception as error:

                self.root.after(
                    0,
                    lambda: self.add_log(
                        f"Message processing error: {error}"
                    )
                )

                try:

                    self.client_socket.sendall(
                        b"Message decryption failed."
                    )

                except Exception:

                    pass

                break

        self.client_connected = False

        self.root.after(
            0,
            self.client_disconnected_ui
        )

    # ========================================================
    # DISPLAY ENCRYPTED DATA
    # ========================================================

    def display_encrypted_data(
        self,
        encrypted_data
    ):

        self.encrypted_text.delete(
            "1.0",
            tk.END
        )

        self.encrypted_text.insert(
            tk.END,
            encrypted_data
        )

        self.add_log(
            "Encrypted data received from client."
        )

    # ========================================================
    # DISPLAY DECRYPTED MESSAGE
    # ========================================================

    def display_decrypted_message(
        self,
        message
    ):

        self.decrypted_label.config(
            text=message
        )

        self.add_log(
            "Original message recovered using RSA private key."
        )

    # ========================================================
    # CLIENT DISCONNECTED
    # ========================================================

    def client_disconnected_ui(self):

        self.client_status_label.config(
            text="● Client Disconnected",
            fg="red"
        )

        self.add_log(
            "Client disconnected."
        )

    # ========================================================
    # CLOSE SERVER
    # ========================================================

    def close_application(self):

        self.server_running = False
        self.client_connected = False

        try:

            if self.client_socket:
                self.client_socket.close()

        except Exception:

            pass

        try:

            if self.server_socket:
                self.server_socket.close()

        except Exception:

            pass

        self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = RSAServerGUI(
        root
    )

    root.mainloop()
