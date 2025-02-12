#All icons have been kindly taken from this site: <a target="_blank" href="https://icons8.com/icon/89446/copy">Copy</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
#All bg have benn kindly taken from this site: <a href="https://www.freepik.com/free-vector/purple-fluid-background_14731345.htm">Image by rawpixel.com on Freepik</a>
import os
import sys
import customtkinter as ctk
from cryptography.fernet import Fernet 
from PIL import Image
import pyperclip

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

my_wa=my_wr= my_wm= my_ws  = 371
my_ha=my_hr= my_hm=my_hs =  208

expanding = True
#cartella e percorsi vari
cartella_password = os.path.join(BASE_DIR, "password")
percorso = os.path.join(cartella_password, "password_salvate.txt")
KEY_FILE = os.path.join(cartella_password, "Key.key")


# percorsi immagini
sfondo_path = os.path.join(BASE_DIR, "immagini", "sfondo_test.png")
add_path = os.path.join(BASE_DIR, "immagini", "add.png")
remove_path = os.path.join(BASE_DIR, "immagini", "minus.png")
show_path = os.path.join(BASE_DIR, "immagini", "show.png")
modify_path = os.path.join(BASE_DIR, "immagini", "modify.png")
copy_path = os.path.join(BASE_DIR, "immagini", "copy.png")
icon_path = os.path.join(BASE_DIR, "immagini", "icons8-chiavi-62.ico")
# Creazione cartelle
os.makedirs(cartella_password, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "immagini"), exist_ok=True)

#crittografia
# creazione chiave generata automaticamente la prima volta (se esiste gia la legge)
if  os.path.exists(KEY_FILE):
    with open(KEY_FILE, 'rb') as key_file:
        key = key_file.read().strip()
else:
    key = Fernet.generate_key()
    with open (KEY_FILE, 'wb') as key_file:
        key_file.write(key)
f = Fernet(key)

def encrypt(sit):
    return f.encrypt(sit.encode()).decode()

def decript(sit):
    return f.decrypt(sit.encode()).decode()

#funzioni del progrmmma
def aggiungi (chiave, valore, popup):
    #controllo se vengono scritte le cose negli entry
    if chiave == '' or chiave == ' ' and valore == '' or valore == ' ':
        testono = ctk.CTkLabel (popup, 
                                    text='WRITE \n SOMETHING',
                                    font=('Arial Rounded MT Bold', 44), 
                                    text_color='white') 
        testono.place(x=107, y=574)
        testono.after(2000, lambda:testono.destroy())
        return
    elif chiave == '' or valore == '' or chiave == ' ' or valore == ' ':
        noo = ctk.CTkLabel (popup, 
                            text='WRITE \n SOMETHING',
                            font=('Arial Rounded MT Bold', 44), 
                            text_color='white') 
        noo.place(x=107, y=574)
        noo.after(2000, lambda:noo.destroy())
        return
    #se sono scritte viene visualizzato il successo e momerizzate le password
    else:
        for widget in popup.winfo_children():
            widget.destroy()
        Testoconferma = ctk.CTkLabel (popup, 
                                    text='DONE!',
                                    font=('Arial Rounded MT Bold', 42), 
                                    text_color='white') 
        Testoconferma.place(x=177, y=270)
        popup.after(1500, lambda: popup.destroy())
    #variabili criptate
    sito_cript = encrypt(chiave)
    pass_cprit = encrypt(valore)
    # se non esiste il file nella cartella lo crea   
    if not os.path.exists(percorso):
        file = open(percorso, 'w')
        file.write(f'Sito: {sito_cript}. Password: {pass_cprit}. \n')
        file.close()
    # se esiste gia lo appende al file
    else:
        file = open(percorso, 'a')
        file.write(f'Sito: {sito_cript}. Password: {pass_cprit}. \n')
        file.close()
        
def modify(content, I, new_ch, finestra, file_path):
    #controllo se e' stato scritto qualcosa
    if new_ch == '':
        no = ctk.CTkLabel(finestra, text='WRITE \n SOMETHING', font=('Arial Rounded MT Bold', 44), text_color='white')
        no.place(x=107, y=555)
        no.after(2000, lambda: no.destroy())
        return
    new_ch_crpit = encrypt(new_ch)  # Cripta la nuova password

    # Aggiorna la riga corrispondente
    sito_name = content[I].split('. Password: ')[0].split('Sito: ')[1]
    content[I] = f"Sito: {sito_name}. Password: {new_ch_crpit}.\n"

    # Messaggio di successo
    done = ctk.CTkLabel(finestra, text='DONE!', font=('Arial Rounded MT Bold', 32), text_color='white',height=120,width=600)
    done.place(x=-60, y=545)
    finestra.after(3000, lambda: finestra.destroy())

    # 🔹 Scrive tutto il file aggiornato
    with open(file_path, 'w') as f:
        f.writelines(content)  # Sovrascrive tutto il file con i dati aggiornati

    

def readplu(dom, popup):
    lista_cruda_sito_password = []
    trovato = False  # Per verificare se il sito è stato trovato almeno una volta
    if dom.strip() == '':
        no = ctk.CTkLabel(popup, text='WRITE \n SOMETHING', font=('Arial Rounded MT Bold', 44), text_color='white')
        no.place(x=107, y=575)
        no.after(2000, lambda: no.destroy())
        return

    try:
        # Pulisce la finestra
        for widget in popup.winfo_children():
            widget.destroy()
        #cerca il sito con il nome selezionato
        with open(percorso, 'r+') as file:
            contenuto = file.readlines()

        for i, riga in enumerate(contenuto):
            riga = riga.strip()
            
            # Estrazione dati
            sito_part = riga.split('. Password: ')
            if len(sito_part) != 2:
                print(f"Formato non valido nella riga {i}: {riga}")
                continue

            sito_crudo = sito_part[0].replace('Sito: ', '').strip()
            password_cruda = sito_part[1].replace('.', '').strip()

            # Decripta i dati
            dec_sit = decript(sito_crudo)
            dec_pas = decript(password_cruda)

            # Aggiunge il sito alla lista
            lista_cruda_sito_password.append((dec_sit, dec_pas, i))

        # Frame del titolo (viene creato UNA sola volta)
        title_f = ctk.CTkFrame(popup, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
        title_f.place(x=40, y=62)
        titolo = ctk.CTkLabel(title_f, text='MODIFY', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
        titolo.place(x=120, y=5)


        for sito, password, i in lista_cruda_sito_password:
            if dom == sito:  # Se il sito corrisponde, mostra i dati
                trovato = True

                # Label con sito e password
                trovato_label = ctk.CTkLabel(
                    popup,
                    text=f"Current Data:\n Site: {sito}\n Password: {password}",
                    font=('Arial Rounded MT Bold', 30),
                    text_color='white',
                    justify="left",
                )
                trovato_label.place(x=127, y=130)

                # Campo per nuova password
                new_choice = ctk.StringVar()
                new = ctk.CTkEntry(
                    popup,
                    textvariable=new_choice,
                    fg_color="#15043a",
                    border_width=3,
                    border_color='#5730e2',
                    corner_radius=20,
                    width=273,
                    height=53,
                    font=('Arial Rounded MT Bold', 20),
                    text_color='white',
                )
                new.place(x=107, y=361)

                # Bottone "DONE"
                sovrascrivi = ctk.CTkButton(
                    popup,
                    text='DONE',
                    command=lambda idx=i: modify(contenuto, idx, new_choice.get().strip(), popup, percorso),
                    text_color='#15043A',
                    corner_radius=20,
                    fg_color='#5f19e1',
                    hover_color='#5730e2',
                    font=('Arial Rounded MT Bold', 32),
                    width=273,
                    height=53,
                )
                sovrascrivi.place(x=107, y=574)

        if not trovato:
            non_trovato = ctk.CTkLabel(
                popup,
                text=f"SITE: {dom} \n NOT FOUND",
                text_color='white',
                font=('Arial Rounded MT Bold', 25)
            )
            non_trovato.place(x=160, y=340)
            popup.after(3000, lambda: popup.destroy())

    except FileNotFoundError:
        errore = ctk.CTkLabel(popup, text='FILE NOT FOUND', text_color='white', font=('Arial Rounded MT Bold', 32))
        errore.place(x=107, y=250)
        popup.after(3000, lambda: popup.destroy())

    except Exception as e:
        imprevisto = ctk.CTkLabel(popup, text=f'Errore: {e}', text_color='white', font=('Arial Rounded MT Bold', 32))
        imprevisto.place(x=107, y=250)
        popup.after(3000, lambda: popup.destroy())



def remove (choice, popup):
    if choice.strip() == '':
        no = ctk.CTkLabel(popup, text='WRITE \n SOMETHING!', font=('Arial Rounded MT Bold', 42), text_color='white')
        no.place(x=107, y=574)
        no.after(1800, lambda: no.destroy())
        return

    try:
        for widget in popup.winfo_children():
            widget.destroy()
            
        # Frame del titolo
        title_f = ctk.CTkFrame(popup, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
        title_f.place(x=40, y=62)
        titolo = ctk.CTkLabel(title_f, text='REMOVE', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
        titolo.place(x=120, y=5)

        # Leggi il file
        with open(percorso, 'r') as file:
            contenuto = file.readlines()

        nuovo_contenuto = []
        trovato = False

        for i, riga in enumerate(contenuto):
            riga = riga.strip()

            # Estrai sito e password
            sito_part = riga.split('. Password: ')
            if len(sito_part) != 2:
                print(f"Formato non valido nella riga {i}: {riga}")
                continue

            sito_crudo = sito_part[0].replace('Sito: ', '').strip()
            password_cruda = sito_part[1].replace('.', '').strip()

            # Decripta i dati
            dec_sit = decript(sito_crudo)

            # Se il sito corrisponde, non aggiungerlo al nuovo contenuto
            if choice.lower() == dec_sit.lower():
                trovato = True
                continue  
            
            # Se non è il sito da rimuovere, aggiungilo alla nuova lista
            nuovo_contenuto.append(riga + '\n')

        # Riscrivi il file
        with open(percorso, 'w') as file:
            file.writelines(nuovo_contenuto)

        # Mostra il messaggio di conferma o di errore
        if trovato:
            done = ctk.CTkLabel(popup, text='DONE!', font=('Arial Rounded MT Bold', 42), text_color='white')
            done.place(x=177, y=270)
            popup.after(2000, lambda: popup.destroy())
        else:
            non_trovato = ctk.CTkLabel(popup, text=f"SITE: {choice} NOT FOUND", text_color='white', font=('Arial Rounded MT Bold', 32))
            non_trovato.place(x=119, y=216)
            popup.after(2000, lambda: popup.destroy())

    except FileNotFoundError:
        errore = ctk.CTkLabel(popup, text='FILE NOT FOUND', text_color='white', font=('Arial Rounded MT Bold', 32))
        errore.place(x=119, y=216)
        popup.after(3000, lambda: popup.destroy())
    except Exception as e:
        imprevisto = ctk.CTkLabel(popup, text=f'UNEXPECTED ERROR: \n {e}', text_color='white', font=('Arial Rounded MT Bold', 32))
        imprevisto.place(x=119, y=216)
        popup.after(3000, lambda: popup.destroy())

            
#funzione che elimina tutto il file
def elimina_file(finestra):
    for widget in finestra.winfo_children():
                widget.destroy()
    try:
        os.remove(percorso)
        done=ctk.CTkLabel(finestra, text='DONE!', font=('Arial Rounded MT Bold', 42), text_color='white')
        done.place(x=177, y=270)
        finestra.after(3000, lambda:finestra.destroy())
    except FileNotFoundError:
        errore=ctk.CTkLabel(finestra, text='FILE NOT FOUND', font=('Arial Rounded MT Bold', 32), text_color='White')
        errore.place(x=119,y=216)
        finestra.after(3000, lambda:finestra.destroy())

def main():
    #creazione finestra e varie
    ctk.set_appearance_mode("system") 
    ctk.set_default_color_theme('blue')
    ctk.set_window_scaling(True)
    
    
    root = ctk.CTk()
    root.title('Password Manager')
    root.configure(fg_color='#15043a')
    root.geometry('1056x720')
    root.resizable(False,False)
    root.iconbitmap(icon_path)
    # frame principale dei pulsanti
    sfondo = ctk.CTkImage(dark_image=Image.open(sfondo_path), size=(1280, 900))
    first_f = ctk.CTkLabel(root, image=sfondo, text='')
    first_f.place(x=1, y = 1)
    
    #frame del titolo
    title_f = ctk.CTkFrame(first_f, 
                           corner_radius=20,
                           fg_color='#11B9F8', 
                           height=74, 
                           width=998)
    title_f.place(x=31, y=32)
    
    #label titolo  
    titolo = ctk.CTkLabel(title_f, 
                          text='Welcome To Your Password Manager', 
                          font=('Arial Rounded MT Bold', 42), 
                          text_color='#15043A')
    titolo.place(x=110, y=9)
    
    #popup
    def popup_add():
        #creazione pop up con sfondo
        sfondo = ctk.CTkImage(Image.open(sfondo_path), size=(687,914))
        popupentry=ctk.CTkToplevel()
        popupentry.geometry('487x714')
        popupentry.title('ADD')
        popupentry.attributes('-topmost', True)
        popupentry.iconbitmap(icon_path)
        popupentry.resizable(False,False)
        popupentry.configure(fg_color='#15043a')
        
        bg = ctk.CTkLabel(popupentry, 
                          image=sfondo, 
                          text='')
        bg.place(x=1, y=1)
        
        #frame del titolo
        title_f = ctk.CTkFrame(bg, 
                               corner_radius=20, 
                               fg_color='#11B9F8',
                               height=56, 
                               width=407)
        title_f.place(x=40, y=62)
        
        #label titolo  
        titolo = ctk.CTkLabel(title_f, 
                              text='ADD',
                              font=('Arial Rounded MT Bold', 42),
                              text_color='#15043A')
        titolo.place(x=161, y=5)
        
        text_site=ctk.CTkLabel(bg, 
                             text="SITE", 
                             font=('Arial Rounded MT Bold', 26), 
                             text_color='white')
        text_site.place(x=220,y=170)
        
        #variabili aggiunta
        sito = ctk.StringVar()
        entrysito = ctk.CTkEntry(bg, 
                                 textvariable=sito, 
                                 fg_color="#15043a",
                                 border_width=3,
                                 border_color='#5730e2',
                                 corner_radius=20,
                                 width=273,
                                 height=53,
                                 font=('Arial Rounded MT Bold', 32),
                                 text_color='white')
        entrysito.place(x=116, y=208)
        entrysito.after(100, lambda: entrysito.focus())
        
        text_ps=ctk.CTkLabel(bg, 
                             text="PASSWORD", 
                             font=('Arial Rounded MT Bold', 26), 
                             text_color='white')
        text_ps.place(x=170,y=323)
        password = ctk.StringVar()
        entrypassword = ctk.CTkEntry(bg, 
                                    textvariable=password, 
                                    fg_color="#15043a",
                                    border_width=3,
                                    border_color='#5730e2',
                                    corner_radius=20,
                                    width=273,
                                    height=53,
                                    font=('Arial Rounded MT Bold', 32),
                                    text_color='white')
        entrypassword.place(x=116, y=361)
        
        #pulsante done
        exit_conferma=ctk.CTkButton(bg, 
                                    text='DONE', 
                                    command=lambda:aggiungi(sito.get().capitalize(),password.get(), popupentry), 
                                    text_color='#15043A', 
                                    corner_radius=20,
                                    fg_color='#5f19e1',
                                    hover_color='#5730e2',
                                    font=('Arial Rounded MT Bold',32),
                                    width=273,
                                    height=53,)
        exit_conferma.place(x=116, y=574)
    
    def popop_mod():
        sfondo = ctk.CTkImage(Image.open(sfondo_path), size=(687,914))
        popupentry_m=ctk.CTkToplevel()
        popupentry_m.geometry('487x714')
        popupentry_m.title('MODIFY')
        popupentry_m.attributes('-topmost', True)
        popupentry_m.iconbitmap(icon_path)
        popupentry_m.resizable(False, False)
        popupentry_m.configure(fg_color ='#15043a') 
        
        bg = ctk.CTkLabel(popupentry_m, 
                          image=sfondo, 
                          text='')
        bg.place(x=1, y=1)
        
        #frame del titolo
        title_f = ctk.CTkFrame(bg, 
                               corner_radius=20, 
                               fg_color='#11B9F8',
                               height=56, 
                               width=407)
        title_f.place(x=40, y=62)
        
        #label titolo  
        titolo = ctk.CTkLabel(title_f, 
                              text='MODIFY',
                              font=('Arial Rounded MT Bold', 42),
                              text_color='#15043A')
        titolo.place(x=130, y=5)
        
        domanda=ctk.CTkLabel(bg, 
                             text="WICH SITE DO \n YOU WANT TO \n MODIFY?", 
                             font=('Arial Rounded MT Bold', 36), 
                             text_color='white')
        domanda.place(x=109,y=200)
        
        risp_utente = ctk.StringVar()
        entry_risp= ctk.CTkEntry(bg, 
                                 textvariable=risp_utente, 
                                 fg_color="#15043a",
                                 border_width=3,
                                 border_color='#5730e2',
                                 corner_radius=20,
                                 width=273,
                                 height=53,
                                 font=('Arial Rounded MT Bold', 32),
                                 text_color='white')
        entry_risp.place(x=107, y=361)
        entry_risp.after(100, lambda: entry_risp.focus())
        
        invia=ctk.CTkButton(bg, 
                            command=lambda: readplu(risp_utente.get().capitalize().strip(), popupentry_m), 
                            text='DONE',
                            text_color='#15043A', 
                            corner_radius=20,
                            fg_color='#5f19e1',
                            hover_color='#5730e2',
                            font=('Arial Rounded MT Bold',32),
                            width=273,
                            height=53,)
        invia.place(x=107, y=574)

    def popup_show():
        def copia_password(password, button):
            pyperclip.copy(password)  # Copia la password negli appunti
            button.configure(text="Copied!")  # Cambia testo del bottone
            button.after(2000, lambda: button.configure(text=''))
        try:
            popupentry_s = ctk.CTkToplevel()
            popupentry_s.geometry('487x714')
            popupentry_s.title('Leggi')
            popupentry_s.resizable(False, False)
            popupentry_s.attributes('-topmost', True)
            popupentry_s.iconbitmap(icon_path)
            popupentry_s.configure(fg_color='#15043a')
            #funzione rotella mouse
            def on_mouse_wheel(event):
                if event.delta:  # Windows/macOS
                    canvas.yview_scroll(-1 * (event.delta // 120), "units")
                else:  # Linux (event.button 4 = scroll up, 5 = scroll down)
                    if event.num == 4:
                        canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        canvas.yview_scroll(1, "units")

            # Canvas for scrolling
            canvas = ctk.CTkCanvas(popupentry_s, bg='#15043a', width=470, height=680, highlightthickness=0)
            canvas.pack(side="left", fill="both", expand=True)

            # Scrollbar
            scroll = ctk.CTkScrollbar(popupentry_s, 
                                      orientation='vertical', 
                                      command=canvas.yview,
                                      )
            scroll.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scroll.set)

            # Frame inside the Canvas
            content_frame = ctk.CTkFrame(canvas, fg_color='#15043a')
            frame_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

            # Read the file
            with open(percorso, 'r') as file:
                righe = file.readlines()

            # Title frame
            title_f = ctk.CTkFrame(popupentry_s, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
            title_f.place(x=40, y=12)

            # Title label
            titolo = ctk.CTkLabel(title_f, text='SHOW', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
            titolo.place(x=130, y=5)
            # Frame per la lista delle password (lo mettiamo a metà schermo con expand=True)
            password_list_frame = ctk.CTkFrame(content_frame, fg_color='#15043a')
            password_list_frame.pack(pady=100, padx=20, fill="both", expand=True)  #Qui lo mettiamo a metà

            # Display the saved passwords
            for i, riga in enumerate(righe):
                riga = riga.strip()
                sito_part = riga.split('. Password: ')
                if len(sito_part) != 2:
                    continue

                sito_crudo = sito_part[0].replace('Sito: ', '').strip()
                password_cruda = sito_part[1].replace('.', '').strip()

                # Decripta i dati
                dec_sit = decript(sito_crudo)
                dec_pas = decript(password_cruda)

                # Contenitore per sito e password
                frame = ctk.CTkFrame(password_list_frame, fg_color='#15043a', corner_radius=10)
                frame.pack(pady=5, padx=10, fill="x")

                # Label per mostrare sito e password
                labelpass = ctk.CTkLabel(frame, 
                                        text=f'Password Salvate:\nSito: {dec_sit}\nPassword: {dec_pas}', 
                                        font=('Arial Rounded MT Bold', 20), 
                                        text_color='white', 
                                        wraplength=350)
                labelpass.pack(pady=5, padx=10, anchor="center")

                # Creiamo il bottone PRIMA della lambda
                copy_image = ctk.CTkImage(Image.open(copy_path), size=(30,30))
                copy_button = ctk.CTkButton(frame, 
                                            text_color='#15043A',
                                            corner_radius=10,
                                            fg_color='#5f19e1',
                                            hover_color='#5730e2',
                                            width=60,
                                            height=40,
                                            image=copy_image,
                                            text='')
                
                # Ora assegniamo la funzione con una chiusura che cattura la variabile copy_button
                copy_button.configure(command=lambda p=dec_pas, b=copy_button: copia_password(p, b))

                # Infine, posizioniamo il bottone
                copy_button.pack(pady=5)



            # Close button
            exit_b = ctk.CTkButton(content_frame, text='Close', command=popupentry_s.destroy,
                                text_color='#15043A', corner_radius=20, fg_color='#5f19e1',
                                hover_color='#5730e2', font=('Arial Rounded MT Bold', 32),
                                width=273, height=53)
            exit_b.pack(padx=100, pady=10)

            # Update the scrolling region
            content_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows/macOS
            canvas.bind_all("<Button-4>", on_mouse_wheel)     # Linux Scroll Up
            canvas.bind_all("<Button-5>", on_mouse_wheel)     # Linux Scroll Down
        except FileNotFoundError:
            errore = ctk.CTkLabel(popupentry_s, text='FILE NOT FOUND', font=('Arial Rounded MT Bold', 42),
                                text_color='white')
            errore.place(x=87, y=250)
            popupentry_s.after(3000, popupentry_s.destroy)

    #funzioncina per scrivere label del non eliminato
    def nessun_file_eliminato(fines):
        for widget in fines.winfo_children():
            widget.destroy()
        # Frame del titolo 
        title_f = ctk.CTkFrame(fines, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
        title_f.place(x=40, y=62)
        titolo = ctk.CTkLabel(title_f, text='REMOVE', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
        titolo.place(x=120, y=5)

        not_done=ctk.CTkLabel(fines, text='NO FILE REMOVED!', font=('Arial Rounded MT Bold', 32), text_color='white')
        not_done.place(x=119,y=216)
        fines.after(1500,lambda:fines.destroy())
        
    #funzione per rimuovere tutti i file       
    def remove_fil(popup):
        try:
            for widget in popup.winfo_children():
                widget.destroy()
                
            # Frame del titolo 
            title_f = ctk.CTkFrame(popup, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
            title_f.place(x=40, y=62)
            titolo = ctk.CTkLabel(title_f, text='REMOVE', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
            titolo.place(x=120, y=5)

            #pulsanti e label    
            sure=ctk.CTkLabel(popup, text='ARE YOU SURE \n TO REMOVE YOUR FILE?', font=('Arial Rounded MT Bold', 32), text_color='white')
            sure.place(x=49,y=216)
            si=ctk.CTkButton(popup, text='YEAH...', command=lambda:elimina_file(popup),
                             text_color='#15043A',
                             corner_radius=20,
                             fg_color='#5f19e1',
                             hover_color='#5730e2',
                             font=('Arial Rounded MT Bold', 32),
                             width=193,
                             height=53,)
            si.place(x=19, y=324)
            no=ctk.CTkButton(popup, text='NO', command=lambda:nessun_file_eliminato(popup),
                             text_color='#15043A',
                             corner_radius=20,
                             fg_color='#5f19e1',
                             hover_color='#5730e2',
                             font=('Arial Rounded MT Bold', 32),
                             width=193,
                             height=53)
            no.place(x=278, y=324)
            
        except FileNotFoundError:
            errore=ctk.CTkLabel(popup, text='FILE NOT FOUND', font=('Arial Rounded MT Bold', 32), text_color='White')
            errore.grid(row=0, column=2)
            popup.after(3000, lambda:popup.destroy())
        except Exception as e:
            imprevisto= ctk.CTkLabel(popup, text=f'UNEXPECTED ERROR \n {e}', text_color='white', font=('Arial Rounded MT Bold', 32))
            imprevisto.grid(row=0, column=2)
            popup.after(3000,lambda: popup.destroy())
    
    
    def popump_rem():
        sfondo = ctk.CTkImage(Image.open(sfondo_path), size=(687,914))
        popupentry_r=ctk.CTkToplevel()
        popupentry_r.geometry('487x714')
        popupentry_r.title('REMOVE')
        popupentry_r.attributes('-topmost', True)
        popupentry_r.resizable(False, False)
        popupentry_r.iconbitmap(icon_path)
        popupentry_r.configure(fg_color = '#15043a')
        #sfondo
        bg =ctk.CTkLabel(popupentry_r,text='', image=sfondo, )
        bg.place(x=1,y=1)
        
        # Frame del titolo 
        title_f = ctk.CTkFrame(popupentry_r, corner_radius=20, fg_color='#11B9F8', height=56, width=407)
        title_f.place(x=40, y=62)
        titolo = ctk.CTkLabel(title_f, text='REMOVE', font=('Arial Rounded MT Bold', 42), text_color='#15043A')
        titolo.place(x=120, y=5)

        #label e pulsanti ed entry
        central_text = ctk.CTkLabel(popupentry_r, text='WHICH SITE DO \n YOU WANT TO \n REMOVE?', text_color='white', font=('Arial Rounded MT Bold',32))
        central_text.place(x=119,y=216)
        
        scelta = ctk.StringVar()
        entryscelta = ctk.CTkEntry(bg, 
                                 textvariable=scelta, 
                                 fg_color="#15043a",
                                 border_width=3,
                                 border_color='#5730e2',
                                 corner_radius=20,
                                 width=273,
                                 height=53,
                                 font=('Arial Rounded MT Bold', 32),
                                 text_color='white')
        entryscelta.place(x=107, y=361)
        
        conferma = ctk.CTkButton(popupentry_r, text='DONE', command=lambda: remove(scelta.get().capitalize(), popupentry_r),
                                 text_color='#15043A',
                                 corner_radius=20,
                                 fg_color='#5f19e1',
                                 hover_color='#5730e2',
                                 font=('Arial Rounded MT Bold', 32),
                                 width=273,
                                 height=53,)
        conferma.place(x=107, y=574)
        tutto = ctk.CTkButton(popupentry_r, text='REMOVE FILE', command=lambda:remove_fil(popupentry_r),
                              text_color='#15043A',
                              corner_radius=20,
                              fg_color='#5f19e1',
                              hover_color='#5730e2',
                              font=('Arial Rounded MT Bold', 19),
                              width=130,
                              height=29,)
        tutto.place(x=303, y=678)
        
    
    #funzione animazione pulsanti aggiungi
    def an_pulsante_a():
        global my_wa, my_ha
        if my_wa <= 386  and my_ha <= 223 and expanding:
            my_wa += 5
            my_ha += 5
            add_button.configure(width=my_wa, height=my_ha)
            add_button.after(5,an_pulsante_a)
            
        elif my_wa >= 371 and my_ha >= 208 and not expanding:
            my_wa -= 5
            my_ha -= 5
            add_button.configure(width=my_wa, height=my_ha)
            add_button.after(5, an_pulsante_a)
            
    # funzione animazione rimuovi
    def an_pulsante_r():
        global my_wr, my_hr
        if my_wr <=386  and my_hr <= 223 and expanding:
            my_wr += 5
            my_hr += 5
            remove_button.configure(width=my_wr, height=my_hr)
            remove_button.after(5,an_pulsante_r)
            
        elif my_wr >= 371 and my_hr >= 208 and not expanding:
            my_wr -= 5
            my_hr -= 5
            remove_button.configure(width=my_wr, height=my_hr)
            remove_button.after(5,an_pulsante_r)
            
    # funzione animazione modify        
    def an_pulsante_m():
        global my_wm, my_hm
        if my_wm <=386 and my_hm <= 223 and expanding:
            my_wm += 5
            my_hm += 5
            modify_button.configure(width=my_wm, height=my_hm)
            modify_button.after(5,an_pulsante_m)
            
        elif my_wm >= 371 and my_hm >= 208 and not expanding:
            my_wm -= 5
            my_hm -= 5
            modify_button.configure(width=my_wm, height=my_hm)
            modify_button.after(5,an_pulsante_m)
    # funzione animazione show        
    def an_pulsante_s():
        global my_ws, my_hs
        if my_ws <= 386  and my_hs <= 223 and expanding:
            my_ws += 5
            my_hs += 5
            show_button.configure(width=my_ws, height=my_hs)
            show_button.after(5,an_pulsante_s)
            
        elif my_ws >= 371 and my_hs >= 208 and not expanding:
            my_ws -= 5
            my_hs -= 5
            show_button.configure(width=my_ws, height=my_hs)
            show_button.after(5,an_pulsante_s)

    #funzione se sopra pulsante aggiungi
    def hover_a(event):
        global expanding
        expanding = True
        an_pulsante_a()
    
    #funzione se non sopra pulsante aggiungi
    def not_hover_a(event):
        global expanding
        expanding = False
        an_pulsante_a()
    
    #funzione se sopra pulsante remove
    def hover_r(event):
        global expanding
        expanding = True
        an_pulsante_r()
    
    #funzione se non sopra pulsante remove
    def not_hover_r(event):
        global expanding
        expanding = False
        an_pulsante_r()
        
    #funzione se sopra pulsante modify
    def hover_m(event):
        global expanding
        expanding = True
        an_pulsante_m()
    
    #funzione se non sopra pulsante modify
    def not_hover_m(event):
        global expanding
        expanding = False
        an_pulsante_m()
    #funzione se sopra pulsante show
    def hover_s(event):
        global expanding
        expanding = True
        an_pulsante_s()
    
    #funzione se non sopra pulsante show
    def not_hover_s(event):
        global expanding
        expanding = False
        an_pulsante_s()
        
   
    
    #pulsanti first frame
    immagine_add = ctk.CTkImage(Image.open(add_path), size=(100,100))
    add_button = ctk.CTkButton(first_f, 
                               text='ADD', 
                               text_color='#15043A', 
                               font=('Arial Rounded MT Bold', 42), 
                               command=popup_add, 
                               image=immagine_add, 
                               corner_radius=20, 
                               width= my_wa, 
                               height=my_ha, 
                               fg_color='#5f19e1', 
                               compound='top',
                               hover_color='#5730e2')
    add_button.place (x=101, y=171)
    add_button.bind('<Enter>', hover_a )
    add_button.bind('<Leave>', not_hover_a)
    
    
    immagine_remove = ctk.CTkImage(Image.open(remove_path), size=(100,100))
    remove_button = ctk.CTkButton(first_f, 
                                  text='REMOVE',
                                  image=immagine_remove,
                                  font=('Arial Rounded MT Bold', 42), 
                                  compound='top', 
                                  text_color='#15043A', 
                                  command=popump_rem, 
                                  corner_radius=20, 
                                  width= my_wr, 
                                  height=my_hr, 
                                  fg_color='#5f19e1',
                                  hover_color='#5730e2')
    remove_button.place(x=575, y=171)
    remove_button.bind('<Enter>', hover_r )
    remove_button.bind('<Leave>', not_hover_r)
    remove_button.propagate(False)
    
    modify_image = ctk.CTkImage(Image.open(modify_path),size=(100,100))
    modify_button = ctk.CTkButton(first_f, 
                                  text='MODIFY', 
                                  text_color='#15043A', 
                                  font=('Arial Rounded MT Bold', 42), 
                                  image=modify_image, compound='top', 
                                  command=popop_mod, corner_radius=20, 
                                  width= my_wm,
                                  height=my_hm,
                                  fg_color='#5f19e1',
                                  hover_color='#5730e2')
    modify_button.place(x=101, y=449)
    modify_button.bind('<Enter>', hover_m )
    modify_button.bind('<Leave>', not_hover_m)
    modify_button.propagate(False)
    
    show_image = ctk.CTkImage(Image.open(show_path), size=(100,100))
    show_button = ctk.CTkButton(first_f, 
                                text='SHOW', 
                                font=('Arial Rounded MT Bold', 42), 
                                image= show_image,
                                compound='top', 
                                text_color='#15043A',
                                command=popup_show, 
                                corner_radius=20,
                                width= my_ws, 
                                height=my_hs,
                                fg_color='#5f19e1',
                                hover_color='#5730e2')
    show_button.place(x=575, y=449)
    show_button.bind('<Enter>', hover_s)
    show_button.bind('<Leave>', not_hover_s)
    show_button.propagate(False)

    
    root.mainloop()
    
    
