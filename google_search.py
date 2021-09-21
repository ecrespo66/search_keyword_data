import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sqlite3
from iRobot import robot, settings


class Keywords:
    def __init__(self, robotInstance):
        self.robot = robotInstance
        self.browser = robotInstance.browser
        self.search_data = []
        self.pages_data = []

    def store_data(self):
        df_search_data = pd.DataFrame(self.search_data)
        df_pages_data = pd.DataFrame(self.pages_data)

        conn = sqlite3.connect(settings.BD_PATH)
        df_search_data.to_sql('search_data', conn, if_exists='replace', index=True)
        df_pages_data.to_sql('pages_data', conn, if_exists='replace', index=True)

    def get_search_data(self, Qitem):
        keyword = Qitem.value['Keyword']
        self.browser.get("https://google.com")
        self.browser.waitFor("XPATH", "//button[@id='L2AGLb']", 10)
        try:
            self.browser.find_element_by_xpath("//button[@id='L2AGLb']").click()
        except:
            pass
        self.browser.waitFor("XPATH", "//input[@title='Buscar']")
        input = self.browser.find_element_by_xpath("//input[@title='Buscar']")
        input.click()
        input.send_keys(keyword)
        input.send_keys(Keys.ENTER)
        self.browser.waitFor("XPATH", "//span[@class='sc-bdnylx evNsMB']", seconds=20)
        if self.browser.element_exists("XPATH", "//*[text()='No results found']"):
            raise robot.BusinessException("No hay resultados", "next", Qitem)
        else:
            time.sleep(5)
            arrows = self.browser.find_elements_by_xpath("//span[@class='sc-bdnylx evNsMB']")
            arrows[0].click()
            time.sleep(1)
            dataTable = self.getDataTable()
            for element in dataTable:
                self.search_data.append(element)
                for k in self.search_data:
                    self.robot.Log.debug(k['keyword'])
                    if k['keyword'] != element['keyword']:
                        self.robot.queue.createItem(element['keyword'])
                        self.robot.queue

            while True:
                arrows = self.browser.find_elements_by_xpath("//span[@class='sc-bdnylx evNsMB']")
                if len(arrows) < 2:
                    break
                else:
                    arrows[-1].click()
                    time.sleep(2)
                    self.search_data.append(self.getDataTable())
            time.sleep(1)

    def getDataTable(self):
        data=[]
        keyword = self.browser.find_elements_by_xpath("//span[@class='sc-bdnylx hKziVK']/a").text
        similarity = self.browser.find_elements_by_xpath(
            "//td[@class='sc-iCoHVE sc-jrsJCI fzKnCn eoHezd']").text
        volume = self.browser.find_elements_by_xpath("//span[@class='sc-bdnylx fTWMJh']").text
        for k,s,v in zip(keyword, similarity, volume):
            data.append({"keyword": k, "similarity": s, "volume": v})
        return data


    def get_page_data(self):
        snippets = self.browser.find_elements_by_xpath("//div[@class='tF2Cxc']")
        for snippet in snippets:
            try:
                site = snippet.find_element_by_tag_name("a").get_attribute("href")
                stats = snippet.find_element_by_class_name("surfer-result-widget").text
                domain_traffic = stats.split("📖")[0].replace("🔎 ","")
                text_length = stats.split("📖")[1].split("🔑")[0].replace("📖 ","")
                keyword_number = stats.split("📖")[1].split("🔑")[1].replace("🔑 ","")
                self.pages_data.append({"site": site,
                                        "domain_traffic": int(domain_traffic.replace(",","")),
                                        "text_length": int(text_length.replace(",","")),
                                        "keyword_number": int(keyword_number.replace(",",""))})
            except:
                pass
