import datetime
import hashlib

user_psk = str(input("Please enter the security code: "))

#hash
hash_code_psk = hashlib.sha256()
hash_code_psk.update(user_psk.encode('utf-8'))

#Get the date
date = datetime.datetime.now()
concat = hash_code_psk.hexdigest() + date.strftime("%Y%m%d")

#Hash the date and the user psk
hash_code = hashlib.sha256()
hash_code.update(concat.encode('utf-8'))

token = hash_code.hexdigest()[0:6]

print(f"Your MFA token is: {token}")
