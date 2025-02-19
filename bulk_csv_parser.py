import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from tqdm import tqdm

def get_inspirehep_tag_selenium(url, driver, timeout=10):
    """
    Opens the given Inspire link with Selenium WebDriver and searches for 
    a <span class="ant-tag __UnclickableTag__"> element. If found, returns 
    the text (e.g., 'hep-th'); otherwise returns None.
    """
    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait up to `timeout` seconds for the specified element
        tag_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.ant-tag.__UnclickableTag__")
            )
        )
        return tag_element.text
    except Exception:
        # If an error or timeout occurs, return None
        return None

def main():
    # Parse arguments for input CSV path
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, required=True)
    args = parser.parse_args()
    
    input_csv_path = args.csv
    # Read the CSV file
    df = pd.read_csv(input_csv_path, sep=",")  # If tab-delimited, use sep="\t"
    
    # Set up headless Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)

    # Extract tag from each row's Inspire link and store in 'Area' column
    areas = []
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        url = row["Inspire link"]
        tag = get_inspirehep_tag_selenium(url, driver)
        areas.append(tag)
    
    df["Area"] = areas
    
    # Quit the driver when finished
    driver.quit()
    
    # Save the updated DataFrame to a new CSV file
    output_csv_path = f"{input_csv_path[:-4]}_with_area.csv"
    df.to_csv(output_csv_path, index=False)
    print(f"Saved updated CSV to: {output_csv_path}")

if __name__ == "__main__":
    main()
