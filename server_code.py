import ssl
import socket
import datetime
import hashlib

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile="server.crt", keyfile="server.key")
context.load_verify_locations(cafile="client.crt")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.50.13', 443))
server_socket.listen(5)

with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
	#Running the server
	print("SSL server is running...")
	connection, address = ssl_socket.accept()

	#Awaiting Connections
	print(f"Connection attempt from {address}")

	#Authentication----------------------------------------------------------------------------------
	SECRET = "094f48b26e71f43accf38a26c27ce66d7295be36ec1ffde35ca8ff4604959faf"

	#Get the random operator - the date
	date = datetime.datetime.now()
	concat = SECRET + date.strftime("%Y%m%d")

	#Hash the date to the secret PSK
	hash_code = hashlib.sha256()
	hash_code.update(concat.encode('utf-8'))

	EXPECTED_CODE = hash_code.hexdigest()[0:6]
	#Receive Code from the client
	user_auth = connection.recv(1024)
	USER_CODE = str(user_auth.decode())

	#Code Comparison
	if EXPECTED_CODE == USER_CODE:
		print("Successful Authentication - Logging In")

		#Send a message to the client telling successful login
		auth_success_msg = "success"
		connection.send(auth_success_msg.encode())

		#Chat room Logic
		while True:
			data = connection.recv(1024)
			if not data:
				break
			print(f"Received from user: {data.decode()}")
			data = input(' -> ')
			connection.send(data.encode())
		connection.close()
	else:
		#Send a failure code
		print("Unauthorized Connection - Shutting down")
		connection.close()
