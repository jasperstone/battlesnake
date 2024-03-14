import unittest
from tree import node

class Testnode(unittest.TestCase):
    def test_output(self):
        root = node('grandmother')
        root.children = [node('daughter'), node('son')]
        root.children[0].children = [node('granddaughter'), node('grandson')]
        root.children[1].children = [node('granddaughter'), node('grandson')]

        print(root)

if __name__ == '__main__':
    unittest.main()

