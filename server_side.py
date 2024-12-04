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
                
                data_of_headlines, detailed_informations = fetch_top_headlines(key)
                sock.sendall(data_of_headlines.encode('utf-8'))

                #After sending the top 15 headlines I'll ask the client about which article they want to know more and then send it to them
                sock.sendall(('Please choose the article number you want').encode('utf-8'))
                specific_selection = int(sock.recv(1024).decode('utf-8') )-1 

                source, author, title, description,url, publication = detailed_informations[specific_selection]
                detailed_send = (
                    f"Source: {source} \n" 
                    f"Author: {author}\n"
                    f"Title: {title}\n"
                    f"URL: {url}\n"
                    f"Description: {description}\n"
                    f"Publication: {publication}\n"
                )
                sock.sendall(detailed_send.encode('utf-8'))

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
    detailed_articales = [] #save all informations but will not send it to the user from the beginning 

    for i, article in enumerate(articles[:15], start=1):
        source = article.get('source','??')
        auther = article.get('author','??')
        title = article.get('title', '??')
        description = article.get('description', '??')
        publication = article.get('publishedAt', '??')
        url = article.get('url', '#')

        send_articles.append(f"Article {i}:") 
        send_articles.append(f"source: {source}")
        send_articles.append(f"Auther: {auther}")
        send_articles.append(f"Title: {title}") 
        send_articles.append("")  

        detailed_articales.append((source, auther, title, description,url, publication))

    returned_articles = "\n".join(send_articles)
    return returned_articles , detailed_articales 

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