import asyncio
import traceback
import os
import subprocess
import sys
import yaml

from dotenv import load_dotenv
from pydoll.browser.chromium import Chrome

load_dotenv()

SERVER = os.getenv("LOGIN_SERVER")
wt = 1
running = True

def clr_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear')

async def main_menu():

    menu_actions = {
        '1':{"title": "Absent all", "func": all_account},
        '2':{"title": "Just an account", "func": one_account},
        '3':{"title": "Custom account", "func": custom_account},
        '0':{"title": "Exit", "func": program_exit},
    }

    while running:
        clr_screen()
        menu_header("Available Command:")
        for key, value in menu_actions.items():
            print(f"[{key}] {value['title']}")

        choice = input("\nSelect an option: ").strip()

        if choice in menu_actions:
            await menu_actions[choice]["func"]()
        else:
            print("Invalid selection. Please try again.")
            await asyncio.sleep(wt)

def get_accounts():
    with open("data/accounts.yaml", "r") as file:
        return yaml.safe_load(file)

def menu_header(text=None):
    clr_screen()
    print("PBx Sleman Presence Record")
    print("======= PBxS_APR v.1.0 RLS\n")
    if text is not None:
        print(text)

async def one_account():
    accounts = get_accounts()
    if not accounts:
        print("You don't have any saved account.")
        await asyncio.sleep(2)
        return False
    
    n = 1
    account_list = {}
    for key, value in accounts.items():
        account_list[f"{n}"] = {"email": key, "password": value}
        n += 1
    
    l = True
    while l:
        menu_header("One account to record.")
        for key, value in account_list.items():
            print(f"  [{key}] {value['email']}")

        print("\nType 0 to cancel")
        select = input("Select an account (number): ")

        if select.strip() == "0":
            l = False
            return False

        if select in account_list:
            l = False
            grab_account = account_list[select]
            email = grab_account["email"]
            password = grab_account["password"]
            await accounting({email:password})
        else:
            print("\nInvalid selecton. Please try again.")
            await asyncio.sleep(wt)

async def all_account():
    accounts = get_accounts()
    if accounts:
        await accounting(accounts)
    else:
        print("You don't have any saved account.")
        await asyncio.sleep(2)
        return False

async def custom_account():
    menu_header("Absence for custom account\n")

    account = {
        "email":"your.email@gmail.com",
        "password":"1234568"
    }

    print("Type 0 to cancel")
    email = input("Enter an email: ").strip()
    if email.strip() == "0":
        return False
    elif email == "":
        print("Email or password can't be null")
        await asyncio.sleep(wt)
        return False

    password = input("Enter the password: ").strip()

    if email or password is None:
        print("Email or password can't be null")
        await asyncio.sleep(wt)
        return False

    account.update({"email":email})
    account.update({"password":password})

    await accounting(account)

async def accounting(accounts:dict):
    for email, password in accounts.items():
        await simulation(email, password)

async def simulation(email, password):
    async with Chrome() as browser:
        tab = await browser.start()
        await browser.set_window_maximized()
        tab.mouse.debug = True
        async with tab.expect_and_bypass_cloudflare_captcha():
            await tab.go_to(SERVER)

        print('Turnstile handled, continuing...')

        email_field = await tab.find(tag_name="input", type="email", name="email")
        await email_field.type_text(text=email)
        
        password_field = await tab.find(tag_name="input", type="password", name="password")
        await password_field.type_text(text=password, humanize=True)

        login_submit = await tab.find(tag_name="button", type="submit")
        await login_submit.click()

        error_element = await tab.find(
            css_selector=".text-danger",
            text="These credentials do not match our records.",
            timeout=4,
            raise_exc=False,
        )
        
        if error_element:
            print(f"Login Failed for {email}: Invalid credentials.")
            return False
        
        try:
            presence_button = await tab.find(tag_name="button", type="button", data_bs_target="#modalPresensi")
            await presence_button.click(humanize=True)

            await asyncio.sleep(1)

            presence = await tab.query("//input[@value='1']/..")
            await presence.click(humanize=True)

            presence_submit = await tab.find(xpath="//button[contains(., 'Simpan Presensi')]")
            await presence_submit.click(humanize=True)
        
        except:
            pass

        print("Presence has been checked.")
        traceback.print_exc
        return

async def program_exit():
    print("Exiting program...")
    running = False
    sys.exit(0)

asyncio.run(main_menu())