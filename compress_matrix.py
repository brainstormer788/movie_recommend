import pickle
import gzip
import numpy as np

print("Loading similarity matrix...")
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

print("Converting to float32...")
similarity = similarity.astype(np.float32)

print("Saving compressed version...")
with gzip.open("similarity.pkl.gz", "wb", compresslevel=9) as f:
    pickle.dump(similarity, f)

print("Done! You can now remove the original similarity.pkl file")
