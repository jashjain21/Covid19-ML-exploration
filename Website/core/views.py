from django.shortcuts import render
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import os


def index(request):
    return render(request, 'base.html')


def search(request):
    if request.method == "POST":
        search_input = request.POST["search"]
        print(search_input)
        research_papers = []

        df = pd.read_csv(os.path.join("metadata2020.csv"))

        # Cleaning data
        spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
                      "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~", "–"]
        for char in spec_chars:
            df['title'] = df['title'].str.replace(char, ' ')
            df['abstract'] = df['abstract'].str.replace(char, ' ')

        df['title'] = df['title'].str.split().str.join(" ")
        df['abstract'] = df['abstract'].str.split().str.join(" ")
        df['authors'] = df['authors'].str.split().str.join(" ")

        name = list(df["title"])
        text = list(df["abstract"].values.astype('U'))
        authors = list(df["authors"])

        with open("research_paper_vec.pkl", "rb") as f:
            vec = pickle.load(f)

        text_arr = vec.transform(text)

        # create an object
        md = NearestNeighbors(metric="cosine")

        # fit the data
        md.fit(text_arr)

        if search_input in name:
            try:
                print("Init", search_input)
                x = name.index(search_input)
                search_input_text = text[x]
                # print("-" * 30)
                # print(search_input_text)
                # print("Authors:", authors[x])
                # print("-" * 30)
                search_input_text_arr = vec.transform([search_input_text])

                dist, ind = md.kneighbors(search_input_text_arr, n_neighbors=6)

                for i in ind[0][1:]:
                    # print(name[i])
                    research_papers.append(name[i])

            except:
                print("Exception")

        else:
            print("Sorry Page ain't available...\nConsider checking spelling...")

        # print(research_papers)

        return render(request, "search.html", {"research_papers": research_papers})
    return render(request, "search.html")
