import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageSequence

# Função para calcular e exibir o gráfico de pizza com imagem de fundo
def calcular_tempo():
    try:
        # Obtém os horários inseridos pelo usuário
        hora_acordar = entry_acordar.get()
        hora_dormir = entry_dormir.get()

        # Converte os horários para o formato datetime
        formato_hora = "%H:%M"
        acordar = datetime.strptime(hora_acordar, formato_hora)
        dormir = datetime.strptime(hora_dormir, formato_hora)

        # Calcula o tempo acordado
        if dormir < acordar:
            dormir += timedelta(days=1)  # Ajusta se o horário de dormir passar da meia-noite
        tempo_acordado = (dormir - acordar).total_seconds() / 3600  # Converte segundos para horas

        # Obtém os tempos de responsabilidades
        tempo_responsabilidades = float(entry_responsabilidades.get())
        tempo_estudo = float(entry_estudo.get())
        tempo_trabalho = float(entry_trabalho.get())

        # Soma o tempo de todas as responsabilidades
        tempo_total_responsabilidades = tempo_responsabilidades + tempo_estudo + tempo_trabalho

        # Verifica se o tempo total de responsabilidades ultrapassa o tempo acordado
        if tempo_total_responsabilidades > tempo_acordado:
            messagebox.showwarning("Atenção", "O tempo de responsabilidades excede o tempo acordado disponível.")
            return

        # Calcula o tempo livre restante
        tempo_restante = tempo_acordado - tempo_total_responsabilidades

        # Dados para o gráfico de pizza
        labels = ['Tempo Livre Restante', 'Responsabilidades', 'Estudo', 'Trabalho']
        valores = [tempo_restante, tempo_responsabilidades, tempo_estudo, tempo_trabalho]
        cores = ['#66b3ff', '#ff9999', '#99ff99', '#ffcc99']

        # Criar o gráfico de pizza
        fig, ax = plt.subplots(figsize=(7, 7))

        # Carregar a imagem de fundo
        img = plt.imread("fundo.png")
        ax.imshow(img, extent=[-1, 1, -1, 1], aspect='auto')

        # Gerar o gráfico de pizza
        ax.pie(valores, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Assegura que o gráfico seja desenhado como um círculo

        # Título
        plt.title("Gestão de Tempo Livre e Responsabilidades")
        plt.show()

    except ValueError:
        # Exibe um erro caso o usuário insira valores inválidos
        messagebox.showerror("Erro", "Por favor, insira valores válidos para horários e responsabilidades.")

# Função para atualizar o GIF redimensionado
def update_gif():
    global gif_frame
    gif_frame = gif_frame % len(gif_frames)
    frame = gif_frames[gif_frame]
    resized_frame = frame.resize((janela.winfo_width(), janela.winfo_height()), Image.ANTIALIAS)
    tk_frame = ImageTk.PhotoImage(resized_frame)
    gif_label.config(image=tk_frame)
    gif_label.image = tk_frame  # Manter referência para evitar coleta de lixo
    gif_frame += 1
    janela.after(100, update_gif)

# Configuração da janela principal
janela = tk.Tk()
janela.title("Gestão de Tempo Livre")
janela.state('zoomed')  # Coloca a janela em tela cheia

# Carregar o GIF e preparar os frames para a animação
gif_bg = Image.open("fundo2.gif")
gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif_bg)]
gif_frame = 0  # Índice do frame atual
gif_label = tk.Label(janela)
gif_label.place(x=0, y=0, relwidth=1, relheight=1)

# Iniciar a animação do GIF em tela cheia
janela.after(0, update_gif)

# Criação dos elementos de interface
label_acordar = tk.Label(janela, text="Hora que acorda (HH:MM):", bg="white")
label_acordar.pack(pady=5)

entry_acordar = tk.Entry(janela)
entry_acordar.pack(pady=5)

label_dormir = tk.Label(janela, text="Hora que dorme (HH:MM):", bg="white")
label_dormir.pack(pady=5)

entry_dormir = tk.Entry(janela)
entry_dormir.pack(pady=5)

label_responsabilidades = tk.Label(janela, text="Tempo para outras responsabilidades (em horas):", bg="white")
label_responsabilidades.pack(pady=5)

entry_responsabilidades = tk.Entry(janela)
entry_responsabilidades.pack(pady=5)

label_estudo = tk.Label(janela, text="Tempo de estudo (em horas):", bg="white")
label_estudo.pack(pady=5)

entry_estudo = tk.Entry(janela)
entry_estudo.pack(pady=5)

label_trabalho = tk.Label(janela, text="Tempo de trabalho (em horas):", bg="white")
label_trabalho.pack(pady=5)

entry_trabalho = tk.Entry(janela)
entry_trabalho.pack(pady=5)

# Botão para calcular e gerar o gráfico
botao_calcular = tk.Button(janela, text="Calcular e Exibir Gráfico", command=calcular_tempo)
botao_calcular.pack(pady=20)

# Inicia o loop da interface gráfica
janela.mainloop()
