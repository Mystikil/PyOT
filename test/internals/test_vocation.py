import unittest
import importlib

from game import vocation

class TestVocationRegistration(unittest.TestCase):
    def setUp(self):
        vocation._vocations_by_id.clear()
        vocation._vocations_by_name.clear()
        vocation._vocations_by_cid.clear()

    def test_reg_and_lookup(self):
        voc = vocation.regVocation(99, 99, "Tester", "Test voc", 100, 50, 200)
        self.assertIs(vocation.getVocation("Tester"), voc)
        self.assertIs(vocation.getVocationById(99), voc)

if __name__ == "__main__":
    unittest.main()
