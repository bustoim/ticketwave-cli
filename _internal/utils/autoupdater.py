import os
import requests
import zipfile
import shutil

DOWNLOAD_URL = "https://github.com/bustoim/Ticketwave-CLI/archive/refs/heads/main.zip"
DOWNLOAD_PATH = "ticketwave-cli.zip"
LOCAL_VERSION_FILE = "version.txt"  # Archivo para almacenar la versión actual

def download_zip(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Downloaded .zip file.")
    else:
        print(f"Error downloading: {response.status_code} - {response.text}")

def check_for_updates():
    # Obtener la versión del servidor
    server_version = requests.get(
        "https://raw.githubusercontent.com/bustoim/ticketwave-cli/main/version.txt"
    ).text.strip()
    try:
        with open(LOCAL_VERSION_FILE, "r") as f:
            local_version = f.read().strip()
    except FileNotFoundError:
        local_version = "0.0.0"

    if server_version != local_version:
        print("New version available. Starting update...")
        update_cli(server_version)
    else:
        print("The CLI is up to date.")

def update_cli(new_version):
    # Descargar y descomprimir la nueva versión
    download_zip(DOWNLOAD_URL, DOWNLOAD_PATH)

    # Descomprimir el archivo ZIP en un directorio temporal
    with zipfile.ZipFile(DOWNLOAD_PATH, 'r') as zip_ref:
        zip_ref.extractall("temp_update")  # Extraer en un directorio temporal

    # Copiar todos los archivos descomprimidos al directorio principal
    src_dir = "temp_update/Ticketwave-CLI-main"
    for root, dirs, files in os.walk(src_dir):
        # Crear directorios en el destino si no existen
        relative_path = os.path.relpath(root, src_dir)
        dest_dir = os.path.join(".", relative_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copiar archivos, sobrescribiendo si es necesario
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy(src_file, dest_file)

    # Limpiar: eliminar el directorio temporal
    shutil.rmtree("temp_update")
    os.remove(DOWNLOAD_PATH)  # Opcional: eliminar el archivo ZIP descargado

    # Actualizar el archivo de versión local
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(new_version)

    print("Update completed.")