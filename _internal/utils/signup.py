import os
import time
import requests
import asyncio
import uuid
import httpx

from colorama import Fore, Style, init
from utils.proxy_manager import get_random_proxy
from urllib.parse import quote

init(autoreset=True)


def load_capsolver_key_from_file():
    file_path = os.path.join(os.path.dirname(__file__), "capsolver.txt")
    try:
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("")  # Crear el archivo vacío si no existe
            print("Capsolver API key file created. Please add your API key.")
            return None

        with open(file_path, "r") as file:
            capsolver_key = file.read().strip()
            if not capsolver_key:
                raise ValueError("Capsolver API key is empty.")
            return capsolver_key

    except FileNotFoundError:
        print("Error: Capsolver API key file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the Capsolver API key: {e}")
        return None


def send_discord_webhook(status_code, email, module, proxy):
    file_path = os.path.join(os.path.dirname(__file__), "discord_webhook.txt")
    try:
        with open(file_path, "r") as f:
            webhook_url = f.read().strip()
            if not webhook_url:
                raise ValueError("Discord webhook URL is empty.")
    except FileNotFoundError:
        print("Error: Discord webhook URL file not found.")
        return
    except Exception as e:
        print(f"An error occurred while loading the Discord webhook URL: {e}")
        return

    # Determinar color según código de estado
    color = 0x00FF00 if status_code in (200, 201) else 0xFF0000
    status_message = (
        "Completed" if status_code in (200, 201) else f"Failed with {status_code} code"
    )

    embed = {
        "title": f"Signup {status_message}",
        "color": color,
        "fields": [
            {"name": "Module", "value": module, "inline": False},
            {"name": "Email", "value": email, "inline": False},
            {"name": "Proxy", "value": f"||{proxy}||" or "None", "inline": False},
        ],
        "footer": {
            "text": "Powered by Ticketwave",
            "icon_url": "https://i.imgur.com/fjHwjPx.png",
        },
    }

    data = {
        "username": "Ticketwave App",
        "avatar_url": "https://i.imgur.com/fjHwjPx.png",
        "embeds": [embed],
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(
                f"Failed to send Discord webhook: {response.status_code} - {response.text}"
            )
    except Exception as e:
        print(f"An error occurred while sending Discord webhook: {e}")


async def signup_lady_gaga(
    email, country, completed_signups, API_KEY, API_ENDPOINT, PROXIES, retries, pbar
):
    url = f"{API_ENDPOINT}/signup/ladygaga"
    headers = {"X-API-KEY": API_KEY}
    capsolver_key = load_capsolver_key_from_file()
    proxy = get_random_proxy(PROXIES)
    data = {
        "email": email,
        "country": country,
        "proxy": proxy,
        "capsolver_key": capsolver_key,
    }

    task_id = str(uuid.uuid4())
    attempts = 0

    proxy_mounts = {
        "http://": proxy,
        "https://": proxy,
    }

    async with httpx.AsyncClient(proxies=proxy_mounts, verify=False, timeout=60) as client:
        while attempts < retries:
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json=data,
                )

                if response.status_code in [200, 201]:
                    completed_signups.append(f"Signup completed for {email}")
                    send_discord_webhook(
                        response.status_code, email, "Lady Gaga", proxy
                    )
                    pbar.set_postfix(
                        {"Status": Fore.GREEN + "Completed" + Style.RESET_ALL}
                    )
                    return {"task_id": task_id, "status": "Completed"}
                else:
                    raise Exception(
                        f"Signup failed with status code {response.status_code}"
                    )

            except Exception as e:
                attempts += 1
                if attempts < retries:
                    await asyncio.sleep(1)  # Breve pausa antes del siguiente intento
                else:
                    error_message = f"Max retries reached for {email}. Error: {str(e)}"
                    completed_signups.append(error_message)
                    send_discord_webhook("Undefined", email, "Lady Gaga", proxy)
                    pbar.set_postfix(
                        {
                            "Status": Fore.RED + "Failed" + Style.RESET_ALL,
                            "Error": Fore.RED + error_message + Style.RESET_ALL,
                        }
                    )
                    return {
                        "task_id": task_id,
                        "status": "Failed",
                        "error": error_message,
                    }


async def signup_tyler(
    first_name,
    last_name,
    email,
    postal_code,
    completed_signups,
    API_KEY,
    API_ENDPOINT,
    PROXIES,
    retries,
    pbar,
):
    url = f"{API_ENDPOINT}/signup/tylerthecreator"
    headers = {"X-API-KEY": API_KEY}

    proxy = get_random_proxy(PROXIES)
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "postal_code": postal_code,
        "proxy": proxy,
    }

    task_id = str(uuid.uuid4())
    attempts = 0

    proxy_mounts = {
        "http://": proxy,
        "https://": proxy,
    }

    async with httpx.AsyncClient(proxies=proxy_mounts, verify=False) as client:
        while attempts < retries:
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json=data,
                )

                if response.status_code in [200, 201]:
                    completed_signups.append(f"Signup completed for {email}")
                    send_discord_webhook(
                        response.status_code, email, "Tyler The Creator", proxy
                    )
                    pbar.set_postfix(
                        {"Status": Fore.GREEN + "Completed" + Style.RESET_ALL}
                    )
                    return {"task_id": task_id, "status": "Completed"}

                else:
                    raise Exception(
                        f"Signup failed with status code {response.status_code}"
                    )

            except Exception as e:
                attempts += 1
                if attempts < retries:
                    pbar.set_postfix(
                        {"Status": Fore.RED + "Retrying..." + Style.RESET_ALL}
                    )
                    await asyncio.sleep(1)  # Breve pausa antes del siguiente intento
                else:
                    error_message = f"Max retries reached for {email}. Error: {str(e)}"
                    completed_signups.append(error_message)
                    send_discord_webhook("Undefined", email, "Tyler The Creator", proxy)
                    pbar.set_postfix(
                        {
                            "Status": Fore.RED + "Failed" + Style.RESET_ALL,
                            "Error": Fore.RED + error_message + Style.RESET_ALL,
                        }
                    )
                    return {
                        "task_id": task_id,
                        "status": "Failed",
                        "error": error_message,
                    }
