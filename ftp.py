import pyftpdlib
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Configuration du serveur FTP
host = "127.0.0.1"
port = 21
ftp_root = "./files"
USER = "epsi"
password = ""

with open(f"./{USER}/password.txt", "r") as file:
    password = file.readline().split()[0]
    
print(password)
print(USER, password, ftp_root, "elradfmw")

# Création et démarrage du serveur FTP
handler = FTPHandler
handler.authorizer = pyftpdlib.authorizers.DummyAuthorizer()
handler.authorizer.add_user(USER, password, ftp_root, perm="elradfmw")
handler.banner = "Bienvenue sur notre serveur FTP !"
server = FTPServer((host, port), handler)
server.serve_forever()
