import time
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

"""run this script, will require user input, what FTSE indices are required? 100, 250 or 350, will create & save csv """


# Correct version of chromedriver must be installed, update path below with your location of chromedriver #
CHROMEDRIVER_PATH = r'C:\Development\chromedriver.exe'

options = Options()
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

# Choose if you want chrome window to open or not
options.add_argument('--headless')
# options.add_argument('--start-maximized')

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)


def update_ftse_100_csv(index: int):
    x = index
    try:
        # Open webpage
        driver.get(f'https://www.fidelity.co.uk/shares/ftse-{x}/')
        time.sleep(2)
    except Exception as ex:
        print(ex)
        print('could not access webpage')

    try:
        # find html table, convert to dataframe
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all('table')
        tables_dfs = pd.read_html(str(tables))
        ftse_df = tables_dfs[0]
        ftse_df.to_csv(f'ftse_{x}.csv', index=False)
        print('csv file updated!')
    except Exception as ex:
        print(ex)
        print('could not create csv file')

    time.sleep(1)
    driver.quit()


if __name__ == '__main__':
    print('Starting!')

    try:
        indices = [100, 250, 350]
        index_choice = int(input('Enter 100, 250 or 350: '))
        if index_choice in indices:
            update_ftse_100_csv(index_choice)
        else:
            print('You did not enter 100, 250 or 350, run program again')
    except ValueError:
        print('You did not enter 100, 250 or 350, run program again')

    print('Program Finished!')
