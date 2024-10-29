import time
import os
import asyncio

from utils.utils import (
    clear_screen,
    print_banner,
    view_completed_signups,
    upload_accounts_file_lady_gaga,
    upload_accounts_file_tyler,
)

from utils.proxy_manager import load_proxies


def show_menu():
    print(
        """
[1] - Info
[2] - General configuration
[3] - Lady Gaga (Signup)
[4] - Tyler the Creator (Signup)
[5] - Exit
    """
    )


def info():
    clear_screen()
    print_banner()
    print("Bot Info:")
    print("- This is a bot to monitor event tickets.")
    print("- Version: 1.0.0")
    print("- Powered by Ticketwave")
    input("\nPress Enter to return to the menu...")


def save_capsolver_key_to_file(capsolver_key, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(capsolver_key)
        print("Capsolver API key saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the Capsolver API key: {e}")
        

def save_discord_webhook_to_file(webhook_url, file_path):
    try:
        with open(file_path, "w") as file:
            file.write(webhook_url)
        print("Webhook Url saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving the Webhook Url: {e}")
        

def configuration():
    capsolver_file_path = "_internal/utils/capsolver.txt"
    discord_webhook_file_path = "_internal/utils/discord_webhook.txt"
    
    while True:
        clear_screen()
        print_banner()
        print(
            """
[1] - Configure Capsolver API key
[2] - Configure Discord Webhook URL
[3] - Back to menu
            """
        )
        option = input("\nPlease select an option: ")
        
        if option == "1":
            print(" ")
            capsolver_key = input("Paste your Capsolver API key here: ")
            if capsolver_key:
                save_capsolver_key_to_file(capsolver_key, capsolver_file_path)
                print("Capsolver API key saved successfully.")
                time.sleep(2)
            else:
                print("No API key detected.")
                time.sleep(2)
        
        elif option == "2":
            print(" ")
            webhook_url = input("Paste your Discord Webhook URL here: ")
            if webhook_url:
                save_discord_webhook_to_file(webhook_url, discord_webhook_file_path)
                print("Discord Webhook URL saved successfully.")
                time.sleep(2)
            else:
                print("No Discord Webhook URL detected.")
                time.sleep(2)

        elif option == "3":
            break
        
        else:
            print("Invalid option. Try again.")
            time.sleep(1)


async def lady_gaga_menu(completed_signups, API_KEY, API_ENDPOINT, PROXIES):
    filepath = None
    proxies_file_path = None

    while True:
        clear_screen()
        print_banner()
        print("Lady Gaga Signup Bot Configuration:")
        print(
            """
[1] - Run sign-up
[2] - Select an accounts CSV file
[3] - Select a proxies file
[4] - View completed signups
[5] - Back to main menu
            """
        )
        choice = input("Select an option: ")

        if choice == "1":
            if not filepath:
                print("No CSV accounts file selected.")
                await asyncio.sleep(1)
            elif not proxies_file_path:
                print("No .txt proxies file selected.")
                await asyncio.sleep(1)
            else:
                await upload_accounts_file_lady_gaga(
                    filepath, completed_signups, API_KEY, API_ENDPOINT, PROXIES
                )

        elif choice == "2":
            try:
                csv_files = [f for f in os.listdir("files") if f.endswith(".csv")]
                if not csv_files:
                    print("No .csv files found in the 'files' directory.")
                    await asyncio.sleep(1)
                else:
                    print(" ")
                    for idx, file in enumerate(csv_files, start=1):
                        print(f"[{idx}] - {file}")

                    selection = input("Please select your accounts CSV file: ")
                    if selection.isdigit() and 1 <= int(selection) <= len(csv_files):
                        filepath = os.path.join("files", csv_files[int(selection) - 1])
                        print(f"Selected accounts CSV file: {filepath}")
                        await asyncio.sleep(1)
                    else:
                        print("Invalid selection. Try again.")
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"Error accessing 'files' directory: {e}")
                await asyncio.sleep(1)

        elif choice == "3":
            # List .txt files in "files" directory for proxies selection
            try:
                txt_files = [f for f in os.listdir("files") if f.endswith(".txt")]
                if not txt_files:
                    print("No .txt files found in the 'files' directory.")
                    await asyncio.sleep(1)
                else:
                    print(" ")
                    for idx, file in enumerate(txt_files, start=1):
                        print(f"[{idx}] - {file}")

                    selection = input("Please select your proxies file: ")
                    if selection.isdigit() and 1 <= int(selection) <= len(txt_files):
                        proxies_file_path = os.path.join(
                            "files", txt_files[int(selection) - 1]
                        )
                        load_proxies(proxies_file_path, PROXIES)
                        print(f"Selected proxies file: {proxies_file_path}")
                        await asyncio.sleep(1)
                    else:
                        print("Invalid selection. Try again.")
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"Error accessing 'files' directory: {e}")
                await asyncio.sleep(1)

        elif choice == "4":
            view_completed_signups(completed_signups)

        elif choice == "5":
            break

        else:
            print("Invalid option. Try again.")
            await asyncio.sleep(1)



async def tyler_the_creator_menu(completed_signups, API_KEY, API_ENDPOINT, PROXIES):
    filepath = None
    proxies_file_path = None

    while True:
        clear_screen()
        print_banner()
        print("Tyler the Creator Signup Bot Configuration:")
        print(
            """
[1] - Run sign-up
[2] - Select a CSV file with accounts
[3] - Select a proxies file
[4] - View completed signups
[5] - Back to main menu
            """
        )
        choice = input("Select an option: ")

        if choice == "1":
            if not filepath:
                print("No CSV file selected for accounts.")
                await asyncio.sleep(1)
            elif not proxies_file_path:
                print("No proxies file selected.")
                await asyncio.sleep(1)
            else:
                await upload_accounts_file_tyler(
                    filepath, completed_signups, API_KEY, API_ENDPOINT, PROXIES
                )
        elif choice == "2":
            # List CSV files in "files" directory for accounts selection
            try:
                csv_files = [f for f in os.listdir("files") if f.endswith(".csv")]
                if not csv_files:
                    print("No CSV files found in the 'files' directory.")
                    await asyncio.sleep(1)
                else:
                    print(" ")
                    for idx, file in enumerate(csv_files, start=1):
                        print(f"[{idx}] - {file}")

                    selection = input("Please select your accounts file: ")
                    if selection.isdigit() and 1 <= int(selection) <= len(csv_files):
                        filepath = os.path.join("files", csv_files[int(selection) - 1])
                        print(f"Selected accounts file: {filepath}")
                        await asyncio.sleep(1)
                    else:
                        print("Invalid selection. Try again.")
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"Error accessing 'files' directory: {e}")
                await asyncio.sleep(1)

        elif choice == "3":
            # List .txt files in "files" directory for proxies selection
            try:
                txt_files = [f for f in os.listdir("files") if f.endswith(".txt")]
                if not txt_files:
                    print("No .txt files found in the 'files' directory.")
                    await asyncio.sleep(1)
                else:
                    print(" ")
                    for idx, file in enumerate(txt_files, start=1):
                        print(f"[{idx}] - {file}")

                    selection = input("Please select your proxies file: ")
                    if selection.isdigit() and 1 <= int(selection) <= len(txt_files):
                        proxies_file_path = os.path.join("files", txt_files[int(selection) - 1])
                        load_proxies(proxies_file_path, PROXIES)
                        print(f"Selected proxies file: {proxies_file_path}")
                        await asyncio.sleep(1)
                    else:
                        print("Invalid selection. Try again.")
                        await asyncio.sleep(1)
            except Exception as e:
                print(f"Error accessing 'files' directory: {e}")
                await asyncio.sleep(1)

        elif choice == "4":
            view_completed_signups(completed_signups)

        elif choice == "5":
            break

        else:
            print("Invalid option. Try again.")
            await asyncio.sleep(1)
