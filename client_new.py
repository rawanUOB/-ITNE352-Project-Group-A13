import socket
import tkinter as tk
from tkinter import messagebox, Text, Scrollbar

#IT WORKSSSS
class NewsClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("News Client")
        self.server_address = ('127.0.0.1', 49999)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.create_widgets()
        self.connect_to_server()

    def create_widgets(self):
        # Username input section
        self.label = tk.Label(self.master, text="Enter your username:")
        self.label.pack(pady=10)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.send_username)
        self.connect_button.pack(pady=10)

        # Results display area
        self.results_text = Text(self.master, width=60, height=20)
        self.results_text.pack(pady=10)

        self.scrollbar = Scrollbar(self.master, command=self.results_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=self.scrollbar.set)

        # Input for choices and queries
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack(pady=5)

        self.main_menu_frame = None

    def connect_to_server(self):
        try:
            self.client_socket.connect(self.server_address)
            self.results_text.insert(tk.END, "Connected to server.\n")
        except Exception as e:
            messagebox.showerror("Error", f"Could not connect to server: {e}")

    def send_username(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        self.client_socket.sendall(username.encode('utf-8'))
        self.results_text.insert(tk.END, f"Welcome, {username}!\n")
        self.username_entry.config(state='disabled')
        self.connect_button.config(state='disabled')
        self.show_main_menu()

    def show_main_menu(self):
        self.results_text.insert(tk.END, "Choose:\n1 - Headlines\n2 - Sources\n3 - Quit\n")
        self.input_entry.focus()
        self.master.bind("<Return>", self.handle_main_menu_choice)

    def handle_main_menu_choice(self, event):
        choice = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if choice == '1':
            self.get_headlines_menu()
        elif choice == '2':
            self.get_sources_menu()
        elif choice == '3':
            self.quit()
        else:
            messagebox.showwarning("Warning", "Invalid choice. Please enter 1, 2, or 3.")

    def get_headlines_menu(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Choose:\n1 - Search for keywords\n2 - Search by category\n3 - Search by country\n4 - Back to the main menu\n")
        self.input_entry.focus()
        self.master.bind("<Return>", self.handle_headlines_choice)

    def handle_headlines_choice(self, event):
        choice = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if choice in ['1', '2', '3']:
            key = ['q=', 'category=', 'country='][int(choice) - 1]
            self.client_socket.sendall(b'Get_top_headlines')
            prombt = self.client_socket.recv(4096).decode('utf-8')
            self.results_text.insert(tk.END, prombt)
            #self.results_text.insert(tk.END, "Enter a keyword:\n")
            self.input_entry.focus()
            self.master.bind("<Return>", lambda e: self.send_keyword(key))
        elif choice == '4':
            self.show_main_menu()
        else:
            messagebox.showwarning("Warning", "Invalid choice.")

    def get_sources_menu(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Choose:\n1 - Search by category\n2 - Search by country\n3 - Search by language\n4 - Back to the main menu\n")
        self.input_entry.focus()
        self.master.bind("<Return>", self.handle_sources_choice)

    def handle_sources_choice(self, event):
        choice = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if choice in ['1', '2', '3']:
            key = ['category=', 'country=', 'language='][int(choice) - 1]
            self.client_socket.sendall(b'Get_sources')
            prombt = self.client_socket.recv(4096).decode('utf-8')
            self.results_text.insert(tk.END, prombt)
            #self.results_text.insert(tk.END, "Enter a keyword:\n")
            self.input_entry.focus()
            self.master.bind("<Return>", lambda e: self.send_keyword(key))
        elif choice == '4':
            self.show_main_menu()
        else:
            messagebox.showwarning("Warning", "Invalid choice.")

    def send_keyword(self, key):
        query = self.input_entry.get().strip()
        if query:
            send_query = key + query
            self.client_socket.sendall(send_query.encode('utf-8'))
            self.receive_results()  # Call to process the results

    def receive_results(self):
        try:
            results = self.client_socket.recv(4096).decode('utf-8')
            self.results_text.insert(tk.END, "\nResults received from the server:\n")

            #specific_request = self.client_socket.recv(1024).decode('utf-8')
            self.results_text.insert(tk.END, results + "\n")
            specific_message = self.client_socket.recv(4096).decode('utf-8')
            self.results_text.insert(tk.END,specific_message)
            self.results_text.insert(tk.END, "Enter the number of your choice:\n")
            self.input_entry.delete(0, tk.END)
            self.input_entry.focus()
            self.master.bind("<Return>", self.handle_specific_choice)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def handle_specific_choice(self, event):
        specific_choice = self.input_entry.get().strip()
        if specific_choice.isdigit():
            self.client_socket.sendall(specific_choice.encode('utf-8'))
            details = self.client_socket.recv(4096).decode('utf-8')
            self.results_text.insert(tk.END, "\nDetailed information:\n" + details + "\n")
            self.show_main_menu()
        else:
            messagebox.showwarning("Warning", "Please enter a valid number.")

    def quit(self):
        self.client_socket.sendall(b'QUIT')
        self.client_socket.close()
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NewsClientGUI(root)
    root.mainloop()
