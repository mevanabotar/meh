
import unittest

from memoization import Memo

class TestMemo(unittest.TestCase):
 def test_consolidation(self):

  tst = "En la hora de angustia y de luz vaga, en su Golem los ojos detenia. Quien nos diria lo que sentia Dios, al mirar a su rabino en Praga?"

  atst = Memo()
  atst.add_slice(0,5, tst[0:5])
  atst.add_slice(4, 10, tst[4:14])
  atst.add_slice(9,20, tst[9:29])
  atst.add_slice(30,10,tst[30:40])
  atst.add_slice(50,2,tst[50:52])
  atst.add_slice(30,5, tst[30:35])
  atst.add_slice(10,5, tst[10:15])
  atst.consolidate()
  self.assertEqual(atst.rangehash, {(0, 29): 'En la hora de angustia y de l', (30,10): 'z vaga, en', (50, 2): 'lo'})

if __name__ == "__main__":
 unittest.main()
