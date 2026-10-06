import unittest
from bt_history.data_control import core_hour_limit
class Tests(unittest.TestCase):
 def test_removal_requires_explicit_flag_and_reference(self):
  b={'max_total_core_hours':None,'stages':{'train':{'max_reserved_core_hours':None}}}
  with self.assertRaises(PermissionError):core_hour_limit(b)
  b.update(core_hour_limit_removed=True,core_hour_limit_removal_approval='user_explicit')
  self.assertEqual(core_hour_limit(b),float('inf'));self.assertEqual(core_hour_limit(b,'train'),float('inf'))
 def test_old_caps_preserved(self):
  b={'max_total_core_hours':2000,'stages':{'train':{'max_reserved_core_hours':2000}}};self.assertEqual(core_hour_limit(b),2000);self.assertEqual(core_hour_limit(b,'train'),2000)
