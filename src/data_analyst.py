#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sqlalchemy as db
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# import data from MySQL database to Python
engine = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306/scraped_data")
connection = engine.connect()
query = "SELECT title, brand, total_price, rating, num_ratings FROM graphic_cards"
data_raw = pd.read_sql_query(query, engine)
data = data_raw.copy()
data = data.replace("NULL", np.nan).dropna()

# Find the number of products by each brand
top_brand = data.brand.value_counts()[:10]
names = []
for x, y in top_brand.items():
    names.append(x)
data_brand = data.loc[data.brand.isin(names)]
fig, ax = plt.subplots(figsize = (20, 8))
ax.hist(data_brand.brand,
        bins = 10,
        facecolor = "g",
        edgecolor = "lightgrey")
ax.set_ylabel("Number of card products")
ax.set_title("Card product distribution by brand")

# Find price distribution by products
data_price = data.copy()
data_price.total_price = data_price.total_price.replace(0, np.nan)
data_price = data_price.dropna()
data_price = data_price[data_price.total_price < 2000] # remove clusters
fig, ax = plt.subplots(figsize = (16, 8))
ax.hist(data_price.total_price,
        bins = 20,
        facecolor = "g",
        edgecolor = "lightgrey")

ax.set_xticks(range(100, 2001, 100))
ax.set_yticks(range(100, 401, 100))
ax.set_xlabel("Product price")
ax.set_ylabel("Number of products")
ax.set_title("Price Distribution by Product")

ax.annotate("Most common prices",
            xy = (280, 295),
            xytext = (250, 370),
            arrowprops = dict(facecolor = "red", shrink = 5))
ax.annotate("Most common prices",
            xy = (480, 320),
            xytext = (250, 370),
            arrowprops = dict(facecolor = "red", shrink = 5))

# Find price distribution by brand
price_dis_brand = data_brand[(data_brand.total_price > 0) & (data_brand.total_price < 2000)] #remove clusters 
price_dis_brand = price_dis_brand.sort_values(by = "total_price")
fig, ax = plt.subplots(figsize = (16, 8))
sns.violinplot(x='brand', y='total_price', data=price_dis_brand)
ax.set_ylabel("Price ranges")
ax.set_title("Price Distribution by Brand")

# Find the correlation between price and consumer's rating
fig, ax = plt.subplots()
data_price = data_price[data_price.rating > 0]

ax.scatter(data_price["total_price"],
           data_price["rating"],
           facecolor = "g")
ax.set_xlabel("Price")
ax.set_ylabel("Rating")
ax.set_title("Correlation between Price and Consumer's Rating")