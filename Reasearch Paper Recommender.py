import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("./metadata2020.csv")

print("Starting cleaning...")
# Cleaning data
spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
              "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "–"]
for char in spec_chars:
    df['title'] = df['title'].str.replace(char, ' ')
    df['abstract'] = df['abstract'].str.replace(char, ' ')

df['title'] = df['title'].str.split().str.join(" ")
df['abstract'] = df['abstract'].str.split().str.join(" ")
df['authors'] = df['authors'].str.split().str.join(" ")
print("Clean complete...")


name = list(df["title"])
text = list(df["abstract"].values.astype('U'))
authors = list(df["authors"])

print(name[0])

# converting the text into matrix
vec = TfidfVectorizer()
text_arr = vec.fit_transform(text)

# create an object
md = NearestNeighbors(metric="cosine")

# fit the data
print("Synchronising...")
md.fit(text_arr)

buffer = {}
predicted = False
while True:
    reader = input(">> ")
    try:
        print(reader)
        if reader.isdigit() and predicted:
            reader = name[buffer[int(reader)]]
            buffer = {}

        if reader in name:
            try:
                print(reader)
                x = name.index(reader)
                reader_text = text[x]
                print("-" * 30)
                print(reader_text)
                print("Authors:", authors[x])
                print("-" * 30)
                reader_text_arr = vec.transform([reader_text])

                dist, ind = md.kneighbors(reader_text_arr, n_neighbors=6)
                print("Suggestions for you...")
                j = 1
                for i in ind[0][1:]:
                    predicted = True
                    print(j, "\b:", name[i])
                    buffer[j] = i
                    j += 1

            except Exception as e:
                print(">> 1:")

        else:
            print("Sorry Page ain't available...\nConsider checking spelling...")
    except Exception as e1:
        print(">> 0:")
