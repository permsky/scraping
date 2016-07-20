import glob
import os 
import pandas 
import requests 
import shutil 
import wget 
from bs4 import BeautifulSoup


url = 'http://www.nemweb.com.au/REPORTS/ARCHIVE/Dispatch_SCADA/'
response = requests.get(url) soup = BeautifulSoup(response.text, 'html.parser')
links_list = []
for link in soup.find_all('a'):
    links_list.append(link.get('href'))
archives_list = []
for link in links_list[1:]:
    archives_list.append(link[-33:])
for archive in archives_list[0:3]:
    wget.download(url+archive)
    try:
        shutil.unpack_archive(archive, extract_dir=archive[:-4])
        root_dir = os.getcwd()
        zip_list = os.listdir(root_dir + '\\' + archive[:-4])
        os.chdir(path=archive[:-4])
        for filename in zip_list:
            shutil.unpack_archive(filename)
            os.remove(filename)
            os.chdir(root_dir)
        except Exception:
            print ("File is not a zip file")
del response

def concatenate(indir='PUBLIC_DISPATCHSCADA_20150223', outfile='PUBLIC_DISPATCHSCADA_20150223.csv'):
    os.chdir(indir)
    filelist = glob.glob('*.csv')
    dataframe_list = []
    column_list = ['I', 'DISPATCH', 'UNIT_SCADA', '1', 'SETTLEMENTDATE', 'DUID', 'SCADAVALUE']
    for file in filelist:
        print(file) 
        dataframe = pandas.read_csv(file, header=None, engine='python', names=column_list, skiprows=2, skipfooter=1)
        dataframe_list.append(dataframe)
        result_dataframe = pandas.concat(dataframe_list, axis=0)
        result_dataframe.columns = column_list
        result_dataframe.to_csv(outfile, index=None)

concatenate()
print('Task done!')
