import requests
from bs4 import BeautifulSoup
import json
import mysql.connector

# List of url for web scraping
list_of_url = ["https://www.amazon.de/dp/000108173X",
               "https://www.amazon.de/dp/000108142X",
               "https://www.amazon.fr/dp/000108173X",
               "https://www.amazon.fr/dp/000108142X",
               "https://www.amazon.fr/dp/000102163X",
               "https://www.amazon.de/dp/000102163X"]

HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

output_list = []

for url in list_of_url:
    page = requests.get(url, headers=HEADERS)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # Getting Product Title
    try:
        title = soup2.find(id='productTitle').get_text()
    except :
        title = None

    # Getting Price of the Product
    try:
        price = soup2.find("a",{'class':'a-size-mini a-link-normal'}).get_text()
    except :
        price = None

    # Getting Product Details    
    try:
        details = soup2.find(id='detailBullets_feature_div').get_text()
    except:
        try:
            details = soup2.find(id='productDescription').get_text()
        except:
            details = None

    # Getting Product Image URL
    try:
        img_url = soup2.find(id='imgBlkFront').get_attribute_list('src')
    except:
        img_url = None
    
    # Cleaning the Output
    title = title.strip()
    price = price.replace('\n','')
    price = price.strip()[15:]
    details = details.replace('\n','')
    
    # Adding data to Dictonary
    dic = {'Product Title':title, 'Product Image URL':img_url,'Price of the Product':price.replace('   ',''),'Product Details':details.replace('   ','')}
    output_list.append(dic)
    
# Dumbing data to JSON file
json_object = json.dumps(output_list, indent=4)
with open("sample.json", "w") as outfile:
        outfile.write(json_object)


# Storing data in databases Mysql
mydb = mysql.connector.connect(user='root', password='Patil',host='127.0.0.1',database='demo',)
mycursor = mydb.cursor()

try :
    for mydict in output_list:
        placeholders = ', '.join(['%s'] * len(mydict))
        values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in mydict.values())
        sql = "INSERT INTO internship_task (Product_Title,Product_Image_URL,Price_of_the_Product,Product_Details ) VALUES ( %s );" % (values)
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "was inserted.")
except:
    print("Unable to store value in database")
