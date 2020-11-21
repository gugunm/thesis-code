# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

df = pd.DataFrame({'angles': [1, 7, 2],
                   'degrees': [7, 1, 6]},
                  index=['circle', 'triangle', 'rectangle'])

numpy_arr = df.to_numpy()

accumulator = 0
for i in numpy_arr:
    for j in i:
#        accumulator = np.multiply(accumulator, j)
        accumulator += np.log(j)
        print(accumulator)

print(accumulator)