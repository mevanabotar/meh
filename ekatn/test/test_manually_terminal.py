
import unittest

import main

from . import encheiridion


class TestTerminalManually(unittest.TestCase):
 def test_manual(self):
  main.main(encheiridion.enchi)

if __name__ == "__main__":
 unittest.main()
