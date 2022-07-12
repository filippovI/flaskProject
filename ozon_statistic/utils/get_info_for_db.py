import requests as rq

from utils import config as cfg
from app import Items, db


class GetItemsForDB:
    def __init__(self):
        self.headers = cfg.headers
        self.url_get_items = cfg.url_get_items
        self.url_get_info = cfg.url_get_info
        self.items_product_id = []

    def __get_items_product_id(self):
        params_get_items = {
            "filter": {
                "offer_id": [
                ],
                "product_id": [
                ],
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 1000
        }

        result_get_items = rq.post(self.url_get_items, json=params_get_items, headers=self.headers).json()
        self.items_product_id = [i['product_id'] for i in result_get_items['result']['items']]

    def __get_info_and_write_db(self) -> str:
        for i in range(len(self.items_product_id)):
            params_get_info = {
                "offer_id": "",
                "product_id": self.items_product_id[i],
                "sku": 0
            }
            try:
                result_get_info: dict = rq.post(cfg.url_get_info, json=params_get_info, headers=cfg.headers).json()
                item = Items(product_id=result_get_info['result']['id'],
                             offer_id=result_get_info['result']['offer_id'],
                             name=result_get_info['result']['name'],
                             price=result_get_info['result']['price'],
                             image=result_get_info['result']['primary_image'],
                             state_name=result_get_info['result']['status']['state_name'])
                db.session.add(item)
            except(Exception,) as err:
                return f'Ошибка {err}'
        db.session.commit()

    def start(self):
        self.__get_items_product_id()
        self.__get_info_and_write_db()

