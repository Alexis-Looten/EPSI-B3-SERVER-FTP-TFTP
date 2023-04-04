import tftpy
import tftp
import ftp
from multiprocessing import Process

WATCH_DIR = "./epsi"
WATCH_FILE = "password.txt"


def main():
    while True:
        choice = 0
        print("0 - Exit (défaut)")
        print("1 - Start FTP") 
        print("2 - Start TFTP")
        choice = input("Que souhaitez-vous faire ? (numéro)\n")

        # Try if it's an integer
        try:
            int(choice)
        except ValueError as error:
            print(f"Error on input ! {error}\n")
            continue

        if int(choice) < 0 or int(choice) > 2:
            print("This is not a good input ! Please retry.\n")
            continue
        
        # Exit
        if int(choice) == 0:
            break

        # Start FTP server
        if int(choice) == 1:
            ftp_process = Process(target=ftp.start_ftp_server)
            ftp_process.start()
            print("Serveur FTP démarré")

        # Start TFTP server
        if int(choice) == 2:
            server = tftpy.TftpServer(WATCH_DIR)
            tftp_process = Process(target=server.listen, daemon=True)
            tftp_process.start()
            print("Serveur TFTP démarré")
            
            watch_process = Process(target=tftp.watch_file(ftp_process), daemon=True)
            watch_process.start()
            print("Surveillance du fichier démarrée")
            
    exit(0)

if __name__ == "__main__":
    main()