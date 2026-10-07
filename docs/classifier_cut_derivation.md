# 5-sigma classifier boundary

The frozen original neutral-fraction likelihood has zero penalty below xHI=0.06 and `-0.5*((xHI-0.06)/0.05)**2` above it, with model_error=0. Thus the 5-sigma observational exclusion boundary is **0.06 + 5*0.05 = 0.31**, giving delta logL=-12.5 at equality. Quantity: simulator-defined volume-average global_xHI, evaluated with the original interpolant at z=5.9.

All exact histories remain stored. Allowed/positive is xHI<0.31; equality is negative. This label is not a new prior and does not authorize replacing a finite likelihood by minus infinity. Classifier probability threshold, false-negative policy, and hard-gate semantics remain to be validated. NNERO Xe and this volume-mean xHI are distinct quantities.

Source SHA256: `e60f43ea70bc1fc5d274c7645b9a0928c41f3785d3be0546e8f1cc18af4145fa`.
