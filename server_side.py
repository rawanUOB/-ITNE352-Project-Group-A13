import socket
import threading 
import json 
import requests 

clients = {} #here is a dictionary to save the client's information in

def connection_thread(sock, client_name, id):
    print(f">> Start of thread #{id} for {client_name}")
    clients[sock] = client_name 

    while True: 
        try: 
            data = sock.recv(1024).decode('utf-8')  
            if not data:
                break
        
            if data == 'Get_top_headlines':
                sock.sendall('Give a keyword for the top headlines:'.encode('utf-8')) 
                key = sock.recv(1024).decode('utf-8')  
                
                data_of_headlines = fetch_top_headlines(key)
                sock.sendall(data_of_headlines.encode('utf-8'))

            if data == 'Get_sources' : 
                sock.sendall('Give a keyword for the source:'.encode('utf-8')) 
                key = sock.recv(1024).decode('utf-8')
                print(key)

                data_of_sources = fetch_source(key)
                print("data has been fetched")    
                sock.sendall(data_of_sources.encode('utf-8')) 
                print("data has been sent")

                
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    sock.close()         
    print('The connection has ended with client:', client_name)
    print(">> End of Thread no.", id)
    print(50 * '-')


#This function for the top headlines     
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
        send_articles.append("")  

    return "\n".join(send_articles)

#This function for the sources 
def fetch_source(keyword): 
    key_val = '91b9c661fbeb441b958b81ab827689d2'
    URL = f"https://newsapi.org/v2/sources?{keyword}&apiKey={key_val}"
    response = requests.get(URL)
    response.raise_for_status()
    result = response.json()
    
    sources = result.get('sources', [])
    send_sources = [] #the sources will be saved in this list 

    for i, source in enumerate(sources[:15], start=1):
        id = source.get('id', '??')  
        name = source.get('name', '??')
        description = source.get('description', '??')
        category = source.get('category', '??')
        language = source.get('language', '??')
        url = source.get('url', '#')

        send_sources.append(f"Source {i}:")
        send_sources.append(f"ID: {id}")
        send_sources.append(f"Name: {name}")
        send_sources.append(f"Description: {description}")
        send_sources.append(f"Category: {category}")
        send_sources.append(f"Language: {language}")
        send_sources.append(f"Read more: {url}")
        send_sources.append("")  

    return "\n".join(send_sources) # The list will be sent to the user


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss: 
    ss.bind(("127.0.0.1", 49999)) 
    ss.listen(3)
    print("The server has started and is waiting for clients to connect...")

    while True: 
        sock_add, sock_name = ss.accept()
        print('The request has been accepted from', sock_name[0], "That has this port number:", sock_name[1])
        the_thread = threading.Thread(target=connection_thread, args=(sock_add, sock_name[0], len(clients) + 1))
        the_thread.start()