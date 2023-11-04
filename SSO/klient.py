# Importer nødvendige moduler fra Python-biblioteker
from socket import socket, AF_INET, SOCK_DGRAM  # Importer socket-funktioner for netværkskommunikation

try:
    server_name = "10.0.0.5"  # Definer IP-adressen for serveren
    server_port = 12000  # Definer portnummeret til kommunikation med serveren
    client_socket = socket(AF_INET, SOCK_DGRAM)  # Opret en UDP-socket til netværkskommunikation

    # Start af while-løkken, der kører uendeligt
    while True:
        try:
            spiller = input("Vælg spiller: ")  # Prompt brugeren for at vælge en spiller

            if spiller == "exit":
                break  # Hvis brugeren indtaster "exit", bryd løkken og afslut programmet

            if spiller == "start":
                start = "start"
                client_socket.sendto(start.encode(), (server_name, server_port))  # Send "start"-besked til serveren

            elif spiller != "":
                obseva = input("Skriv Observation:")  # Prompt brugeren for en observation

                # Sæt beskedens format med spiller, observation og tekst til ændring
                message = f"Spiller {spiller}: {obseva} \nTid: tid                         Observant: insertip"
                
                # Send beskeden til serveren
                client_socket.sendto(message.encode(), (server_name, server_port))

            else:
                print("Indtast gyldig info")  # Hvis inputtet er tomt eller ugyldigt, udskriv en fejlmeddelelse
            
        # Håndter afslutning ved brugerinput (CTRL-C)
        except KeyboardInterrupt:
            print("CTRL-C pressed, closing down!")
            break  # Afslut loopet ved Ctrl-C

# Håndter eventuelle generelle undtagelser (fejl)
except Exception as e:
    print("An error occurred:", str(e))

# Kør altid efter try-blokken er udført, uanset hvad
finally:
    client_socket.close()  # Luk klientens socket, når programmet afsluttes