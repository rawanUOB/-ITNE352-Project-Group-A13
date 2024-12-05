import socket
import json

def display_menu(menu_title, options):
    print(f"\n--- {menu_title} ---")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    try:
        choice = int(input("Enter your choice: "))
        if 1 <= choice <= len(options):
            return choice
        else:
            print("Invalid choice. Try again.")
            return display_menu(menu_title, options)
    except ValueError:
        print("Invalid input. Enter a number.")
        return display_menu(menu_title, options)

def main_menu(client_socket):
    while True:
        options = ["Search Headlines", "Quit"]
        choice = display_menu("Main Menu", options)

        if choice == 1:
            headlines_menu(client_socket)
        elif choice == 2:
            client_socket.sendall(json.dumps({"action": "quit"}).encode())
            print("Disconnected from the server.")
            break

def headlines_menu(client_socket):
    while True:
        options = ["Search by Keywords", "Search by Category", "Back to Main Menu"]
        choice = display_menu("Headlines Menu", options)

        if choice == 3:
            break

        action = "search_keywords" if choice == 1 else "search_category"
        query = input("Enter your search query: ")
        client_socket.sendall(json.dumps({"action": action, "query": query}).encode())

        response = client_socket.recv(4096).decode()
        results = json.loads(response).get("results", [])
        print("\n--- Results ---")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']} (Source: {result['source_name']})")

        try:
            item_choice = int(input("Enter the number to view details, or 0 to go back: "))
            if 1 <= item_choice <= len(results):
                client_socket.sendall(json.dumps({"action": "details", "item_index": item_choice - 1}).encode())
                details_response = client_socket.recv(4096).decode()
                details = json.loads(details_response).get("details", {})
                print("\n--- Details ---")
                for key, value in details.items():
                    print(f"{key.capitalize()}: {value}")
        except ValueError:
            print("Returning to the previous menu.")

def main():
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 49999

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")

        username = input("Enter your username: ")
        client_socket.sendall(username.encode())

        main_menu(client_socket)

    except ConnectionError:
        print("Connection to the server failed.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
