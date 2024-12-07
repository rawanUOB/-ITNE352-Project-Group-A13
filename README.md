# NEWS API Client Server Architecture 
ITNE352 - semester 1 2024-2025 <br />
Section 02 - Group name: A13 <br/> 
Student #1 name and ID: Rawana Aqeel Almahoozi - 202102421 <br />
Student #2 name and ID: Sara Jawan ALDawood - 20191937 

## Table of Contents
1. Project Description
2. Project Requirements
3. How the System Runs
4. Script Description:
    * Server Side Explanation
    * Client Side Explanation
5. Additional Concepts
6. Acknowledgment
7. Conclusion 


## Project Description
This project contains two main parts: a client and a server, the function of the project is that the server will be providing informations for the client as they request in an easy human readable way.

## Project Requirements
#### In the project, several packages that needed to be installed beforehand for the client/server architecture to work seamlessly: 

**1. requests:** </br>
* To handle sending and receiving HTTP requests. </br>

**2. JSON:** </br>
* As it is required to save all clients' names and their requests in a JSON file, it is important to import the json module in this project. </br>

**3. socket:** </br>
* This project is based on TCP client and server sockets, so to handle opening and closing the sockets, we need to import it in the code. </br>

**4. threading:** </br>
* The reason importing this module is necessary is that the server must be able to handle at least three clients at the same time, and to implement threads in the code, necessary modules need to be imported. </br>

**4. tkinter:** </br>
* This module is important in the client code for having a GUI. </br>

#### Other Requirements Before Starting Are: </br>
**1. Connecting to NewsAPI:** </br>
* Sign in to NewsAPI. 
* Retrieve your API key.
* Implement the API key in the server code to be able to fetch data. </br>

**2. Connecting to the Internet** </br>

## How the System Runs
The system is running in a simultaneous way. First, we need to start the server by writing this: python server_side.py in the terminal. After that, the server will be waiting for the client, so we'll write: python client_new.py in the terminal, and the connection will be established.. 

* Here, the server is starting the necessary configurations and waiting for the client: 
>> ss.bind(("127.0.0.1", 49999)) </br>
    ss.listen(3) </br>
    print("The server has started and is waiting for clients to connect...") </br> 

* And here, the client is connecting to the server:
>>self.server_address = ('127.0.0.1', 49999)</br> 
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)




## Script Description:

* ### Server Side Explanation 
**First, we need to make sure the necessary packages are installed as provided in the requirements, and also that Python version 3.6 or higher is installed.**

#### The main functionalities for the server side are: 
1. Has multithreading functionality to handle multiple client requests.
2. Has four functions, each handling a different task: 
    * **def client_data(client_name, option, data):** This function handles the task of saving client name, the option they choose and the data they requested in a JSON file called: {client_name}_{option}_A13.json. 
    * **def connection_thread(sock, client_id, id):** This function handles the multithreading and all connections with the client will be managed inside it. 
    * **def fetch_top_headlines(keyword):** This function handles all the requests related to the top headlines. It will fetch what is requested and send it back to the client in a human readable way. This function will be called from inside the connection_thread(sock, client_id, id) function.
    * **def fetch_source(keyword):** This function, similar to the previous function, handles all the requests related to the sources. It will fetch what is requested and send it back to the client in a human readable way. This function will be called from inside the connection_thread(sock, client_id, id) function.

In summary, the server script will first start and wait for a client to connect. After connecting, it will print out the client name:
>> print (f"{client_name} has requested from top headlines articles about {key}")

And then wait for the client to choose a request (headlines or sources)and print it on the screen:
>> print (f"{client_name} has requested from top headlines articles about {key}")

>> print(f"{client_name} requested more data about article name: {title_detail}")

It will handle it, send 15 articles related to the request, and wait for the client to choose which article they're interested in. Then, it will send detailed information about the selected article (informations will be sent to the client in a human readable way not as a dictionary) and print the client name and the article title they requested on the server screen : 
>> print(f"{client_name} requested more data about article name: {title_detail}")

>> print(f"{client_name} requested more data about : {title_detail}")


The server will also save this information to a JSON file and continue this process until the client chooses QUIT. At that point, the server will terminate the connection and print:
>> print ('The connection has ended with client ', client_name )


* ### Client Side Explanation


## Additional Concepts

## Acknowledgment

## Conclusion




