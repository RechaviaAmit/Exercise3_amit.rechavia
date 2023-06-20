import meals
import dishes
from flask import Flask
from flask_restful import Api
app = Flask(__name__)  # initialize Flask
api = Api(app)  # create API


api.add_resource(dishes.Dishes, '/dishes')
api.add_resource(dishes.DishName, '/dishes/<string:name>')
api.add_resource(dishes.DishID, '/dishes/<int:dish_id>')
api.add_resource(meals.Meals, '/meals/')
api.add_resource(meals.MealID, '/meals/<int:meal_id>')
api.add_resource(meals.MealName, '/meals/<string:name>')

if __name__ == '__main__':
    # create collection dictionary and keys list
    print("running food-api.py")
    # run Flask app.   default part is 5000
    app.run(host='0.0.0.0', port=8000, debug=False)