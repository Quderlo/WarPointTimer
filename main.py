import timer

if __name__ == "__main__":
    window = timer.TimerWindow()
    window.attributes("-topmost", True)  # поверх всех окон
    window.mainloop()