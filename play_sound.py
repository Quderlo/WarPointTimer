import pygame
import time

pygame.init()

def play_sound():
    pygame.mixer.music.load("sound.mp3")  # Загрузка звукового файла
    pygame.mixer.music.play()  # Проигрывание звука