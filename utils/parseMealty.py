from bs4 import BeautifulSoup
import requests, random
from database import DB
from sqlalchemy import insert


if __name__ == '__main__':
    soup = BeautifulSoup(requests.get('https://www.mealty.ru/').text, 'lxml')

    names = soup.findAll('div', 'meal-card__name')
    desciptions = soup.findAll('div', 'meal-card__description')
    prices = [x for i, x in enumerate(soup.findAll('div', 'meal-card__price')) if i % 2 == 0]
    info = [[names[i].text, desciptions[i].text, int(prices[i].text)] for i in range(len(names))]
    
    db = DB('mysql', 'root', 'vlad', '127.0.0.1', '3306', 'IHW4')
    with db.engine.connect() as connection:
        connection.begin()

        arranged_info = []
        for i in range(len(info)):
            quantity = random.randint(0, 10)
            arranged_info.append({'name' : info[i][0],
                                  'description' : info[i][1],
                                  'price' : info[i][2],
                                  'quantity' : quantity,
                                  'is_available' : quantity != 0
                                 })

        connection.execute(insert(db.dishes), arranged_info)
        connection.commit()