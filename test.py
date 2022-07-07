import pandas as pd
df = pd.read_csv("./static/data/review_form.csv", header=None, names=["review"])
print(df["review"].sample(40))
index = (df["review"].sample(40).index[0])
print(df["review"][1])