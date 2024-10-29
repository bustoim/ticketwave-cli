import os
import sys
import csv
import time
import random
import asyncio
from tqdm.asyncio import tqdm

from utils.signup import signup_lady_gaga, signup_tyler


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(
        r"""
 _________  ___  ________  ___  __    _______  _________        ___       __   ________  ___      ___ _______      
|\___   ___\\  \|\   ____\|\  \|\  \ |\  ___ \|\___   ___\     |\  \     |\  \|\   __  \|\  \    /  /|\  ___ \     
\|___ \  \_\ \  \ \  \___|\ \  \/  /|\ \   __/\|___ \  \_|     \ \  \    \ \  \ \  \|\  \ \  \  /  / | \   __/|    
     \ \  \ \ \  \ \  \    \ \   ___  \ \  \_|/__  \ \  \       \ \  \  __\ \  \ \   __  \ \  \/  / / \ \  \_|/__  
      \ \  \ \ \  \ \  \____\ \  \\ \  \ \  \_|\ \  \ \  \       \ \  \|\__\_\  \ \  \ \  \ \    / /   \ \  \_|\ \ 
       \ \__\ \ \__\ \_______\ \__\\ \__\ \_______\  \ \__\       \ \____________\ \__\ \__\ \__/ /     \ \_______\
        \|__|  \|__|\|_______|\|__| \|__|\|_______|   \|__|        \|____________|\|__|\|__|\|__|/       \|_______|
                                                                                                                   
    """
    )


def view_completed_signups(completed_signups):
    clear_screen()
    print_banner()
    if completed_signups:
        print("Completed Signups:")
        for signup in completed_signups:
            print(f"- {signup}")
    else:
        print("No completed signups yet.")

    input("\nPress Enter to return to the menu...")


def get_user_input():
    while True:
        try:
            concurrent_tasks = int(
                input("Enter the number of concurrent tasks (1-20): ")
            )
            if concurrent_tasks < 1 or concurrent_tasks > 20:
                print("Please enter a number between 1 and 20.")
                continue

            retries = int(input("Enter the number of retries per task (1-4): "))
            if retries < 1 or retries > 4:
                print("Please enter a number between 1 and 4.")
                continue

            return concurrent_tasks, retries
        except ValueError:
            print("Please enter valid integer values.")


async def upload_accounts_file_lady_gaga(
    filepath, completed_signups, API_KEY, API_ENDPOINT, PROXIES
):
    clear_screen()
    print_banner()
    concurrent_tasks, retries = get_user_input()

    clear_screen()
    print_banner()
    print(
        f"[i] Module: LADY GAGA - Concurrent tasks: {concurrent_tasks} | Retries: {retries}"
    )
    print(" ")

    try:
        with open(filepath, mode="r") as file:
            reader = csv.reader(file)
            accounts = [row for row in reader]

        total_accounts = len(accounts)
        tasks = []
        pbar_list = []
        failed_accounts = []  # Lista para almacenar las cuentas que fallaron

        for account in accounts:
            if len(account) != 2:
                print(
                    f"\nSkipping invalid line (expected 'email,country' format): {account}"
                )
                continue

            email, country = account
            pbar = tqdm(
                total=1,
                desc=f"Signup for {email}",
                position=len(pbar_list),
                leave=True,
                ncols=100,
            )
            pbar_list.append(pbar)

            tasks.append(
                signup_lady_gaga(
                    email,
                    country,
                    completed_signups,
                    API_KEY,
                    API_ENDPOINT,
                    PROXIES,
                    retries,
                    pbar,
                )
            )

        for batch_start in range(0, len(tasks), concurrent_tasks):
            batch_tasks = tasks[batch_start : batch_start + concurrent_tasks]
            results = await asyncio.gather(*batch_tasks)

            # Agregar las cuentas fallidas a la lista failed_accounts
            for result, account in zip(
                results, accounts[batch_start : batch_start + concurrent_tasks]
            ):
                if result["status"] == "Failed":
                    failed_accounts.append(account)

            # Actualizar las barras de progreso al completar cada tarea
            for pbar in pbar_list:
                pbar.update(1)

        # Guardar solo las cuentas fallidas en el archivo CSV
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(failed_accounts)

        print(f"\n\n\nSignup process completed for {total_accounts} accounts.")

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading the file: {e}")

    input("\n\n\n\nPress Enter to return to the menu...")


async def upload_accounts_file_tyler(
    filepath, completed_signups, API_KEY, API_ENDPOINT, PROXIES
):
    clear_screen()
    print_banner()
    concurrent_tasks, retries = get_user_input()

    clear_screen()
    print_banner()
    print(
        f"[i] Module: TYLER THE CREATOR - Concurrent tasks: {concurrent_tasks} | Retries: {retries}"
    )
    print(" ")

    try:
        with open(filepath, mode="r") as file:
            reader = csv.reader(file)
            accounts = [row for row in reader]

        total_accounts = len(accounts)
        tasks = []
        pbar_list = []
        failed_accounts = []  # Track accounts that fail

        for account in accounts:
            if len(account) != 4:
                print(
                    f"\nSkipping invalid line (expected 'first_name,last_name,email,postal_code' format): {account}"
                )
                continue

            first_name, last_name, email, postal_code = account
            pbar = tqdm(
                total=1,
                desc=f"Signup for {email}",
                position=len(pbar_list),
                leave=True,
                ncols=100,
            )
            pbar_list.append(pbar)

            tasks.append(
                signup_tyler(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    postal_code=postal_code,
                    completed_signups=completed_signups,
                    API_KEY=API_KEY,
                    API_ENDPOINT=API_ENDPOINT,
                    PROXIES=PROXIES,
                    retries=retries,
                    pbar=pbar,
                )
            )

        for batch_start in range(0, len(tasks), concurrent_tasks):
            batch_tasks = tasks[batch_start : batch_start + concurrent_tasks]
            results = await asyncio.gather(*batch_tasks)

            for result, account in zip(
                results, accounts[batch_start : batch_start + concurrent_tasks]
            ):
                if result["status"] == "Failed":
                    failed_accounts.append(account)

            for pbar in pbar_list:
                pbar.update(1)

        # Write only failed accounts back to file
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(failed_accounts)

        print(f"\n\nSignup process completed for {total_accounts} accounts.")

    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except Exception as e:
        print(f"Error reading the file: {e}")

    input("\nPress Enter to return to the menu...")


def load_api_key_from_file(LICENCE_FILE, API_KEY):
    if os.path.join(os.path.dirname(__file__), LICENCE_FILE):
        with open(LICENCE_FILE, "r") as file:
            api_key = file.read().strip()
            if api_key:
                print(f"Loaded API Key from {LICENCE_FILE}.")
                return api_key
    return None


def save_api_key_to_file(api_key, LICENCE_FILE):
    with open(LICENCE_FILE, "w") as file:
        file.write(api_key)
    print(f"API Key saved to {LICENCE_FILE}.")


def check_for_update(current_version, repo="bustoim/Ticketwave-CLI"):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    response = requests.get(url)
    latest_version = response.json()["tag_name"]

    if latest_version != current_version:
        print(f"New version {latest_version} available! Updating...")
        subprocess.run(["git", "pull", "origin", "main"])
        print("Update complete. Please restart the CLI.")
    else:
        print("You are using the latest version.")
