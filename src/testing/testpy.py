import os
import pandas as pd

DATA_LAT_LON_URL = (r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\data\Cluster-GeoData.csv')
DATA_URL_NEW = (r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\data\JLT_CatLogs.xlsx')
# Banner


def load_data():
    data_cat_details = pd.read_excel(DATA_URL_NEW)
    data_cluster_geo = pd.read_csv(DATA_LAT_LON_URL)
    data_cat_details['NAME'].fillna('No_Name_Yet', inplace=True)
    data_cat_details['USUAL SPOT'] = data_cat_details['USUAL SPOT'].str.split(' ').str[1]
    return data_cat_details


cat_details = load_data()

print(cat_details['NAME'])
print(os.getcwd())

os.chdir(r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\asset\img\cluster-wise-photos')
print(os.getcwd())
for i, row in cat_details.iterrows():
    #print(row['USUAL SPOT'])
    if not os.path.exists(row['USUAL SPOT']):
        os.mkdir(row['USUAL SPOT'])
        print(row['USUAL SPOT'])
    path_dir = r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\asset\img\cats'
    cluster_dir= os.path.join(r'C:\Users\Sudhendu-BCT\Python_Practice\Pycharm_Projects\jlt-cats\asset\img\cluster-wise-photos',row['USUAL SPOT'])
    if os.path.exists(os.path.join(path_dir, row['NAME'])+'.jpg'):
        os.rename(os.path.join(path_dir, row['NAME'])+'.jpg' , os.path.join(cluster_dir, row['NAME']) + '.jpg')

