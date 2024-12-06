import socket

def main():
    server_address = ('127.0.0.1', 49999)  # Server IP and port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_address)
        print("Connected to server.")
        
        # Send username
        user = input("Enter username: ")
        client_socket.sendall(user.encode('utf-8'))

        # Main menu
        print("Choose: \n1 - Headlines\n2 - Sources\n3 - Quit")
        choice = input(">> ")

        # Send user's choice to the server
        if choice == '1':
            client_socket.sendall(b'Get_top_headlines')
        elif choice == '2':
            client_socket.sendall(b'Get_sources')
        elif choice == '3':
            client_socket.sendall(b'QUIT')
            client_socket.close()
            print("Connection closed.")
            return
        else:
            print("Invalid choice.")
            client_socket.close()
            return

        # Receive and display server's prompt
        prompt = client_socket.recv(1024).decode('utf-8')
        print(prompt)

        # Send keyword or query to the server
        query = input("Enter a keyword: ")
        client_socket.sendall(query.encode('utf-8'))

        # Receive and display the results
        results = client_socket.recv(4096).decode('utf-8')
        print("\nResults received from the server:")
        print(results)

        # Ask the user to choose a specific item
        specific_request = client_socket.recv(1024).decode('utf-8')
        print(specific_request)
        specific_choice = input(">> ")
        client_socket.sendall(specific_choice.encode('utf-8'))

        # Receive and display detailed information
        details = client_socket.recv(4096).decode('utf-8')
        print("\nDetailed information:")
        print(details)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
