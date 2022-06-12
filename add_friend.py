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
    return [h.strip() for h in handles]


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


    # Fetching handles that are already friend of this user
    print("\nFetching those handles which are already in your friends...\n")
    driver.get("https://codeforces.com/friends")
    sleep(.5)
    if driver.current_url.startswith("https://codeforces.com/enter"):
        print("\n\n\nUser didn't Logged in")
        print("\nProcess Halted!")
        exit(1)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    friends_list = []
    try:
        table = soup.find("div", {"class": "datatable"}).find("tbody")
        rows = table.find_all("tr")
        for row in rows:
            friend_handle = row.find_all("td")[1].text
            friends_list.append(friend_handle)
    except:
        pass

    # Removing all handles which are already friend of the user
    not_friends = []
    for handle in handles:
        if handle not in friends_list and handle not in not_friends and handle != "":
            not_friends.append(handle)

    # # For debugging
    # print(handles)        # Handles in input file
    # print(friends_list)   # List of friends of user
    # print(not_friends)    # List of handles which are not friends of user

    # Adding friends
    new_friends = []
    for handle in not_friends:
        try:
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
        except Exception as e:
            print(f"Handle doesn't exist: {handle}")
            # print(e)
    
    print("\n\n\n\n")
    print(f"\nSuccess: {len(new_friends)} new friends added !")
    print(*new_friends, sep="\n")
    print("\nDone...")
    
    # Redirecting to My Friends page
    driver.get("https://codeforces.com/friends")
    sleep(6000)

