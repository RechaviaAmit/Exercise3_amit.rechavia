from werkzeug.exceptions import BadRequest
from flask_restful import Resource, reqparse
from api_collections.main_collection import main_col


class Dishes(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        try:
            args = parser.parse_args()
        except BadRequest:
            print("content-type must be application/json")
            return 0, 415
        dish_name = args['name']
        if not dish_name:
            print("Dishes: no name provided")
            return -1, 422
        key = main_col.insert_dish(dish_name)
        if key in [-2, -3]:
            return key, 422
        elif key == -4:
            return key, 504
        return key, 201

    def get(self):
        return main_col.dishes, 200


class DishID(Resource):

    def get(self, dish_id):
        if dish_id in main_col.dishes.keys():
            return main_col.dishes[dish_id], 200
        return -5, 404

    def delete(self, dish_id):
        if dish_id in main_col.dishes.keys():
            main_col.dishes.pop(dish_id)
            main_col.delete_dish_from_meals(dish_id)
            return dish_id, 200
        return -5, 404


class DishName(Resource):

    def get(self, name):
        if dish_id := main_col.get_dish_id_by_name(name):
            return main_col.dishes[dish_id], 200
        return -5, 404

    def delete(self, name):
        if dish_id := main_col.get_dish_id_by_name(name):
            main_col.dishes.pop(dish_id)
            main_col.delete_dish_from_meals(dish_id)
            return dish_id, 200
        return -5, 404