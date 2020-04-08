from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get(
    "https://www.ewg.org/tapwater/search-results.php?stab=US&searchtype=largesys")
time.sleep(10)
container = driver.find_elements_by_xpath(
    "//ul[@class='list']/li[@class='option']")

stateAcro = []
for state in container:
    stateAcro.append(state.get_attribute("data-value"))

writeToFile = [
    "Utility name,Testing Description,City,State,People Served,Utility Name URL,Exceed Contaminant Count,Total Contaminants,Contaminants,Data Available,Source"
]

with open("data.csv", "w+") as obj:
    obj.write(writeToFile[0] + "\n")

for state in stateAcro:
    try:
        driver.get(
            "https://www.ewg.org/tapwater/search-results.php?stab={}&searchtype=largesys".format(state))
        time.sleep(1)

        waterLinks = []
        for x in driver.find_elements_by_xpath("//tbody/tr/td/a"):
            waterLinks.append(x.get_attribute("href"))

        for water in waterLinks:
            try:
                driver.get(water)
                time.sleep(1)

                try:
                    utility_name = driver.find_element_by_xpath("//main/h1").text.strip().replace(",", "%2C")
                except:
                    utility_name = "N/A"
                try:
                    testing_description = driver.find_element_by_xpath(
                    "//p[@class='systemtext']").text.strip().replace(",", "%2C")
                except:
                    testing_description = "N/A"
                try:
                    city = driver.find_elements_by_xpath(
                    "//ul[@class='served-ul']/li")[0].text.strip().split(",")[0].replace(",", "%2C")
                except:
                    city = "N/A"
                try:
                    state = driver.find_elements_by_xpath(
                    "//ul[@class='served-ul']/li")[0].text.strip().split(",")[1].replace(",", "%2C")
                except:
                    state = "N/A"
                try:
                    people_served = driver.find_elements_by_xpath(
                    "//ul[@class='served-ul']/li")[1].text.strip().split("ves: ")[1].replace(",", "")
                except:
                    people_served = "N/A"
                utility_name_url = water
                try:
                    exceed_contaminant_count = driver.find_element_by_xpath(
                    "//p[@class='contaminant-tile-number']").text.strip().replace(",", "%2C").replace(" ","")
                except:
                    exceed_contaminant_count = "N/A"
                try:
                    total_contaminant_count = driver.find_element_by_xpath("//p[@class='total-contaminants']").text.strip().replace(",", "%2C").split("Total ")[0]
                except:
                    total_contaminant_count = "N/A"
                
                contaminants = []
                try:
                    for x in driver.find_elements_by_xpath("//div[@class='contaminant-name']/h3"):
                        if x.text.strip() != "":
                            contaminants.append(x.text.strip().replace(",", "%2C"))
                except:
                    yeah = True


                driver.execute_script("scrollTo(798,1700);")
                time.sleep(1)
                try:
                    driver.find_element_by_id("contaminants-view-other").click()
                    time.sleep(0.3)

                    for x in driver.find_elements_by_xpath("//div[@class='contaminant-name']/h3"):
                        if x.text.strip() != "":
                            contaminants.append(x.text.strip().replace(",", "%2C"))

                    contams = ""
                    for x in range(0, len(contaminants)):
                        if x != len(contaminants)-1:
                            contams = contams + contaminants[x] + ";"
                        else:
                            contams = contams + contaminants[x]
                except:
                    contams = "N/A"
                try:
                    data_available = driver.find_elements_by_xpath(
                    "//ul[@class='served-ul']/li")[2].text.strip().split("lable: ")[1].replace(",", "%2C").replace("—", "-")
                except:
                    data_available = "N/A"
                try:
                    source = driver.find_elements_by_xpath(
                    "//ul[@class='served-ul']/li")[3].text.strip().split("rce: ")[1].replace(",", "%2C")
                except:
                    source = "N/A"

                writeToFile.append(
                    "{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        utility_name, testing_description, city, state, people_served, utility_name_url, exceed_contaminant_count, total_contaminant_count, contams, data_available, source
                    )
                )

                with open("data.csv", 'a') as output:
                    output.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        utility_name, testing_description, city, state, people_served, utility_name_url, exceed_contaminant_count, total_contaminant_count, contams, data_available, source
                    ))
            except:
                print("Skipped local")
    except:
        print("Skipped State")

driver.quit()