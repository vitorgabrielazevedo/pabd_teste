from tkinter import *
from tkinter import messagebox
import qrcode
import psycopg2

class Banco():
    def __init__(self):
        self.conn = psycopg2.connect(
            host = "localhost",
            database = "qrcode",
            user = "postgres",
            password = "pabd"
        )

        self.cursor = self.conn.cursor()

    def insertOne(self, id, url, path):
        self.cursor.execute("INSERT INTO tbcodes (id_code, url, qrcode_path) VALUES ({}, '{}', '{}')".format(id, url, path))
        self.conn.commit()

def gerar_qr_code():
    url = texto_resposta.get()
    
    if (len(url) == 0):
        messagebox.showinfo(
            title = "Erro!",
            message = "Inserir URL válida"
        )
    
    else:
        opcao = messagebox.askokcancel(
            title = url,
            message = f"O endereço é: \n"
                    f"Endereço: {url} \n"
                    f"Salvar?"
        )

        if opcao:
            qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)
            qr.add_data(url)
            qr.make(fit = True)
            img = qr.make_image(fill_color = 'black', back_color = 'white')
            img_save = 'qrExport.png'
            img.save(img_save)
            banco.insertOne(2, url, 'qrCode.png')

banco = Banco()

janela = Tk()
janela.title("Gerador de Código QRCode")

texto1 = Label(janela, text = "ID DO QRCODE: ")
texto1.grid(column = 0, row = 2, padx = 10, pady = 10)

texto_resposta1 = Entry(width = 45)
texto_resposta1.grid(column = 1, row = 2, columnspan = 2)

texto2 = Label(janela, text = "URL: ")
texto2.grid(column = 2, row = 2, padx = 10, pady = 10)

texto_resposta2 = Entry(width = 45)
texto_resposta2.grid(column = 3, row = 2, columnspan = 2)

texto3 = Label(janela, text = "QRCODE_PATH: ")
texto3.grid(column = 4, row = 2, padx = 10, pady = 10)

texto_resposta3 = Entry(width = 45)
texto_resposta3.grid(column = 5, row = 2, columnspan = 2)

botao = Button(janela, text = "Gerar QRCode", command = gerar_qr_code)
botao.grid(column = 6, row = 3, padx = 10, pady = 10)

janela.mainloop()

