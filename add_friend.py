from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import os


READ_INPUT_FROM_FILE = True             # If False or file doesn't exists, then takes input from user
INPUT_FILE_NAME = "friend_list.txt"     # To store CodeForces user handles in separate lines


def take_handle_input():
    """
    Takes input from a file input.txt and returns a list of handles
    If file doesn't exists then takes input from user
    """

    global READ_INPUT_FROM_FILE

    if not os.path.exists(INPUT_FILE_NAME) or not READ_INPUT_FROM_FILE:
        # File doesn't exists' so taking input from user
        handles = []
        while 1:
            handle = input("Enter CodeForces handle (or press Enter if done): ")
            if handle == "":
                break
            handles.append(handle)
        return handles

    with open(INPUT_FILE_NAME, "r") as f:
        handles = f.readlines()
    return list(set(h.strip() for h in handles))


def wait_for_login(browser):
    """
    Waits for login page to load
    """
    for i in range(1, 300):
        if browser.current_url != "https://codeforces.com/":
            sleep(1)
            if i%10 == 0:
                print("\nPlease Login into codeforces...")
        else:
            return

    print("\n\n\nUser didn't Logged in")
    print("\nProcess Halted!")
    exit(1)




# Main

if __name__ == "__main__":
    handles = take_handle_input()
    login_url = 'https://codeforces.com/enter'

    # CodeForces login
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(login_url)
    wait_for_login(driver)

    # Adding friends
    new_friends = []
    for handle in handles:
        driver.get("https://codeforces.com/profile/{}".format(handle))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        h1 = soup.find("h1")
        
        if "Click to add to friends" in str(h1.img):
            print("\nAdding {} to friends".format(handle))
            star = driver.find_element(By.TAG_NAME, "h1").find_element(By.TAG_NAME, "img")
            star.click()
            sleep(.2)
            new_friends.append(handle)
    
    print("\n\n\n\n")
    print(*new_friends, sep="\n")
    print(f"\nSuccess: {len(new_friends)} new friends added !")
    print("\nDone...")
    
    # Redirecting to My Friends page
    driver.get("https://codeforces.com/friends")
    sleep(6000)

