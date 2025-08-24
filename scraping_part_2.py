from bs4 import BeautifulSoup
import pandas as pd
import re

movie_name=[]
movie_year=[]
movie_time=[]
movie_type=[]
movie_rating=[]
movie_description=[]
movie_director=[]
movie_stars=[]

def clean_text(tag):
    raw_text = tag.get_text(separator=' ', strip=True)
    return re.sub(r'\s+', ' ', raw_text)

def safe_append(target_list, value):
    target_list.append(value if value else "NA")

for i in range(1,251):
    print(i)
    try:
        with open(f"scrap/popup{i}.html","r",encoding="utf-8") as f:
            content=f.read()
        soup=BeautifulSoup(content,"lxml")
        name_tags = soup.find_all("h3", class_="ipc-title__text prompt-title-text ipc-title__text--reduced")
        for tag in name_tags:
            name= clean_text(tag)
        g_data=soup.find_all("ul",class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline baseAlt")
        for i in range(len(g_data)):
            if i==0:
                data=[j.get_text(strip=True) for j in g_data[i] if j.get_text(strip=True)!=""]
                year=data[0]
                time=data[1]
            else:
                type=[j.get_text(strip=True) for j in g_data[i] if j.get_text(strip=True)!=""]
                type=" ".join(type)
        rating=soup.find_all("span",class_="ipc-rating-star--rating")[0].get_text(strip=True)
        description=soup.find_all("div",class_="sc-f3a43855-2 dCytFm")[0].get_text(strip=True)
        d_data=soup.find_all("ul",class_="ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline baseAlt")
        for i in range(len(d_data)):
            if i==0:
                data=[j.get_text(separator=' ',strip=True) for j in d_data[i] if j.get_text(strip=True)!=""]
                director=re.sub(r'\s+', ' ', data[0])
            else:
                stars=[j.get_text(separator=' ',strip=True) for j in d_data[i] if j.get_text(strip=True)!=""]
                stars=" ".join(stars)
                stars=re.sub(r'\s+', ' ', stars)
    except Exception as e:
        pass
    
    safe_append(movie_name, name)
    safe_append(movie_year, year)
    safe_append(movie_time, time)
    safe_append(movie_type, type)
    safe_append(movie_rating, rating)
    safe_append(movie_description, description)
    safe_append(movie_director, director)
    safe_append(movie_stars, stars)


movie_dict = {
    "name": movie_name,
    "year": movie_year,
    "duration": movie_time,
    "genre": movie_type,
    "rating": movie_rating,
    "description": movie_description,
    "director": movie_director,
    "stars": movie_stars
}

df=pd.DataFrame(data=movie_dict)
print(df.shape)
df.to_csv("movie_data.csv",index=False)
