import time

def main_loop():
    while True:
        print("Dit is een oneindige loop...")
        with open("test.txt", "a") as f:
            f.write(f"Loop uitgevoerd om {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        time.sleep(5)  # Pauzeert 5 seconden om overmatige CPU-gebruik te voorkomen

if __name__ == "__main__":
    main_loop()