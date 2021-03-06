import json
from pprint import pprint
import jsonlines
import numpy as np


def classify_entail_cnfd(logits_a, logits_b):
    return np.sign(logits_a[:, 0] - logits_b[:, 0])

def classify_contra_cnfd(logits_a, logits_b):
    return np.sign(logits_b[:, 2] - logits_a[:, 2])

logits = np.empty(3)
pairIDs = []
gl = []

directory = '../confidence_levels_winograd_devset.jsonl'
with jsonlines.open(directory) as reader:
    for obj in reader:
        logit = np.array([obj['entailment_confidence'], obj['neutral_confidence'], obj['contradiction_confidence']])
        logits = np.vstack([logits, logit])
        pairID = obj['pairID']
        pairIDs.append(pairID)
        gold_label = obj['gold_label']
        if (gold_label == "entailment"):
            gl.append(1)
        elif (gold_label == "neutral"):
            gl.append(-1)
        else:
            print ("bad label!")

logits = logits[1:, :]

gl_arr = np.array(gl)
labels = gl_arr[np.arange(0, len(gl), 2)]
logits_a = logits[np.arange(0, len(gl), 2)]
logits_b = logits[np.arange(1, len(gl), 2)]

preds_1 = classify_entail_cnfd(logits_a, logits_b)
preds_2 = classify_contra_cnfd(logits_a, logits_b)
acc_1 = np.mean((1 + labels * preds_1)/2)
acc_2 = np.mean((1 + labels * preds_2)/2)

print ('Accuracy achieved by classifying only based on entailment confidence + ' + str(acc_1))
print ('Accuracy achieved by classifying only based on contradiction confidence + ' + str(acc_2))


