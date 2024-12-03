import socket
import threading 
import json 
import requests 

clients = {}

# Inside the connection_thread function
def connection_thread(sock, client_name, id):
    print(f">> Start of thread #{id} for {client_name}")
    clients[sock] = client_name 

    while True: 
        try: 
            data = sock.recv(1024).decode('utf-8')  # Use 'utf-8' here
            if not data:
                break
        
            if data == 'Get_top_headlines':
                sock.sendall('Give a keyword for the top headlines:'.encode('utf-8'))  # Use 'utf-8' here
                key = sock.recv(1024).decode('utf-8')  # Use 'utf-8' here
                
                data_of_headlines = fetch_top_headlines(key)
                sock.sendall(data_of_headlines.encode('utf-8'))  # Use 'utf-8' here
                
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    sock.close()         
    print('The connection has ended with client:', client_name)
    print(">> End of Thread no.", id)
    print(50 * '-')

    
def fetch_top_headlines(keyword):
    key_val = '91b9c661fbeb441b958b81ab827689d2'
    URL = f"https://newsapi.org/v2/top-headlines?{keyword}&apiKey={key_val}"
    response = requests.get(URL)
    response.raise_for_status()
    result = response.json()
    articles = result.get('articles', [])
    send_articles = []

    for i, article in enumerate(articles[:15], start=1):
        title = article.get('title', '??')
        description = article.get('description', '??')
        url = article.get('url', '#')

        send_articles.append(f"Article {i}:")
        send_articles.append(f"Title: {title}")
        send_articles.append(f"Description: {description}")
        send_articles.append(f"Read more: {url}")
        send_articles.append("")  # Add a blank line for better readability

    return "\n".join(send_articles)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss: 
    ss.bind(("127.0.0.1", 49999)) 
    ss.listen(3)
    print("The server has started and is waiting for clients to connect...")

    while True: 
        sock_add, sock_name = ss.accept()
        print('The request has been accepted from', sock_name[0], "That has this port number:", sock_name[1])
        the_thread = threading.Thread(target=connection_thread, args=(sock_add, sock_name[0], len(clients) + 1))
        the_thread.start()