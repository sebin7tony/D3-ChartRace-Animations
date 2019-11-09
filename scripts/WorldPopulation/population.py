import numpy as np
import pandas as pd
import json

df = pd.read_csv("population_total.csv")
results = []
for i,row in df.iterrows():
    country = row['country']
    local_last_population = row['1800']
    for i in range(1800,2100):
        year = i
        population = row[str(i)]
        last_population = local_last_population
        local_last_population = population
        results.append(OrderedDict([("name" , country),
                                   ("value" , population),
                                   ("lastValue" , last_population),
                                   ("year" , year)]));
        
with open('ExpectedJsonFile.json', 'w') as outfile:
    outfile.write(json.dumps(results, indent=4))
