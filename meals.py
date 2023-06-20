from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse
from api_collections.main_collection import main_col

meal_details = ("cal", "size", "sugar", "sodium")
meals_times = ("appetizer", "main", "dessert")


class Meals(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('appetizer', location='json', type=int)
        parser.add_argument('main', location='json', type=int)
        parser.add_argument('dessert', location='json', type=int)
        try:
            args = parser.parse_args()
        except BadRequest:
            print("content-type must be application/json")
            return 0, 415
        meals_to_ids = {'appetizer': args['appetizer'], 'main': args['main'], 'dessert': args['dessert']}
        meals_name = args['name']
        if not all(meals_to_ids.values()) or not meals_name:
            print("Meals: no name/id's provided")
            return -1, 422
        key = main_col.insert_meal(meals_name, meals_to_ids)
        if key in [-2, -6]:
            return key, 422
        return key, 201


    def get(self):
        return main_col.meals


class MealID(Resource):

    def get(self, meal_id):
        if meal_id in main_col.meals.keys():
            return main_col.meals[meal_id], 200
        return -5, 404

    def delete(self, meal_id):
        if meal_id in main_col.meals.keys():
            main_col.meals.pop(meal_id)
            return meal_id, 200
        return -5, 404

    def put(self, meal_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('appetizer', location='json', type=int)
        parser.add_argument('main', location='json', type=int)
        parser.add_argument('dessert', location='json', type=int)
        args = parser.parse_args()
        meals_to_ids = {'appetizer': args['appetizer'], 'main': args['main'], 'dessert': args['dessert']}
        meals_name = args['name']
        main_col.insert_meal(meals_name, meals_to_ids, meal_id, True)
        return meal_id, 200


class MealName(Resource):

    def get(self, name):
        if meal_id := main_col.get_meal_id_by_name(name):
            return main_col.meals[meal_id], 200
        return -5, 404

    def delete(self, name):
        if meal_id := main_col.get_meal_id_by_name(name):
            main_col.meals.pop(meal_id)
            return meal_id, 200
        return -5, 404
