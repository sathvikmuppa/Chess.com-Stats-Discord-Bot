from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from info import mac_webdriver, win_webdriver


class Stats:

    def checkExistence(self, user):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(win_webdriver, chrome_options=options)
        driver.get(f'https://www.chess.com/stats/live/rapid/{user}')

        try:
            driver.find_element_by_class_name('error-pages-title')
            driver.quit()
            return False
        except Exception:
            driver.quit()
            return True
        driver.quit()

    def getScore(self, user):
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(
            win_webdriver, chrome_options=options)
        driver.get(f'https://www.chess.com/stats/live/rapid/{user}')

        if 'Unrated' in driver.find_element_by_css_selector('div.rating-block-container').text:
            driver.quit()
            return 1
        else:
            rating = driver.find_element_by_css_selector(
                'div.rating-block-container').text
            wins = driver.find_elements_by_css_selector(
                'div.tricolor-bar-text')[0].text
            losses = driver.find_elements_by_css_selector(
                'div.tricolor-bar-text')[1].text
            draws = driver.find_elements_by_css_selector(
                'div.tricolor-bar-text')[2].text
            driver.quit()
            output = [rating, wins, losses, draws]
            return output

    def getAllStats(self, guild):
        f = open(f'{guild} users.txt', 'r')
        stat = Stats()
        output = []
        users = []
        for line in f:
            user = line.strip('\n')
            users.append(user)
            if stat.checkExistence(user):
                score = stat.getScore(user)
                if score == 1:
                    output.append(f'Unrated')
                else:
                    output.append(
                        f'{score[0]}  {score[1]}/{score[2]}/{score[3]}')
            else:
                output.append(f'{user} does not exist')
        return users, output
