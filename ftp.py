import pyftpdlib
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server():
    # Configuration du serveur FTP
    host = "127.0.0.1"
    port = 21
    ftp_root = "./files"
    USER = "epsi"
    password = ""

    with open(f"./{USER}/password.txt", "r") as file:
        password = file.readline().split()[0]

    handler = FTPHandler
    handler.authorizer = pyftpdlib.authorizers.DummyAuthorizer()
    handler.authorizer.add_user(USER, password, ftp_root, perm="elradfmw")
    handler.banner = "Bienvenue sur notre serveur FTP !"
    server = FTPServer((host, port), handler)
    server.serve_forever()