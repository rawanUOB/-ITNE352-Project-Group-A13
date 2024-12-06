import socket
import threading 
import json 
import requests 

clients = {} #here is a dictionary to save the client's information in

def connection_thread(sock, client_id, id):
    print(f">> Start of thread #{id} for {client_id}")
    client_name = sock.recv(1024).decode('utf-8') # I need to save the client name into a JSON file!

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

                name_of_sources, details_source = fetch_source(key) 
                sock.sendall(name_of_sources.encode('utf-8')) 

                #After sending 15 source names the client will choose one of them 
                sock.sendall(('Please choose the source number you want to recieve more informations about').encode('utf-8'))
                specified = int(sock.recv(1024).decode('utf-8') )-1 
                
                name,description,category,language,country,url = details_source [specified]
                detailed_source = (
                    f"Name: {name} \n"
                    f"Description: {description} \n"
                    f"Category: {category} \n"
                    f"Language: {language} \n"
                    f"Country: {country} \n"
                    f"URL: {url} \n"
                )

                sock.sendall(detailed_source.encode('utf-8'))

            if data == 'QUIT': 
                sock.close()         
                print('The connection has ended with client:', client_name)
                print(">> End of Thread no.", id)
                print(50 * '-') 

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    


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
    send_sources = [] #The source names will be saved in this list and sent to the client
    detailed_sources = [] # All the other detailes will be saved in here but they'll not be sent 

    for i, source in enumerate(sources[:15], start=1):
        name = source.get('name', '??')  
        description = source.get('description', '??')
        category = source.get('category', '??')
        language = source.get('language', '??')
        country = source.get('country', '??')
        url = source.get('url', '#')

        send_sources.append(f"Source {i}:")
        send_sources.append(f"Name: {name}")
        send_sources.append("")  

        detailed_sources.append((name,description,category,language,country,url))

    returned_sources = "\n".join(send_sources)    
    return returned_sources, detailed_sources # The will return 2 things 


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss: 
    ss.bind(("127.0.0.1", 49999)) 
    ss.listen(3)
    print("The server has started and is waiting for clients to connect...")

    while True: 
        sock_add, sock_name = ss.accept()
        print('The request has been accepted from', sock_name[0], "That has this port number:", sock_name[1])
        the_thread = threading.Thread(target=connection_thread, args=(sock_add, sock_name[0], len(clients) + 1))
        the_thread.start()