# Importer de nødvendige moduler
from socket import socket, AF_INET, SOCK_DGRAM  #Importer socket-funktioner for netværkskommunikation
from sys import exit  # Importerer sys modulen for exit-funktionen
from time import time  # Importerer time funktionen for at håndtere tid

# Definerer serverens portnummer og opretter en socket
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(("", server_port))

# Funktion til at konvertere sekunder til minutter:sekunder format
def convert(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

# Initialiser variabler til tidstagning
starttid = time()

# Udskriv besked om, at serveren er klar til at modtage
print("Serveren er klar til at modtage")

# Lytter konstant efter beskeder
while True:
    try:
        # Modtag besked og klientadresse
        message, client_address = server_socket.recvfrom(2048)
        modified_message = message.decode()   # Konverter besked til en streng

        # Hvis beskeden er "start", start tidstagningen
        if modified_message == "start":
            starttid = time()
        # Hvis beskeden ikke er tom
        elif modified_message != "":
            sluttid = time()
            totaltid = sluttid - starttid

            # Konverter tid til ønsket format og erstat relevante dele af beskeden
            tid = convert(totaltid)
            ny_message = modified_message.replace("tid", f"{tid}")
            ny_message2 = ny_message.replace("insertip", f"{client_address[0]}")
            print(ny_message2)

            # Nulstil beskedvariablerne
            ny_message = ""
            modified_message = ""

    except KeyboardInterrupt:
        # Håndterer Ctrl-C, lukker socket og afslutter programmet
        print("CTRL-C pressed, closing down!")
        server_socket.close()
        exit()