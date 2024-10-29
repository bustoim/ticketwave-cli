import random
import time

def load_proxies(file_path, proxies_list):
    """Load proxies from a file into a provided list."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:  # Verifica que la línea no esté vacía
                    proxies_list.append(proxy)
        print(f"{len(proxies_list)} proxies loaded from {file_path}.")  # Agrega esta línea para verificar la carga
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while loading proxies: {e}")



def get_random_proxy(PROXIES):
    if len(PROXIES) > 0:
        proxy = str(random.choice(PROXIES)).split(":")
        if len(proxy) > 2:
            ip, port, user, password = proxy 
            return f"http://{user}:{password}@{ip}:{port}"
        else:
            ip, port = proxy
            return f"http://{ip}:{port}"
    return None