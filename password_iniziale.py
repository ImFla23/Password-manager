#All icons have been kindly taken from this site: <a target="_blank" href="https://icons8.com/icon/89446/copy">Copy</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
#All bg have benn kindly taken from this site: <a href="https://www.freepik.com/free-vector/purple-fluid-background_14731345.htm">Image by rawpixel.com on Freepik</a>
import customtkinter as ctk
import os
import sys
from PIL import Image
from cryptography.fernet import Fernet
import password_manager

def get_base_dir():
    """ Ritorna la cartella in cui si trova l'eseguibile o lo script Python """
    if getattr(sys, 'frozen', False):
        # Se è un .exe generato con PyInstaller, usa la cartella dell'eseguibile
        base_dir = os.path.dirname(sys.executable)
    else:
        # Se è in esecuzione come script Python normale
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    return base_dir

BASE_DIR = get_base_dir()

CRED = os.path.join(BASE_DIR, "password", "credenziali.bin")
KEY_FILE = os.path.join(BASE_DIR, "password", "Key.key")

#creazione chiave di criptazione
TOKEN = b'piedi'
#percorsi vari (cartelle etc)        
icon_path = os.path.join(BASE_DIR, "immagini", "icons8-chiavi-62.ico")
bg_path = os.path.join(BASE_DIR, "immagini", "image_with_custom_dark_background.png")
bg2_path = os.path.join(BASE_DIR, "immagini", "new_processed_image.png")
cartella_password = os.path.join(BASE_DIR, "password")
percorso = os.path.join(cartella_password, "password_salvate.txt")

def ensure_directories():
    """ Crea le cartelle necessarie se non esistono """
    os.makedirs(os.path.join(BASE_DIR, "password"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "immagini"), exist_ok=True)

ensure_directories()


def store_credentials(username, password):
    if os.path.exists (KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read().strip()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key = key_file.write(key)   
    f = Fernet(key)
    us_criptato = f.encrypt(username.encode()).decode()
    ps_criptato = f.encrypt(password.encode()).decode()

    with open(CRED, 'w') as file:  
        file.write(f"{us_criptato}\n{ps_criptato}") 
        
def verify (username, password):
    # primo avvio per salvare le credenziali
    if not os.path.exists(CRED):
        store_credentials(username, password)
        return True
    #lettura di chiave per ogni funzione
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key= key_file.read().strip()
        f = Fernet(key)
    else: 
        return False
    
    try:
        with open(CRED, "r") as file:
            lines = file.readlines()

        if len(lines) != 2:
            return False

        decrypted_us = f.decrypt(lines[0].strip().encode()).decode()
        decrypted_ps = f.decrypt(lines[1].strip().encode()).decode()
        return decrypted_us == username and decrypted_ps == password

    except Exception as e:
        print(f"Errore nella verifica: {e}")
        return False


    
def popup_prima_volta (finestra):
    if os.path.exists(CRED):
        gia_registrato = ctk.CTkLabel(finestra, 
                                      text='ALREADY REGISTRED',
                                      font=('Arial Rounded MT Bold', 23),
                                      text_color='white',
                                      fg_color='#00001e',
                                      height=50)
        gia_registrato.place(relx=0.05,rely=0.848)
        gia_registrato.after(2000, lambda:gia_registrato.destroy())
    else:
        popup = ctk.CTkToplevel()
        popup.geometry('700x700')
        popup.title('Register')
        popup.attributes('-topmost', True)
        popup.iconbitmap(icon_path)
        popup.resizable(False,False)
        bg2_image = ctk.CTkImage(dark_image=Image.open(bg2_path), size=(700, 700))
        
        bg = ctk.CTkLabel(popup, 
                        text='  Enter Username and Password \n \n \n \n \n \n \n \n', 
                        font=('Arial Rounded MT Bold', 32), 
                        image=bg2_image, 
                        width=600, 
                        height=600 )
        bg.place(relx=0)
        
        
        
        us=ctk.StringVar()
        username=ctk.CTkEntry(bg, 
                               textvariable=us,
                               fg_color="#15043a",
                               border_width=3,
                               border_color='#5730e2',
                               corner_radius=20,
                               width=273,
                               height=53,
                               font=('Arial Rounded MT Bold', 32),
                               text_color='white')
        username.place(relx=0.30, rely=0.41)
        #entry password
        ps=ctk.StringVar()
        password=ctk.CTkEntry(bg, 
                               textvariable=ps,
                               fg_color="#15043a",
                               border_width=3,
                               border_color='#5730e2',
                               corner_radius=20,
                               width=273,
                               height=53,
                               font=('Arial Rounded MT Bold', 32),
                               text_color='white')
        password.place(relx=0.30, rely=0.61)
        
        fatto = ctk.CTkLabel(popup, 
                        text='DONE!', 
                        font=('Arial Rounded MT Bold', 32),
                        text_color='white',
                        fg_color='#00001e',
                        height=50,
                        width=300)
        
        register = ctk.CTkButton(bg, text='REGISTER', 
                                corner_radius=20,
                                fg_color='#7e28ed',
                                hover_color='#5730e2',
                                font=('Arial Rounded MT Bold', 34),
                                width=130,
                                height=29, 
                                command=lambda:(store_credentials(us.get(), ps.get()), fatto.place(relx=0.28, rely=0.8), popup.after(1500, lambda:popup.destroy())))
        register.place(relx=0.35, rely=0.8)

       
def login(username, password, finestra, finestra_principale):
    if not os.path.exists(CRED):
        noregistr = ctk.CTkLabel(finestra, 
                               text='No account registered! \n Please sign up before logging in.',
                               text_color='white',
                               font=('Arial Rounded MT Bold', 22),
                               fg_color='#00001e')
        noregistr.place(relx=0.32, rely=0.7)
        noregistr.after(1500, lambda:noregistr.destroy())
        return

    try:
        if verify(username, password):
            corretto = ctk.CTkLabel(finestra, 
                                    text='CORRECT',
                                    text_color='white',
                                    font=('Arial Rounded MT Bold', 32),
                                    fg_color='#00001e')
            corretto.place(relx=0.35, rely=0.7)
            finestra_principale.destroy()
            password_manager.main()
        else:
            incorretto = ctk.CTkLabel(finestra, 
                                    text='Hmmm... SURE?, RETRY!',
                                    text_color='white',
                                    font=('Arial Rounded MT Bold', 32),
                                    fg_color='#00001e',
                                    height=70)
            incorretto.place(relx=0.30, rely=0.68)
            incorretto.after(1500, lambda:incorretto.destroy())
    except FileNotFoundError:
        errore = ctk.CTkLabel(finestra, 
                                    text='file not found',
                                    text_color='white',
                                    font=('Arial Rounded MT Bold', 32),
                                    fg_color='#00001e')
        errore.place(relx=0.35, rely=0.7)
        errore.after(1500,lambda: errore.destroy())
#funzione di recupero pass che controlla se la password inserita esiste tra le password registrate

def controllo_reimposta(password, finestra):
    
    # controllo se c e la chiave
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        no_chiave= ctk.CTkLabel(finestra,
                            text='NEVER REGISTERED',
                            font=('Arial Rounded MT Bold', 22),
                            text_color='white',
                            fg_color='#00001e')
        no_chiave.place (relx=0.10, rely = 0.85)
        no_chiave.after(1500, finestra.destroy())   
    f = Fernet(key)
    
    #controllo se non c e il file
    lista_password = []
    if not os.path.exists(percorso):
        no = ctk.CTkLabel(finestra,
                            text='No passwords have ever been saved.',
                            font=('Arial Rounded MT Bold', 32 ),
                            text_color='white',
                            fg_color='#00001e',
                            height=100)
        no.place (relx=0.10, rely = 0.65)
        no.after(1500, lambda:no.destroy())
    #vero e proprio controllo delle password salvate
    elif os.path.exists(percorso):
        try:
            with open(percorso, 'rb') as password_file:
                contenuto =  password_file.readlines()
                for i, riga in enumerate(contenuto):
                    riga = riga.strip()
                    step = riga.split(b'. Password: ')
                    pass_cruda = step[1].replace(b'.', b'')
                    dec_pas = f.decrypt(pass_cruda).decode()
                    #controllo se password scritta nell entry e nella lista delle password registrate
                    lista_password.append(dec_pas)
                    if password in lista_password:
                        with open(CRED) as cred_file:
                            recuperata = cred_file.readlines()
                            if len(recuperata) != 2:
                                return False
                            recuperata_cruda = f.decrypt(recuperata[1].strip().encode()).decode()
                            us_recuperato = f.decrypt(recuperata[0].strip().encode()).decode()
                        #password recuperata
                        label_pass=ctk.CTkLabel(finestra,
                                                text=f'Your passowrd: {recuperata_cruda}',
                                                font=('Arial Rounded MT Bold', 32),
                                                text_color='white',
                                                fg_color='#00001e',
                                                height=70)
                        label_pass.place(relx=0.30, rely=0.7)
                        label_pass.after(3000, lambda:label_pass.destroy())
                        #username recuperato
                        label_us=ctk.CTkLabel(finestra,
                                                text=f'Your username: {us_recuperato}',
                                                font=('Arial Rounded MT Bold', 32),
                                                text_color='white',
                                                fg_color='#00001e',
                                                height=70)
                        label_us.place(relx=0.30, rely=0.8)
                        label_us.after(3000, lambda:label_us.destroy())
                    else:
                        no_pass=ctk.CTkLabel(finestra,
                                                text=f'No match was found \n with the saved passwords.',
                                                font=('Arial Rounded MT Bold', 32),
                                                text_color='white',
                                                fg_color='#00001e')
                        no_pass.place(relx=0.20, rely=0.7)
                        no_pass.after(1500, lambda:no_pass.destroy())
        except FileNotFoundError as e:
            errore_file=ctk.CTkLabel(finestra,
                                text=f'file not found',
                                text_color='white',
                                font=('Arial Rounded MT Bold', 32),
                                fg_color='#00001e')
            errore_file.place(relx=0.40, rely=0.7)
            errore_file.after(3000, lambda:errore_file.destroy())
        except Exception as e:
            errore=ctk.CTkLabel(finestra,
                                text=f'Errore imprevisto: \n {e}',
                                text_color='white',
                                font=('Arial Rounded MT Bold', 32),
                                fg_color='#00001e')
            errore.place(relx=0.30, rely=0.7)
            errore.after(3000, lambda:errore.destroy())
        

def password_dimenticata():
    popup = ctk.CTkToplevel()
    popup.geometry('700x700')
    popup.title('Register')
    popup.attributes('-topmost', True)
    popup.iconbitmap(icon_path)
    popup.resizable(False,False)
    popup.configure(fg_color = '#370478' )
    bg2_image = ctk.CTkImage(dark_image=Image.open(bg2_path), size=(700, 700))
    
    bg = ctk.CTkLabel(popup, 
                      text='Enter at least one password \n from all registered sites. \n \n \n \n \n \n \n \n \n \n', 
                      font=('Arial Rounded MT Bold', 32), 
                      image=bg2_image, 
                      width=600, 
                      height=600 )
    bg.place(relx=0)
    #entry per reimpostare
    reimpost = ctk.StringVar()
    entry_scord = ctk.CTkEntry(bg, 
                               textvariable=reimpost,
                               fg_color="#15043a",
                               border_width=3,
                               border_color='#5730e2',
                               corner_radius=20,
                               width=273,
                               height=53,
                               font=('Arial Rounded MT Bold', 32),
                               text_color='white')
    entry_scord.place(relx=0.30, rely=0.5)
    #pulsante per registrare
    pul = ctk.CTkButton(bg,
                        corner_radius=20,
                        text='DONE!',
                        hover_color='#5730e2',
                        fg_color='#5f19e1',
                        font=('Arial Rounded MT Bold', 32),
                        width=130,
                        height=29,
                        text_color='white',
                        command=lambda:controllo_reimposta(reimpost.get(), popup))
    pul.place(relx=0.40, rely=0.7)
    remove_cred = ctk.CTkButton(bg,
                                corner_radius=20,
                                text='REMOVE CRED',
                                text_color='white',
                                hover_color='#5730e2',
                                fg_color='#5f19e1',
                                font=('Arial Rounded MT Bold', 19),
                                width=130,
                                height=29,
                                command=lambda:cancella_cred(bg, popup))
    remove_cred.place(relx=0.10, rely=0.9)
    
 #rimuove se ce il file delle password e credenziali
def elimina(finestra):
    try:
        os.remove(CRED)
        os.remove(os.path.join('password', "password_salvate.txt"))
        finestra.after(1500, lambda:finestra.destroy())
    except FileNotFoundError:
        pass
        
    
def cancella_cred(popup, finestra):
    try:
        if os.path.exists(CRED):
            #toglie tutto dallo schermo
            for widget in finestra.winfo_children():
                widget.destroy()
                #pulsanti e label
                no_file = ctk.CTkLabel(finestra, text='NO FILES REMOVED!', font=('Arial Rounded MT Bold', 32), text_color='white')    
                sure=ctk.CTkLabel(finestra, text='ARE YOU SURE \n TO REMOVE YOUR FILE?', font=('Arial Rounded MT Bold', 32), text_color='white')
                done = ctk.CTkLabel(finestra, text='DONE!', font=('Arial Rounded MT Bold', 32), text_color='white')
                sure.place(x=149,y=216)
                si=ctk.CTkButton(finestra, text='YEAH...', command=lambda:(done.place(x=198, y=380),elimina(finestra), finestra.after(1500, lambda:finestra.destroy())),
                                text_color='#15043A',
                                corner_radius=20,
                                fg_color='#5f19e1',
                                hover_color='#5730e2',
                                font=('Arial Rounded MT Bold', 32),
                                width=193,
                                height=53,)
                si.place(x=180, y=324)
                no=ctk.CTkButton(finestra, text='NO', command=lambda:(no_file.place(x=198, y=380), finestra.after(1500, lambda:finestra.destroy())),
                                text_color='#15043A',
                                corner_radius=20,
                                fg_color='#5f19e1',
                                hover_color='#5730e2',
                                font=('Arial Rounded MT Bold', 32),
                                width=193,
                                height=53)
                no.place(x=378, y=324)
                    
        elif not os.path.exists(CRED):
            no_pass = ctk.CTkLabel(finestra, 
                                text='NO CREDS FOUND', 
                                font=('Arial Rounded MT Bold', 25),
                                fg_color='#00001e')
            no_pass.place(relx=0.08, rely=0.90)
            no_pass.after(1500, lambda:no_pass.destroy())
            return
            
    except FileNotFoundError:
            errore=ctk.CTkLabel(finestra, text='FILE NOT FOUND', font=('Arial Rounded MT Bold', 32), text_color='White')
            errore.grid(row=0, column=2)
            finestra.after(3000, lambda:finestra.destroy())
    except Exception as e:
            imprevisto= ctk.CTkLabel(finestra, text=f'UNEXPECTED ERROR \n {e}', text_color='white', font=('Arial Rounded MT Bold', 32))
            imprevisto.grid(row=0, column=2)
            finestra.after(3000,lambda: finestra.destroy())
    
    
def password_iniziale():
    
    # Caricamento dell'immagine di sfondo con PIL
    bg_image = ctk.CTkImage(dark_image=Image.open(bg_path), size=(400, 720))  # Dimensione adattata al frame
    bg2_image = ctk.CTkImage(dark_image=Image.open(bg2_path), size=(845, 655))

    # Impostazioni di CustomTkinter
    ctk.set_appearance_mode('dark')  # Tema scuro
    ctk.set_default_color_theme('blue')
    ctk.set_window_scaling(True)

    # Creazione della finestra principale
    root = ctk.CTk()
    root.geometry('1280x720')
    root.title('Password Manager Login')
    root.resizable(False, False)
    root.iconbitmap(icon_path)
  
    
    bg=ctk.CTkLabel(root,text='WELCOME BACK!', font=('Arial Rounded MT Bold', 32), image=bg_image, width=400, height=720)
    bg.place(x=10)
    bg2=ctk.CTkLabel(root,text='  USERNAME \n \n \n \n PASSWORD \n \n', font=('Arial Rounded MT Bold', 32), width=880, height=720, image=bg2_image)
    bg2.place(x=400)
    
    #entry username
    us=ctk.StringVar()
    username=ctk.CTkEntry(bg2,
                          textvariable=us, 
                          fg_color="#15043a",
                          border_width=3,
                          border_color='#5730e2',
                          corner_radius=20,
                          width=273,
                          height=53,
                          font=('Arial Rounded MT Bold', 32),
                          text_color='white')
    username.place(relx=0.35, rely=0.41)
    #entry password
    ps=ctk.StringVar()
    password=ctk.CTkEntry(bg2,
                          textvariable=ps, 
                          fg_color="#15043a",
                          border_width=3,
                          border_color='#5730e2',
                          corner_radius=20,
                          width=273,
                          height=53,
                          font=('Arial Rounded MT Bold', 32),
                          text_color='white',
                          show = '*')
    password.place(relx=0.35, rely=0.61)

    #prima volta?
    prima_label = ctk.CTkLabel(bg2,
                               text='FIRST TIME?',
                               font=('Arial Rounded MT Bold', 20),
                               text_color='white',
                               fg_color='#00001e')
    prima_label.place (relx=0.112, rely = 0.80)
    
    #pulsante scordat recupero pass
    dimenti = ctk.CTkButton(bg2, text="Forgot password?", #cambia i colori delle scritte con il colore dello sfondo
                            command=lambda:password_dimenticata(),
                            text_color='white',
                            corner_radius=20,
                            fg_color='#5f19e1',
                            hover_color='#5730e2',
                            font=('Arial Rounded MT Bold', 22),
                            width=130,
                            height=29,)
    dimenti.place(relx=0.67, rely=0.85)
    
    #pulsante register
    fisttime = ctk.CTkButton(bg2, text='REGISTER', command=lambda:popup_prima_volta(bg2),
                             text_color='white',
                             corner_radius=20,
                             fg_color='#5f19e1',
                             hover_color='#5730e2',
                             font=('Arial Rounded MT Bold', 22),
                             width=130,
                             height=29,)
    fisttime.place(relx=0.10, rely=0.85)
    
    #pulsante login
    pulsante = ctk.CTkButton(bg2, text='LOGIN', command=lambda:login(us.get(), ps.get(), bg2, root),
                             text_color='white',
                             corner_radius=20,
                             fg_color='#5f19e1',
                             hover_color='#5730e2',
                             font=('Arial Rounded MT Bold', 29),
                             width=130,
                             height=29,)
    pulsante.place(relx=0.43, rely=0.7)
    
    root.mainloop()
   
    
    
if __name__ == '__main__':
    password_iniziale()
