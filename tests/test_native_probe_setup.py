import ast,unittest
from pathlib import Path
from types import SimpleNamespace

class NativeProbeSetupTests(unittest.TestCase):
 def test_both_native_global_pointer_sets_initialized_with_retained_structs(self):
  script=Path(__file__).resolve().parents[1]/'scripts/native_power_probe.py'
  tree=ast.parse(script.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='initialize_power_structs')
  ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(script),'exec'),ns)
  calls=[];u=object();c=object();native=SimpleNamespace(lib=SimpleNamespace(Broadcast_struct_global_PS=lambda a,b:calls.append(('PS',a,b)),Broadcast_struct_global_UF=lambda a,b:calls.append(('UF',a,b))))
  retained=ns['initialize_power_structs'](native,lambda:u,lambda:c)
  self.assertEqual(calls,[('PS',u,c),('UF',u,c)]);self.assertIs(retained[0],u);self.assertIs(retained[1],c)
