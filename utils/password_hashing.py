import bcrypt

password = "J3rryTh3B3rry"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())  # Copy this and update `admin_credentials.json`
