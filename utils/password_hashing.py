import bcrypt

password = "Gr3yW0rmD4nc3r"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hashed.decode())  # Copy this and update `admin_credentials.json`
