import requests
from collections import defaultdict
from typing import List, Union
import json


meals_times = ("appetizer", "main", "dessert")
meal_details = ("cal", "size", "sugar", "sodium")


class MainCollection:

    def __init__(self):
        self.id_for_dish = 0
        self.dishes = {}
        self.id_for_meal = 0
        self.meals = {}

    def get_dishes_details(self, dish_name) -> Union[List, int]:
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query={dish_name}"
        try:
            response = requests.get(api_url, headers={'X-Api-Key': 'MMkBzAjO/9Zan4bB0vs8hg==HRH4ztQNI3Enz90t'})
            if response.status_code == requests.codes.ok:
                return json.loads(response.text)
        except requests.exceptions.RequestException:
            return -4

    def get_dish_id_by_name(self, dish_name) -> Union[int, bool]:
        for dish in self.dishes.values():
            if dish["name"] == dish_name:
                return dish["ID"]
        return False

    def insert_valid_dish(self, dish_name, dish_details) -> int:
        required_details = {"cal": "calories", "size": "serving_size_g", "sugar": "sugar_g", "sodium": "sodium_mg"}
        self.id_for_dish += 1
        self.dishes[self.id_for_dish] = defaultdict(int)
        for dish in dish_details:
            for api_detail_key, response_api_detail_key in required_details.items():
                self.dishes[self.id_for_dish][api_detail_key] += dish[response_api_detail_key]
        self.dishes[self.id_for_dish] = dict(self.dishes[self.id_for_dish])
        self.dishes[self.id_for_dish]["ID"] = self.id_for_dish
        self.dishes[self.id_for_dish]["name"] = dish_name
        self.update_meals_details_after_dish_insertion(self.id_for_dish)
        return self.id_for_dish

    def insert_dish(self, dish_name) -> int:
        if self.get_dish_id_by_name(dish_name):
            print("DishesCollection: word ", dish_name, " already exists")
            return -2
        dish_details = self.get_dishes_details(dish_name)
        if dish_details == -4:
            print("api error")
            return -4
        if not dish_details:
            print("not recognized dish name")
            return -3
        return self.insert_valid_dish(dish_name, dish_details)

    def find_meal_id_by_dish_id(self, dish_id):
        for meal in self.meals.values():
            if dish_id in meal.values():
                return meal["ID"]
        return False

    def get_dishes_ids_by_meal_id(self, meal_id):
        return {self.meals[meal_id][meal_time] for meal_time in meals_times}

    def update_meals_details_after_dish_insertion(self, dish_id):
        if meal_id := self.find_meal_id_by_dish_id(dish_id):
            dishes_ids = self.get_dishes_ids_by_meal_id(meal_id)
            self.meals[meal_id].update(self.addition_details_by_dishes_ids(dishes_ids))

    def get_meal_id_by_name(self, meal_name) -> Union[int, bool]:
        for meal in self.meals.values():
            if meal["name"] == meal_name:
                return meal["ID"]
        return False

    def delete_dish_from_meals(self, dish_id):
        for meal in self.meals.values():
            for meal_time in meals_times:
                if meal[meal_time] == dish_id:
                    meal[meal_time] = None

    def addition_detail_by_ids(self, dishes_ids, detail):
        return sum(self.dishes[dish_id][detail] for dish_id in dishes_ids)

    def addition_details_by_dishes_ids(self, dishes_ids):
        return {detail: self.addition_detail_by_ids(dishes_ids, detail) for detail in meal_details}
    
    def meal_name_exists(self, meal_name):
        for meal in self.meals.values():
            if meal["name"] == meal_name:
                return True
        return False
    
    def meals_to_ids_exists_in_meal(self, meals_to_ids):
        for meal in self.meals.values():
            if meal["appetizer"] == meals_to_ids["appetizer"] and \
                    meal["main"] == meals_to_ids["main"] and \
                    meal["dessert"] == meals_to_ids["dessert"]:
                return True
        return False
    
    def meal_exists(self, meal_name, meals_to_ids):
        if self.meal_name_exists(meal_name) or self.meals_to_ids_exists_in_meal(meals_to_ids):
            return True
        return False
    
    def delete_meal(self, meal_id):
        key_to_delete = None
        for key_meal, meal in self.meals.items():
            if meal["ID"] == meal_id:
                key_to_delete = key_meal
                break
        if key_to_delete:
            self.meals.pop(key_to_delete)

    def insert_meal(self, meal_name, meals_to_ids, id_for_meal=None, change_meal=False):
        if not change_meal and self.meal_exists(meal_name, meals_to_ids):
            return -2
        if not set(meals_to_ids.values()).issubset(main_col.dishes.keys()):
            return -6
        if not id_for_meal:
            self.id_for_meal += 1
            id_for_meal = self.id_for_meal
        if change_meal:
            self.delete_meal(id_for_meal)
        self.meals[id_for_meal] = {"ID": id_for_meal, "name": meal_name} | \
                                       self.addition_details_by_dishes_ids(meals_to_ids.values()) | meals_to_ids
        return id_for_meal



main_col = MainCollection()