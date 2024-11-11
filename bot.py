
import json
from tkinter import *

import requests
from handlers.extract import class_prediction, get_response
from keras.models import load_model
from PIL import Image, ImageTk
from io import BytesIO

model = load_model('model.h5')

intents = json.loads(open('intents.json').read())

base = Tk()
base.title("Omnichat - Teste")
base.geometry("400x500") 
base.resizable(width=FALSE, height=FALSE)

url = "https://app.omni.chat/assets/branding/open-graph.png"

# Passo 1: Baixar a imagem da internet
response = requests.get(url)
image_data = response.content

# Passo 2: Abrir a imagem com Pillow
image = Image.open(BytesIO(image_data))

def chatbot_response(msg):
    ints = class_prediction(msg, model)
    res = get_response(ints, intents, msg)
    return res

def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    if msg != '':
        Chat.config(state=NORMAL)
        Chat.insert(END, f"Você: {msg}\n\n")
        Chat.config(foreground="#000000", font=("Arial", 12))

        response = chatbot_response(msg)
        Chat.insert(END, f"Bot: {response}\n\n")

        Chat.config(state=DISABLED)
        Chat.yview(END)


Chat = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
Chat.config(state=DISABLED)

scrollbar = Scrollbar(base, command=Chat.yview)
Chat['yscrollcommand'] = scrollbar.set

SendButton = Button(base, font=("Verdana", 10, 'bold'), text="Enviar", width="12", height=2, bd=0, bg="#666", activebackground="#333", fg='#ffffff', command=send)

EntryBox = Text(base, bd=0, bg="white", width="29", height="2", font="Arial")

image = Image.open(BytesIO(image_data))
image.thumbnail((400, 70))
fundo_branco = Image.new("RGB", (400, 70), "white")
posicao = ((400 - image.width) // 2, (70 - image.height) // 2)
fundo_branco.paste(image, posicao)
tk_image = ImageTk.PhotoImage(fundo_branco)
label = Label(base, image=tk_image)

scrollbar.place(x=376, y=6, height=386)
Chat.place(x=6, y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=50, width=260)
SendButton.place(x=6, y=401, height=50)
label.place(x=0, y=452, height=50)
base.mainloop()
