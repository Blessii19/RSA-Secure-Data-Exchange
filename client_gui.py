import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime

from rsa_crypto import encrypt_message


# ============================================================
# SERVER CONFIGURATION
# ============================================================

HOST = "10.119.72.231"
PORT = 5000


# ============================================================
# CLIENT GUI
# ============================================================

class RSAClientGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("RSA Secure Data Exchange - Client")
        self.root.geometry("950x700")
        self.root.minsize(700, 500)

        self.client_socket = None
        self.public_key = None
        self.connected = False

        self.root.configure(bg="#eef2f7")

        # ====================================================
        # SCROLLABLE MAIN WINDOW
        # ====================================================

        main_canvas = tk.Canvas(
            self.root,
            bg="#eef2f7",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=main_canvas.yview
        )

        main_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Main content frame
        self.main_frame = tk.Frame(
            main_canvas,
            bg="#eef2f7"
        )

        canvas_window = main_canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        # Update scroll region
        def update_scroll_region(event):
            main_canvas.configure(
                scrollregion=main_canvas.bbox("all")
            )

        self.main_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        # Make content width match window
        def update_width(event):
            main_canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        main_canvas.bind(
            "<Configure>",
            update_width
        )

        # Mouse wheel scrolling
        def mouse_scroll(event):
            main_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        main_canvas.bind_all(
            "<MouseWheel>",
            mouse_scroll
        )

        # ====================================================
        # TITLE
        # ====================================================

        title_frame = tk.Frame(
            self.main_frame,
            bg="#1f3c88",
            height=100
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
            text="Computer Networks Mini Project - Client",
            font=("Arial", 11),
            fg="white",
            bg="#1f3c88"
        )

        subtitle_label.pack(
            pady=(0, 15)
        )

        # ====================================================
        # SERVER CONNECTION
        # ====================================================

        connection_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        connection_frame.pack(
            padx=25,
            pady=20,
            fill="x"
        )

        connection_title = tk.Label(
            connection_frame,
            text="Server Connection",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        connection_title.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=15,
            pady=12,
            sticky="w"
        )

        # IP
        ip_label = tk.Label(
            connection_frame,
            text="Server IP:",
            font=("Arial", 11),
            bg="white"
        )

        ip_label.grid(
            row=1,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.ip_entry = tk.Entry(
            connection_frame,
            width=22,
            font=("Arial", 11)
        )

        self.ip_entry.insert(
            0,
            HOST
        )

        self.ip_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=10
        )

        # Port
        port_label = tk.Label(
            connection_frame,
            text="Port:",
            font=("Arial", 11),
            bg="white"
        )

        port_label.grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )

        self.port_entry = tk.Entry(
            connection_frame,
            width=8,
            font=("Arial", 11)
        )

        self.port_entry.insert(
            0,
            str(PORT)
        )

        self.port_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=10
        )

        # Connect button
        self.connect_button = tk.Button(
            connection_frame,
            text="CONNECT",
            font=("Arial", 10, "bold"),
            bg="#2e7d32",
            fg="white",
            width=12,
            command=self.connect_to_server
        )

        self.connect_button.grid(
            row=1,
            column=4,
            padx=15,
            pady=10
        )

        # Status
        self.status_label = tk.Label(
            connection_frame,
            text="● Disconnected",
            font=("Arial", 11, "bold"),
            fg="red",
            bg="white"
        )

        self.status_label.grid(
            row=2,
            column=0,
            columnspan=5,
            padx=15,
            pady=(5, 15),
            sticky="w"
        )

        # ====================================================
        # MESSAGE
        # ====================================================

        message_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        message_frame.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        message_title = tk.Label(
            message_frame,
            text="Message",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        message_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.message_entry = tk.Text(
            message_frame,
            height=5,
            font=("Arial", 11),
            wrap=tk.WORD
        )

        self.message_entry.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.send_button = tk.Button(
            message_frame,
            text="ENCRYPT & SEND",
            font=("Arial", 11, "bold"),
            bg="#1f3c88",
            fg="white",
            width=20,
            height=2,
            command=self.send_message
        )

        self.send_button.pack(
            pady=12
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
            text="Encrypted Data",
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
            height=6,
            font=("Consolas", 9),
            wrap=tk.WORD
        )

        self.encrypted_text.pack(
            padx=15,
            pady=(0, 15),
            fill="x"
        )

        # ====================================================
        # SERVER RESPONSE
        # ====================================================

        response_frame = tk.Frame(
            self.main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        response_frame.pack(
            padx=25,
            pady=5,
            fill="x"
        )

        response_title = tk.Label(
            response_frame,
            text="Server Response",
            font=("Arial", 15, "bold"),
            bg="white"
        )

        response_title.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        self.response_label = tk.Label(
            response_frame,
            text="No response received.",
            font=("Arial", 11),
            bg="white",
            anchor="w",
            justify="left"
        )

        self.response_label.pack(
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
            pady=10,
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
            height=8,
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
            text="RSA Encryption  |  TCP/IP Communication  |  Secure Data Exchange",
            font=("Arial", 9),
            bg="#eef2f7",
            fg="#555555"
        )

        footer.pack(
            pady=15
        )

        # ====================================================
        # INITIAL LOG
        # ====================================================

        self.add_log(
            "Client application started."
        )

        self.add_log(
            "Waiting for server connection..."
        )

        # ====================================================
        # CLOSE EVENT
        # ====================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ========================================================
    # ADD LOG
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
    # CONNECT
    # ========================================================

    def connect_to_server(self):

        if self.connected:

            messagebox.showinfo(
                "Connection",
                "Already connected to the server."
            )

            return

        server_ip = self.ip_entry.get().strip()

        try:

            server_port = int(
                self.port_entry.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Port",
                "Please enter a valid port number."
            )

            return

        if not server_ip:

            messagebox.showerror(
                "Invalid IP",
                "Please enter the server IP address."
            )

            return

        try:

            self.client_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client_socket.connect(
                (server_ip, server_port)
            )

            # Receive public key
            self.public_key = self.client_socket.recv(
                4096
            )

            self.connected = True

            self.status_label.config(
                text="● Connected",
                fg="green"
            )

            self.connect_button.config(
                text="CONNECTED",
                state="disabled"
            )

            self.ip_entry.config(
                state="disabled"
            )

            self.port_entry.config(
                state="disabled"
            )

            self.add_log(
                f"Connected to server {server_ip}:{server_port}"
            )

            self.add_log(
                "RSA public key received from server."
            )

            messagebox.showinfo(
                "Connection Successful",
                "Connected to server successfully."
            )

        except ConnectionRefusedError:

            self.status_label.config(
                text="● Connection Failed",
                fg="red"
            )

            self.add_log(
                "Connection refused by server."
            )

            messagebox.showerror(
                "Connection Error",
                "Could not connect to the server.\n\n"
                "Make sure server.py is running."
            )

        except Exception as error:

            self.status_label.config(
                text="● Connection Failed",
                fg="red"
            )

            self.add_log(
                f"Connection error: {error}"
            )

            messagebox.showerror(
                "Connection Error",
                str(error)
            )

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(self):

        if not self.connected:

            messagebox.showwarning(
                "Not Connected",
                "Please connect to the server first."
            )

            return

        message = self.message_entry.get(
            "1.0",
            tk.END
        ).strip()

        if not message:

            messagebox.showwarning(
                "Empty Message",
                "Please enter a message."
            )

            return

        try:

            # Encrypt message
            encrypted_message = encrypt_message(
                message,
                self.public_key
            )

            # Show encrypted message
            self.encrypted_text.delete(
                "1.0",
                tk.END
            )

            self.encrypted_text.insert(
                tk.END,
                encrypted_message
            )

            # Send encrypted message
            self.client_socket.sendall(
                encrypted_message.encode()
            )

            self.add_log(
                "Message encrypted using RSA public key."
            )

            self.add_log(
                "Encrypted message sent to server."
            )

            # Receive server response
            response = self.client_socket.recv(
                4096
            ).decode()

            self.response_label.config(
                text=response
            )

            self.add_log(
                "Server confirmation received."
            )

            # Clear message
            self.message_entry.delete(
                "1.0",
                tk.END
            )

        except Exception as error:

            self.add_log(
                f"Transmission error: {error}"
            )

            messagebox.showerror(
                "Transmission Error",
                str(error)
            )

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        if self.connected:

            try:

                self.client_socket.sendall(
                    b"EXIT"
                )

            except Exception:
                pass

            try:

                self.client_socket.close()

            except Exception:
                pass

        self.root.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = RSAClientGUI(
        root
    )

    root.mainloop()
