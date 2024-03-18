import unittest
import main
import json

class TestMain(unittest.TestCase):
    def test_manhattan_distance(self):
        a = { "x": 0, "y": 0 }
        b = { "x": 1, "y": 1 }

        self.assertEqual(main.manhattan_distance(a,b), 2)
        self.assertEqual(main.manhattan_distance(b,a), 2)

    def test_food_distance(self):
        with open("responses\\test_one_food.json") as reader:
            game_state = json.load(reader)
            snake = game_state["you"]
            self.assertEqual(main.food_distance(snake, game_state), 1/2)

        with open("responses\\test_two_food.json") as reader:
            game_state = json.load(reader)
            snake = game_state["you"]
            self.assertEqual(main.food_distance(snake, game_state), 3/4)

    def test_eval_functions(self):
        with open('responses\\test_snake_eval_function.json') as reader:
            game_state = json.load(reader)
            me = game_state["you"]
            them = game_state["board"]["snakes"][0]

            self.assertEqual(main.snake_eval_function(me, game_state), 2.5)
            self.assertEqual(main.snake_eval_function(them, game_state), 2.5)
            self.assertEqual(main.eval_function(game_state), 0)

    def test_get_current_snake(self):
        with open("responses\\test_snake_eval_function.json") as reader:
            game_state = json.load(reader)
            snake = main.get_current_snake(game_state, True)
            self.assertEqual(snake["id"], "1e2a641d-9017-448d-b5b3-d92bacdc1cbb")
            
            snake = main.get_current_snake(game_state, False)
            self.assertEqual(snake["id"], "44bc903b-327a-4bbe-94cd-471821f37cbd")

    def test_process_move_eating_food(self):
        with open("responses\\test_process_move.json") as reader:
            game_state = json.load(reader)
            new_state = main.process_move(game_state, "up", True)

            our_snake = main.get_current_snake(new_state, True)
            self.assertEqual(len(new_state["board"]["food"]), 3)
            self.assertEqual(len(our_snake["body"]), 3)
            self.assertEqual(our_snake["head"], {"x": 10, "y": 7})
            self.assertEqual(our_snake["health"], 100)

    @unittest.skip("not implemented yet")
    def test_process_move_not_eating_food(self):
        self.assertTrue(True)

    def test_minimax(self):
        with open("responses\\test_process_move.json") as reader:
            game_state = json.load(reader)
            value, best_move = main.minimax(game_state, 2, True)
            self.assertEqual(best_move, "up")

if __name__ == '__main__':
    unittest.main()