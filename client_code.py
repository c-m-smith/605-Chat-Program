import ssl
import socket
import datetime
import hashlib

context = ssl.create_default_context()
context.load_cert_chain(certfile="client.crt", keyfile="client.key")
context.load_verify_locations(cafile="server.crt")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with context.wrap_socket(client_socket, server_hostname='www.example.com') as ssl_socket:
	#Initial Connection
	ssl_socket.connect(('192.168.50.13', 443))
	#Authentication--------------------------------------------------------------------------------------------

	#Gather user input for the code
	user_auth = str(input("Please enter the MFA code: "))

	#Send the auth code
	ssl_socket.send(user_auth.lower().strip().encode())

	#Receive Reply
	auth_reply = str(ssl_socket.recv(1024).decode())
	print(auth_reply)
	if auth_reply.lower().strip() == "success":
		print("Connection Successful - You have entered the chat")
		message = input(" -> ")

		while message.lower().strip() != "-quit":
			ssl_socket.send(message.encode())
			data = ssl_socket.recv(1024).decode()
			print('Received from server: ' + data)

			message = input(" -> ")
	else:
		print("Failure to Authenticate")
		ssl_socket.close()

	ssl_socket.close()
