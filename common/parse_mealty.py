import random

import requests
from bs4 import BeautifulSoup
from sqlalchemy import insert
from sqlalchemy.orm import Session

from common.db_manager import Model, DBManager


def parse_mealty(db_manager: DBManager, db: type[Model]):
    soup = BeautifulSoup(requests.get('https://www.mealty.ru/').text, 'lxml')

    names = soup.findAll('div', 'meal-card__name')
    descriptions = soup.findAll('div', 'meal-card__description')
    prices = [x for i, x in enumerate(soup.findAll('div', 'meal-card__price')) if i % 2 == 0]
    all_dishes_info = [[names[i].text, descriptions[i].text, int(prices[i].text)] for i in range(len(names))]

    with Session(db_manager.engine) as session:
        arranged_info = []
        for dish_info in all_dishes_info:
            quantity = random.randint(0, 10)
            arranged_info.append({**dict((*zip(['name', 'description', 'price'], dish_info),)), 'quantity': quantity})

        session.execute(insert(db), arranged_info)
        session.commit()
