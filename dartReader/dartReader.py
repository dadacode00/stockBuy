import requests
import os
import zipfile
import pandas as pd
from bs4 import BeautifulSoup


class DnCorpCode():
    def __init__(self):
        self.crtfc_key = '40aa53cf246254eedfb269ac614c24fe7105329b'
        self.apiurl = 'https://opendart.fss.or.kr/api/corpCode.xml'
        self.zipFileName = 'CORPCODE.zip'
        self.xmlFileName = 'CORPCODE.xml'
        self.binFileName = 'CORPCODE.bin'

    def reqCorpCode(self):
        apiurl = 'https://opendart.fss.or.kr/api/corpCode.xml'
        param_corpcode = {
            'crtfc_key': self.crtfc_key
        }
        data = requests.get(apiurl, params=param_corpcode)
        print(data)
        with open(self.zipFileName, 'wb') as f:
            f.write(data.content)
        zip = zipfile.ZipFile(self.zipFileName)
        zip.extractall()
        zip.close()
        os.remove(self.zipFileName)
        print('file download complete')

    def corpCodeDataFrame(self):
        dirlist = os.listdir()
        if self.xmlFileName in dirlist:
            with open(self.xmlFileName, 'r', encoding='utf8') as f:
                datas = BeautifulSoup(f, 'lxml')

            print('xml file 확인. 변환 중')
            corplists = datas.find_all('list')
            datalist = list()
            for i in corplists:
                datalist.append({
                    'corp_code': i.corp_code.text,
                    'corp_name': i.corp_name.text,
                    'stock_code': i.stock_code.text,
                    'modify_date': i.modify_date.text,
                })
            setlist = pd.DataFrame(datalist)
            stocklist = setlist[setlist['stock_code'] != chr(32)]
            stocklist.to_pickle(self.binFileName)
            print('DataFrame bin file 생성')
        else:
            self.reqCorpCode()
            print(f'{self.xmlFileName} 이 없습니다.')
            self.corpCodeDataFrame()

    def searchCorpCode(self, corpName):
        if not os.path.exists(self.binFileName):
            print('Data file이 없습니다.')
            try:
                self.corpCodeDataFrame()
            except:
                print('API Data Download Error')
        else:
            with open(self.binFileName, 'rb') as f:
                corpDataFrame = pd.read_pickle(f)
            searchResult = corpDataFrame[corpDataFrame['corp_name'] == corpName]
            print(searchResult['corp_name'].values)
            print(searchResult['corp_code'])
            print(searchResult['stock_code'])


if __name__ == '__main__':
    test = DnCorpCode()
    test.searchCorpCode('한국전력공사')
