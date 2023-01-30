import socket 
import threading 
import rsa


#generate public and private keys
public_key, private_key = rsa.newkeys(1024)
public_partner = None 

#create socket and conncet to local host IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999)) 

# receive public key from the server then send the generated public key 
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
client.send(public_key.save_pkcs1("PEM"))


def sending_messages(c):
    """this function takes from user input,
       encrypt it with the public key of the sender
       then send it
       """
    while True:
        message = input("")
        #c.send(message.encode())
        # so encrypt the message by the publich key of the partner and send 
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)
        
        
def receiving_messages(c):
    """this function takes from user input,
       dencrypt it with the private key of the reciever
       """
    while True:
        #print("Partner: " + c.recv(1024).decode())
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())
        
threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()


