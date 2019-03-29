import matplotlib.pyplot as plt
import validation as val
import os
import shell as sh
import numpy as np

split = [1e-70, 1e-60, 1e-50, 1e-40, 1e-30, 1e-20, 1e-10, 1e-5, 1e-1, 1e0, 1e5, 1e10, 1e20, 1e30, 1e40, 1e50, 1e60, 1e70]
y = []
sh.boot_loader(sh.label_path, 0.8)

for prop in split:
    val.laplace = prop
    y.append(sh.validation('grading', ' '))
    print(prop)

split = np.log(split)
print(split)
plt.figure(figsize=(8, 4))
plt.plot(split, y, linewidth=1)
plt.show()