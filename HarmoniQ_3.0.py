import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from pydub import AudioSegment
import os

# Inicializar a janela
root = tk.Tk()
root.title("HarminQ Music Player")
root.geometry("300x500")
root.configure(bg="#EEDD82")  # Cor de fundo branco gelo fosco

# Inicializar o mixer do pygame
mixer.init()

# Variável para armazenar o caminho do arquivo convertido (se necessário)
converted_song_path = None
is_playing = False  # Variável para rastrear o estado da música

# Função para carregar música
def load_song():
    global converted_song_path
    song_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.aac *.m4a")]
    )
    if song_path:
        # Se o arquivo não for .mp3 ou .wav, converte para .wav usando pydub
        if not song_path.endswith(('.mp3', '.wav')):
            converted_song = AudioSegment.from_file(song_path)
            converted_song_path = "converted_song.wav"
            converted_song.export(converted_song_path, format="wav")
            mixer.music.load(converted_song_path)
        else:
            mixer.music.load(song_path)
            converted_song_path = None  # Não há conversão

        song_label.config(text=song_path.split("/")[-1])

# Função para reproduzir ou pausar música
def toggle_play_pause():
    global is_playing
    if is_playing:
        mixer.music.pause()
        play_pause_button.config(text="Play")
        is_playing = False
    else:
        mixer.music.unpause() if mixer.music.get_busy() else mixer.music.play()
        play_pause_button.config(text="Pause")
        is_playing = True

# Função para parar a música
def stop_song():
    global is_playing
    mixer.music.stop()
    play_pause_button.config(text="Play")
    is_playing = False
    # Se uma conversão foi feita, remove o arquivo temporário
    if converted_song_path and os.path.exists(converted_song_path):
        os.remove(converted_song_path)

# Função para ajustar o volume
def set_volume(val):
    volume = float(val) / 100  # O valor do slider é de 0 a 100, mas o mixer usa 0 a 1
    mixer.music.set_volume(volume)

# Função para aumentar o volume
def increase_volume():
    current_volume = volume_slider.get()
    new_volume = min(100, current_volume + 5)
    volume_slider.set(new_volume)

# Função para diminuir o volume
def decrease_volume():
    current_volume = volume_slider.get()
    new_volume = max(0, current_volume - 5)
    volume_slider.set(new_volume)

# Estilo dos botões e labels
button_bg = "#EEDD82"  # Cor de fundo dos botões
button_fg = "#000000"  # Cor do texto dos botões
label_bg = "#EEDD82"  # Cor de fundo para o label (branco gelo fosco)
label_fg = "#000000"  # Cor do texto do label

# Label para o nome do aplicativo
app_name_label = tk.Label(root, text="HarminQ", font=("Arial", 18, "bold"), bg=label_bg, fg=label_fg)
app_name_label.pack(pady=10)

# Criar botões de controle
load_button = tk.Button(root, text="Play List", command=load_song, bg=button_bg, fg=button_fg)
load_button.pack(pady=10)

play_pause_button = tk.Button(root, text="Play", command=toggle_play_pause, bg=button_bg, fg=button_fg)
play_pause_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_song, bg=button_bg, fg=button_fg)
stop_button.pack(pady=5)

# Label para mostrar a música carregada
song_label = tk.Label(root, text="No song loaded", bg=label_bg, fg=label_fg)
song_label.pack(pady=10)

# Slider para controle de volume
volume_slider = tk.Scale(root, from_=0, to=100, orient='horizontal', label='       Volume', command=set_volume,
                         bg=label_bg, fg=label_fg, troughcolor="#EEDD82")
volume_slider.set(50)  # Volume inicial em 50%
volume_slider.pack(pady=10)

# Frame para os botões de controle de volume
volume_frame = tk.Frame(root, bg=label_bg)
volume_frame.pack(pady=5)

# Botões de controle de volume lado a lado
increase_volume_button = tk.Button(volume_frame, text="+ Vol.", command=increase_volume, bg=button_bg, fg=button_fg)
increase_volume_button.grid(row=0, column=1, padx=5)

decrease_volume_button = tk.Button(volume_frame, text="- Vol.", command=decrease_volume, bg=button_bg, fg=button_fg)
decrease_volume_button.grid(row=0, column=0, padx=5)

# Iniciar o loop do tkinter
root.mainloop()
