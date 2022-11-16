from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchAttributeException


coursesLinks = []
subLessonLinks = []
urlDictionary = {}
driveLinks = []
driver = webdriver.Chrome()

def login_to_website(username, password):
    u = driver.find_element(By.ID, 'userid')
    u.send_keys(username)
    p = driver.find_element(By.ID, 'password')
    p.send_keys(password)
    p.send_keys(Keys.ENTER)
    driver.get('https://ilearn.cyber.org.il/user_dashboard')

def get_all_courses():
    driver.get('https://ilearn.cyber.org.il/user/completed/')
    elements = driver.find_elements(By.TAG_NAME, 'a')
    for element in elements:
        try:
            link = element.get_attribute("href")
            if "student_class" in link:
                coursesLinks.append(link)
        except:
            print("a was without course")



def get_all_course_links(course_link):
    urlDictionary.clear()
    driver.get(course_link)
    driveLinks.append(" ------------------- " + get_course_title() + " ------------------")
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    for element in elems:
        add_link_to_dictionary(element)

def get_course_title():
    element = driver.find_element(By.CLASS_NAME, "sectionTitle")
    textElement = element.find_element(By.TAG_NAME, "h1").text
    return textElement

def add_link_to_dictionary(element):
    link = element.get_attribute("href")
    if 'lesson_id=' in link:
        lessonName = element.find_element(By.TAG_NAME, "h2").text
        urlDictionary[link] = lessonName

def get_drive_from_lesson(link):
    links = []
    try:
        driver.get(link)
        if len(subLessonLinks) == 0:
            get_sublessons()
        driveElement = driver.find_elements(By.TAG_NAME, 'a')
        for element in driveElement:
            try:
                if "drive" in element.get_attribute("href"):
                    links.append(element.get_attribute("href"))
            except:
                print("Couldn't find link in a container (It's fine...)")
        return links
    except:
        return []

def get_sublessons():
    collumnElement = driver.find_element(By.CLASS_NAME, 'open')
    ulElement = collumnElement.find_element(By.TAG_NAME, 'ul')
    aElement = ulElement.find_elements(By.TAG_NAME, 'a')
    for item in aElement:
        try:
            link = item.get_attribute("href")
            if "section_id" in link and item.get_attribute('class') != "selected":
                subLessonLinks.append(link)
        except NoSuchAttributeException:
            print('link')


def get_all_drives():
    for link in urlDictionary:
        driveLinks.append(urlDictionary[link]+ ": \n" + "\n".join(get_drive_from_lesson(link)))
        for link in subLessonLinks:
                driveLinks.append("\n".join(get_drive_from_lesson(link)))
        subLessonLinks.clear()

def save_to_file():
    with open("allDriveLinks.txt", "w") as txt_file:
        for link in driveLinks:
            txt_file.write(link + "\n")

def main():
    driver.get("https://ilearn.cyber.org.il/")

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    login_to_website(username, password)

    get_all_courses()
    for link in coursesLinks:
        get_all_course_links(link)
        get_all_drives()
    save_to_file()
    driver.quit()

if __name__ == "__main__":
    main()
