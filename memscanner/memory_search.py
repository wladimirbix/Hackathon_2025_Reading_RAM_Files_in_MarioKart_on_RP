import subprocess

def search_memory_value(address, value):
    """
    Überprüft, ob der angegebene Wert an der gegebenen Speicheradresse im Prozess existiert.
    :param address: Die zu überprüfende Speicheradresse.
    :param value: Der Wert, nach dem gesucht wird.
    :return: True, wenn der Wert an der Adresse gefunden wurde, sonst False.
    """
    try:
        # Lese den Speicher an der angegebenen Adresse mit `gdb`
        command = f"gdb -batch -ex 'attach 7224' -ex 'x/1xb {address:#x}'"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Suche nach dem Wert "1" in der Ausgabe
        if str(value) in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Fehler beim Überprüfen der Adresse {address}: {e}")
        return False
