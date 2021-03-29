# PROJEct: LEVEL BASED PERSONA DESCRIPTION, SIMPLE SEGMENTATION AND LEVEL BASED CLASSIFICATION

# Purpose of the Project:
# - Making level based persona description
# - Separating customer descriptions into segments using qcut function
# - Classification of a new customer based on the basic segmentation


# 1. Reading datasets and merge them by a common variable which is user id in our case

import pandas as pd
pd.set_option("display.float_format", lambda x: "%.2f" % x)

purchases = pd.read_csv("purchases.csv")
users = pd.read_csv("users.csv")
df = purchases.merge(users, how="inner", on="uid")

df.head()


# 2. What are the total revenue by country, device, gender, age variables ?

df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"})


# 3. Sorting variables based on price and defining a new dataframe

agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False)
agg_df.head()



# 4. Turning index names to variable names

agg_df.reset_index(inplace=True)
agg_df.head()

# 5. Turning variable age to a categorical variable and adding it to the data

agg_df["age_cat"] = pd.DataFrame(
    (pd.cut(agg_df["age"], [0, 18, 25, 40,agg_df["age"].max()], labels=["0_18", "19_25", "26_40", "40_"+str(agg_df["age"].max())])))

agg_df.head()


# 6. Defining new level based customers and addin to the data set

agg_df["customers_level_based"] = [row[0] + "_" + row[1].upper() + "_" + row[2] + "_" + row[5] for row in agg_df.values]
agg_df.index = agg_df["customers_level_based"]
agg_df.drop(["country", "device", "gender", "age_cat", "customers_level_based", "age"], axis=1, inplace=True)
agg_df.reset_index(inplace=True)
agg_df.head()

agg_df["customers_level_based"].count()
# Out[11]: 450
agg_df = agg_df.groupby("customers_level_based").agg({"price": "mean"})
agg_df.head()

agg_df = agg_df.reset_index()
agg_df["customers_level_based"].count()
# We have now 93 different persona defined.


# 7. Segmentation of new customers based on price - spending behaviour

agg_df["segment"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"])
agg_df.head()



# Description of price segmentation

segment_df = agg_df.groupby("segment").agg({"price": "mean"})
segment_df.head()

# 8. Let us find which price segment a woman from Turkey who are 42 years old and uses IOS belongs to

new_user = "TUR_IOS_F_40_75"

agg_df[agg_df["customers_level_based"] == new_user]


#     customers_level_based   price segment
# 72       TUR_IOS_F_40_90  1596.0       D
