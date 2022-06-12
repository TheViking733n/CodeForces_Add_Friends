# CodeForces_Add_Friends
### _Automatically adds friends on CodeForces from a list of handles._
A simple selenium and webscraping project I made to automate the process of adding friends to my alternate CodeForces handle.

## Features
- Easy to Use and Fast 🙂
- Automatically detects those handles which are already in your friends 🔥
- Cross Platform 💻
- No technical knowledge required to use 😎


## Dependencies
- [Selenium](https://github.com/SeleniumHQ/Selenium)
- [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)


## Installation
```sh
pip install selenium
```
```sh
pip install webdriver-manager
```
```sh
pip install beautifulsoup4
```
```sh
pip install lxml
```

## Usage
1. First add the list of handles in the text file, "friend_list.txt" in seperate lines.
2. Install all the above dependencies. 
3. Run the python code using below command. 
  ```sh
  python3 add_friend.py
  ```
5. In the browser window, login your CodeForces account.
6. Sit back and relax. 👍



## How it works
It first prompts the user to login, then it fetches all the friends of the user, so that it adds only those handles which are not already friend of user.
