# Partie 1 :

import numpy as np 
import pandas as pd
df = pd.read_csv('https://drive.google.com/uc?export=download&id=1Uc-ZvLWaWY9Ua5Y5lEsP8FTOz9UarTcU' , index_col=0)
df = df.set_index('ID')
# print(df.head(10))
# print(df.dtypes)
# print(df.isna().sum())

#partie 2 :
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Age'] = df['Age'].astype(int)
df['Salary'] = df['Salary'].fillna(df.groupby('Department')['Salary'].transform('mean')).round(2)
def cate (anc) :
    if anc <= 3 :
        return 'Junior'
    elif 3 < anc < 7 :
        return 'Intermédiaire'
    elif 8 < anc < 15 :
        return 'Senior'
    elif anc >= 15 :
        return 'Expert'
        
df['Ancient_category'] = df['Years_Experience'].apply(cate)
#partie 3 :
global_salary_avg = df['Salary'].mean()
# print("global avg salary :",global_salary_avg)
max_employe_salary = df.loc[df['Salary'].idxmax()]
# print("max_employe_salary :",max_employe_salary['Name'])

avg_salary_per_dep = df.groupby('Department').agg(
    avg_salary = ('Salary' , 'mean')
).round(2)
# print('Avg salary per dep :\n' , avg_salary_per_dep)
avg_salary_per_anc = df.groupby('Ancient_category').agg(
    avg_salary = ('Salary' , 'mean'),
    med_salary = ('Salary' , 'median')
).round(2)
# print('avg salary per anc :\n' , avg_salary_per_anc)
remote_count = df[df['Remote'] == 'Yes'].groupby('Department').size()
# print('Remont count per dep : \n'  ,remote_count)
pivote_table_dep_rem = df.pivot_table(
    values='Salary',
    index='Department',
    columns='Remote',
    aggfunc='mean'
)
# print(pivote_table_dep_rem)
pivote_table_ann_age = df.pivot_table(
    values='Years_Experience',
    index='Department',
    columns='Ancient_category',
    aggfunc='mean'
).round(0).astype('Int64')
# print(pivote_table_ann_age)
df['Performance '] = np.where(df['Salary'] < 60000 ,'Bon' , np.where((df['Salary'] >=60000)  & (df['Salary'] < 80000) , 'Moyen' , 'Haut'))
seuil_age = 40
conditions = [
    (df['Age'] < seuil_age) & (df['Ancient_category'].isin(['Junior' , 'Intermédiaire'])),
    (df['Age'] < seuil_age) & (df['Ancient_category'].isin(['Expert' , 'Senior' ])),
    (df['Age'] >= seuil_age) & (df['Ancient_category'].isin(['Junior' , 'Intermédiaire'])),
    (df['Age'] >= seuil_age) & (df['Ancient_category'].isin(['Expert' , 'Senior' ]))
]
choix = [
    'Jeune & Nouveau',
    'Jeune & Expérimenté',
    'Senior & Nouveau',
    'Senior & Expérimenté'
]
df['Categorie'] = np.select(conditions, choix , default='non classe')

dif_sal_avg = df['Salary'] - df.groupby('Department')['Salary'].transform('mean').round(2)
print(dif_sal_avg)

