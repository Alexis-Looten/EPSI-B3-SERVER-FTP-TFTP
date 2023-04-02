import os
import time
import threading
import tftpy
import ftplib
import psutil
import subprocess
from pyftpdlib import servers, handlers

WATCH_DIR = "./epsi"

WATCH_FILE = "password.txt"

FTP_HOST = "127.0.0.1"
FTP_PORT = 21

def get_ftp_pid():
    for proc in psutil.process_iter():
        try:
            if proc.name() == "python3" and "ftp.py" in proc.cmdline():
                pid = proc.pid
                print(f"PID du processus 'ftp.py' : {pid}")
                return pid
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass


def restart_ftp_server(pid):
    print(pid)
    subprocess.run(["kill", str(pid)])
    subprocess.run(['/bin/python3', 'ftp.py'])
    print("Server restarted")

def watch_file():
    pid = get_ftp_pid()
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
                restart_ftp_server(pid)
                
                prev_content = content
                
                print("Instruction de redémarrage envoyée")
                

def main():
    server = tftpy.TftpServer(WATCH_DIR)
    
    tftp_thread = threading.Thread(target=server.listen, daemon=True)
    tftp_thread.start()
    
    print("Serveur TFTP démarré")

    watch_thread = threading.Thread(target=watch_file, daemon=True)
    watch_thread.start()
    
    print("Surveillance du fichier démarrée")

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
