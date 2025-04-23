def prompt_int(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Bitte eine gültige Zahl eingeben.")
