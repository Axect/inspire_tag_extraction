from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_inspirehep_tag_selenium(url, driver, timeout=10):
    """
    Opens the given URL with Selenium WebDriver,
    searches for a <span class="ant-tag __UnclickableTag__"> element,
    and returns its text. If it times out or encounters an error, returns None.
    """
    driver.get(url)
    
    try:
        # Wait up to `timeout` (default 10 seconds) for the element to appear
        tag_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.ant-tag.__UnclickableTag__"))
        )
        # If the element is found, return its text
        return tag_element.text
    except:
        # Return None if there's a timeout or any other exception
        return None

def main():
    # Headless Chrome options (run without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Launch Chrome WebDriver (chromedriver must be in PATH)
    driver = webdriver.Chrome(options=chrome_options)

    print("=== INSPIRE Tag Parser (Selenium) ===")
    print("Enter a URL to parse <span class='ant-tag __UnclickableTag__'> text from the page.")
    print("Type 'quit', 'q', or 'exit' to stop.\n")

    while True:
        user_input = input("Enter INSPIRE link (or 'quit' to exit): ").strip()
        
        # If the user types a quit command, exit the loop
        if user_input.lower() in ["quit", "q", "exit"]:
            print("Exiting the program.")
            break
        
        # Render the page and extract the tag
        tag_text = get_inspirehep_tag_selenium(user_input, driver)
        
        if tag_text is not None:
            print(f"Found tag: {tag_text}\n")
        else:
            print("No tag found (None)\n")

    # Quit the WebDriver after all work is done
    driver.quit()

if __name__ == "__main__":
    main()

