import numpy as np
import pandas as pd
import random

data = pd.read_csv(r"../../test_task1_latest.csv")
for n in range(data.shape[0]):
    row = data.ix[n]
    question = row["question"]
    paragraph = row["paragraph"] 
    print(question)







