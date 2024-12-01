# if u forgot venv syntax (i did)
# python -m venv venv
#  venv\Scripts\activate

# run this  
# pip install -r 140dataDrop2/dependencies.txt


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#read csv
csvFile = "140dataDrop2/dataDrop.csv"
df = pd.read_csv(csvFile)

# 1. Data Profiling
print("\n=== Data Profiling ===")

# Get basic statistics for numeric columns
# df.describe() generates summary statistics for numeric columns including:
# count, mean, std, min, 25%, 50% (median), 75%, and max
numeric_stats = df.describe()
numeric_stats.loc['median'] = df.median(numeric_only=True)
print("\nNumeric Column Statistics:")
print(numeric_stats)

# Calculate null percentages for all columns
# if df target is null sum then divide by length and add two 0's to convert to percentage
null_percentages = (df.isnull().sum() / len(df)) * 100
print("\nNull Percentages for Each Column:")
print(null_percentages)

# 2. Measuring Completeness
print("\n Completeness check,  Row | Percentage")

# conv to datetime
df['DateRepConf'] = pd.to_datetime(df['DateRepConf'])

# month column
df['Month'] = df['DateRepConf'].dt.to_period('M')

# Everything below is just hard chatgpt'ed idk what this code does but from the way i understand it its: 
# lambda x let x be BarangayRes Row is not na and sum it then divide by length and multiply by 100 to turn into percentage
# lowkey i think i understood record completeness incorrectly so this code may need to be changed
# Then create a new column called Completeness and set it to the result of the lambda function
# Calculate completeness per month (non-null BarangayRes entries)
monthly_completeness = df.groupby('Month').apply(
    lambda x: (x['BarangayRes'].notna().sum() / len(x)) * 100
).reset_index()
monthly_completeness.columns = ['Month', 'Completeness']

# Convert Period to datetime for plotting
monthly_completeness['Month'] = monthly_completeness['Month'].astype(str).apply(lambda x: pd.to_datetime(x))

# Plot time series 
plt.figure(figsize=(10, 6))
plt.plot(monthly_completeness['Month'], monthly_completeness['Completeness'], marker='o')
plt.title('Record Completeness Over Time (BarangayRes)')
plt.xlabel('Month')
plt.ylabel('Completeness (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
