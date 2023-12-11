from tkinter import *
from tkinter import messagebox
import qrcode
import psycopg2

texto_resposta = ""

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

    '''InsertOne com tratamento de exceções'''
    def insertOne(self, id, url, path):
        try:
            self.cursor.execute("INSERT INTO tbcodes (id_code, url, qrcode_path) VALUES ({}, '{}', '{}')".format(id, url, path))
        except psycopg2.Error as e:
            print("ERROR:", e.pgcode)
            self.conn.rollback()
        self.conn.commit()

    '''def selectAll(self):
        self.cursor.execute("select * from tbcodes")
        return self.cursor.fetchall()'''

    def selectAll(self, id):
        self.cursor.execute("select * from tbcodes where id_code = {}".format(id))
        return self.cursor.fetchall()

def gerar_qr_code():
    id = texto_resposta1.get()
    url = texto_resposta2.get()
    qrcode_path = texto_resposta3.get()
    
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
            banco.insertOne(id, url, qrcode_path)

def ler_qr_code():
    global banco
    id = texto_resposta1.get()
    print(banco.selectAll(id))

banco = Banco()

janela = Tk()
janela.title("Gerador de Código QRCode")

texto1 = Label(janela, text = "ID DO QRCODE: ")
texto1.grid(column = 0, row = 2, padx = 10, pady = 10)

texto_resposta1 = Entry(width = 45)
texto_resposta1.grid(column = 1, row = 2, columnspan = 2)

texto2 = Label(janela, text = "URL: ")
texto2.grid(column = 0, row = 3, padx = 10, pady = 10)

texto_resposta2 = Entry(width = 45)
texto_resposta2.grid(column = 1, row = 3, columnspan = 2)

texto3 = Label(janela, text = "QRCODE_PATH: ")
texto3.grid(column = 0, row = 4, padx = 10, pady = 10)

texto_resposta3 = Entry(width = 45)
texto_resposta3.grid(column = 1, row = 4, columnspan = 2)

botao = Button(janela, text = "Gerar QRCode", command = gerar_qr_code)
botao.grid(column = 0, row = 5, padx = 10, pady = 10)

botao_select = Button(text = "Ler QRCodes do BD", width = 25, command = ler_qr_code)
botao_select.grid(column = 0, row = 6, padx = 10, pady = 10)

janela.mainloop()
