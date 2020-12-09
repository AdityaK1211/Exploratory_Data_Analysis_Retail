# -*- coding: utf-8 -*-
"""Exploratory_Data_Analysis_Retail.ipynb

Original file is located at
    https://colab.research.google.com/drive/1I1eXz9QL513CbRcndT1sVBCIKPhUxkF1

# Task 3 - Exploratory Data Analysis - Retail
## (Level - Beginner)

Author : Aditya K. Kataria
Data Science & Business Analytics Internship
GRIP December2020

Aim : Perform ‘Exploratory Data Analysis’ on dataset ‘SampleSuperstore’. As a business manager, try to find out the weak areas where you can work to
make more profit. 
Dataset : Data can be found at https://bit.ly/3i4rbWl

What all business problems you can derive by exploring the data?
"""

# Importing all the important Libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %matplotlib inline

# Loading Dataset
df = pd.read_csv('SampleSuperstore.csv')
print('Shape:', df.shape)

# Sample Dataset
print(df.head())

# Dataset Columns
print(df.columns)

# Check Missing and Null Values
print(df.isnull().sum())
print("Total number of null values =", df.isnull().sum().sum())

# Dataset Types
print(df.dtypes)

# Dataset Sumamry
print(df.info())

# Dataset Statistical Description
print(df.describe())

"""## Correlation Analysis
Pandas dataframe.corr() is used to find the pairwise correlation of all columns in the dataframe. Both NA and null values are automatically excluded. For any non-numeric data type columns in the dataframe it is ignored.
"""
# Correlation Analysis
corr_mat = df.corr()
print(corr_mat)

plt.figure(figsize=(7, 6))
sns.heatmap(corr_mat, annot=True)
plt.title('Correlation Analysis')
plt.savefig('correlation.png')
plt.show()

"""## Covariance
Pandas dataframe.cov() is used to compute the pairwise covariance among the series of a DataFrame. The returned data frame is the covariance matrix of the columns of the DataFrame.

Both NA and null values are automatically excluded from the calculation. A threshold can be set for the minimum number of observations for each value created. Comparisons with observations below this threshold will be returned as NaN.
"""
# Covariance Analysis
cov_mat = df.cov()
print(cov_mat)

fig, axes = plt.subplots(1, 1, figsize=(9, 6))
sns.heatmap(cov_mat, annot=True)
plt.title('Covariance')
plt.savefig('covariance.png')
plt.show()

# Unique items in attributes
print('Category:', df['Category'].unique())
print('Segment:', df['Segment'].unique())
print('Ship Mode:', df['Ship Mode'].unique())

sns.countplot(x=df['Category'])
plt.title('Category Unique Items')
plt.savefig('categoryUnique.png')

sns.countplot(x=df['Segment'])
plt.title('Segment Unique Items')
plt.savefig('segmentUnique.png')

sns.countplot(x=df['Ship Mode'])
plt.title('Ship Mode Unique Items')
plt.savefig('shipmodeUnique.png')

# Data Cleaning
# Checking null
print(df.isnull().sum())

# Removing Duplicates
print('Total Duplicates:', df.duplicated().sum())
df.drop_duplicates()

print(df['Country'].value_counts())

# Dropping Country column
df = df.drop('Country', axis=1)
print(df.head())

# Calculating Z-score
sorted_data = df.sort_values(by='Sales', ascending=False)
sorted_data['Z-Score'] = (sorted_data.Sales - sorted_data.Sales.mean()) / sorted_data.Sales.std()
print(sorted_data.head())

# Z-score Scatterplot
fig, ax = plt.subplots(figsize=(16, 8))
ax.scatter(sorted_data['Sales'], sorted_data['Z-Score'])
plt.title('Z-Score Scatterplot')
plt.savefig('zscore.png')
plt.show()

# Z-score threshold=3
sorted_data = sorted_data[sorted_data['Z-Score'] < 3]
print(sorted_data.head(10))

new_df = sorted_data
print(new_df.shape)

# Drop columns Z-score and Postal Code
new_df = new_df.drop(['Z-Score', 'Postal Code'], axis=1)

plt.figure(figsize=(16, 8))
sns.countplot(x='State', data=new_df, palette="rocket")
plt.xticks(rotation=90)
plt.title('State wise count')
plt.savefig('stateCount.png')
plt.show()

# Product Level Analysis
print(new_df['Category'].unique())

# Number of products in each category 
print(new_df['Category'].value_counts())

# Number of Sub-categories products are divided.
print('Number of Sub-categories products:', new_df['Sub-Category'].nunique())
# Number of products in each sub-category
print(new_df['Sub-Category'].value_counts())

# Sub-categories w.r.t. Categories
plt.figure(figsize=(16, 8))
sns.countplot(x=new_df['Sub-Category'], palette="rocket")
plt.title('Sub-category count')
plt.savefig('subCategoryCount.png')
plt.show()

plt.figure(figsize=(10, 10))
new_df['Sub-Category'].value_counts().plot.pie(autopct="%1.1f%%")
plt.title('Sub-category Pie-chart')
plt.savefig('subCategoryPiechart.png')
plt.show()

new_df.groupby('Sub-Category')[['Profit', 'Sales']].agg(['sum']).plot.bar()
plt.title('Total Profit and Sales per Sub-Category')
plt.savefig('profitSubCategory.png')
plt.show()

# Count of Sub-Category region wise
plt.figure(figsize=(16, 8))
sns.countplot(x="Sub-Category", hue="Region", data=new_df, palette="rocket")
plt.title('Count of Sub-Category Region wise in United States')
plt.savefig('subCategoryRegion-wise.png')
plt.show()

new_df['Cost'] = new_df['Sales'] - new_df['Profit']
new_df['Profit %'] = (new_df['Profit'] / new_df['Cost']) * 100
print(new_df[['City', 'State', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Cost', 'Profit %']].head())

figsize = (15, 10)
sns.pairplot(new_df, hue='Sub-Category')
plt.title('Sub-category Pairplot')
plt.savefig('subCategoryPairplot.png')

# Segment Level Analysis
print(new_df['Segment'].value_counts())

# Total Profit and Sales per Segment
new_df.groupby('Segment')[['Profit', 'Sales']].agg(['sum']).plot.bar()
plt.title('Total Profit and Sales per Segment')
plt.savefig('profitSegment.png')
plt.show()

# Count of Segment region wise
plt.figure(figsize=(16, 8))
sns.countplot(x="Segment", hue="Region", data=new_df, palette="rocket")
plt.title('Count of Segments Region wise in United States')
plt.savefig('segmentRegion-wise.png')
plt.show()

figsize = (15, 10)
sns.pairplot(new_df, hue='Segment')
plt.title('Segment Pairplot')
plt.savefig('segmentPairplot.png')

# Ship Mode Level Analysis
print(new_df['Ship Mode'].value_counts())

# Total Profit and Sales per Ship Mode
new_df.groupby('Ship Mode')[['Profit', 'Sales']].agg(['sum']).plot.bar()
plt.title('Total Profit and Sales per Ship Mode')
plt.savefig('profitShipMode.png')
plt.show()

figsize = (15, 10)
sns.pairplot(new_df, hue='Ship Mode')
plt.title('Ship Mode Pairplot')
plt.savefig('shipModePairplot.png')

# Relation between Ship Mode and Segment
plt.figure(figsize=(16, 8))
sns.catplot(x="Ship Mode", data=new_df, hue="Segment", kind="count", palette="rocket")
plt.title('Relation between Ship Mode and Segment')
plt.savefig('shipModeandSegment.png')
plt.show()

"""## Top 10 Profit and Sales Analysis"""
# Region wise Profit and Sales
data_top_10_region = new_df.groupby("Region")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                   ascending=False)
print(data_top_10_region.head())

# Top 10 State wise Profit and Sales
data_top_10_states = new_df.groupby("State")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                  ascending=False)
print(data_top_10_states.head(10))

# Top 10 City wise Profit and Sales
data_top_10_cities = new_df.groupby("City")[["Profit", "Sales"]].sum().reset_index().sort_values(by="Profit",
                                                                                                 ascending=False)
print(data_top_10_cities.head(10))

# Top 10 Sub-category wise Profit and Sales
data_top_10_sub_categories = new_df.groupby("Sub-Category")[["Profit", "Sales"]].sum().reset_index().sort_values(
    by="Profit", ascending=False)
print(data_top_10_sub_categories.head(10))
