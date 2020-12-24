import pandas as pd
import re

def findRes(X, name):
    li = []
    for sen in X:
        results = re.findall(r'[^,.]*{}[^,.]*[,.]'.format(name), sen)
        if len(results) > 0:
            results = " ".join(results)
            li.append(results)
    
    return li

dat = pd.read_csv('hair_dryer.tsv', sep='\t', header=0)
target = dat['review_body']

res = findRes(target,'cord')
