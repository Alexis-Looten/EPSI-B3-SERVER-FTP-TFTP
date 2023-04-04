import os
import time
from multiprocessing import Process
import ftp

WATCH_DIR = "./epsi"

WATCH_FILE = "password.txt"

FTP_HOST = "127.0.0.1"
FTP_PORT = 21

def restart_ftp_server(ftp_process):
    ftp_process.terminate()
    ftp_process = Process(target=ftp.start_ftp_server)
    ftp_process.start()
    
def watch_file(ftp_process):
    prev_content = ""
    
    file_path = os.path.join(WATCH_DIR, WATCH_FILE)
    
    with open(file_path, "r") as f:
        prev_content = f.read()
    
    while True:
        time.sleep(1)
        
        file_path = os.path.join(WATCH_DIR, WATCH_FILE)
        
        with open(file_path, "r") as f:
            content = f.read()
            if content != prev_content:
                restart_ftp_server(ftp_process)
                
                prev_content = content
                
                print("Instruction de redémarrage envoyée")        