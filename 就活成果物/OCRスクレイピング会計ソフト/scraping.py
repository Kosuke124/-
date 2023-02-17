import pandas as pd
import time
import numpy as np
import re
import datetime as dt
import decimal
from decimal import Decimal,ROUND_HALF_UP,ROUND_FLOOR

url_lists=[]
df_lists=[]
df_lists=["df_1","df_2","df_3","df_4"]
url_lists=["https://db.netkeiba.com/?pid=trainer_detail&id=01148&page=1","https://db.netkeiba.com/?pid=trainer_detail&id=01148&page=2","https://db.netkeiba.com/?pid=trainer_detail&id=01148&page=3"]

for i in range(3):
    dfs = pd.read_html(url_lists[i])
    time.sleep(1)
    df_lists[i] = dfs[0]
    df_lists[i] = df_lists[i].drop(columns=['天気','映像','頭数','枠番','馬番','単勝','人気','騎手','斤量','馬場','タイム','着差','通過','ペース','上り','馬体重','勝ち馬'],axis=1)

df_lists[3] = pd.concat([df_lists[0],df_lists[1],df_lists[2]],ignore_index=True)

df=df_lists[3]

df['コース']=['ダート' if 'ダ' in df['距離'][i] else '芝' for i in range(len(df['距離']))]
df['距離']=df['距離'].str[1:]
dfi=df['開催']
df['開催回数']=dfi.str[0]
dfk=df['開催回数']
df['開催回数']=[dfk[i] if dfk[i].isdecimal() else np.nan for i in range(len(dfi))]
df['開催']=dfi.str[1:3]
df['開催']=['帯広' if len(dfi[i])==1 and '広' in dfi[i] else '門別' if '別' in dfi[i] else '盛岡' if '岡' in dfi[i] else '水沢' if '沢' in dfi[i] else '浦和' if '和' in dfi[i] else '船橋' if '橋' in dfi[i] else '大井' if '井' in dfi[i] else '川崎' if '崎' in dfi[i] else '金沢' if '沢' in dfi[i] else '笠松' if '松' in dfi[i] else '名古屋' if '古' in dfi[i] else '姫路' if '路' in dfi[i] else '園田' if '田' in dfi[i] else '高知' if '知' in dfi[i] else '佐賀' if '賀' in dfi[i] else dfi[i] for i in range(len(dfi))]
dfr = df['レース名']
df["グレード"]=["未勝利" if '未勝' in dfr[i] else '2勝クラス' if '2勝' in dfr[i] else '新馬' if '新馬' in dfr[i] else 'G3' if 'G3' in dfr[i] else 'G2' if 'G2' in dfr[i] else 'G1' if 'G1' in dfr[i] else 'オープン' if 'OP' in dfr[i] else "1勝クラス" if '1勝' in dfr[i] else "3勝クラス" if '3勝' in dfr[i] else "リステッド" for i in range(len(df['レース名']))]
df["競争条件"]=['一般' if '以上' in dfr[i] else '一般' if '新馬' in dfr[i] else '一般' if '未勝利' in dfr[i] else "特別" for i in range(len(df['レース名']))]
df['管轄']=['中央' if '札幌' in dfi[i] or '函館' in dfi[i] or '福島' in dfi[i] or '中山' in dfi[i] or '東京' in dfi[i] or '新潟' in dfi[i] or '中京' in dfi[i] or '京都' in dfi[i] or '阪神' in dfi[i] or '小倉' in dfi[i] else '地方' for i in range(len(dfr))]
df['開催回数']=df['開催回数'].astype(float)
df['距離']=df['距離'].astype(int)
df['日付']=pd.to_datetime(df['日付'])
dfd=df['日付']
df['季節']=['春季' if dfd[i] >= dt.datetime(2021,1,1) and dfd[i] < dt.datetime(2021,5,31) else '夏季' for i in range(len(dfd))]
df['日付']=df['日付'].replace('-','/')
df['平or障']=['障害' if '障害' in dfr[i] else '障害' if 'J.G2' in dfr[i] else '障害' if 'J.G3' in dfr[i] else '障害' if 'J.G1' in dfr[i] else '平地' for i in range(len(dfr))]
df_race=df.reindex(columns=['日付','季節','管轄','開催','開催回数','R','レース名','着順','グレード','競争条件','馬名','馬齢','性別','産地','クラス','距離','コース','平or障','賞金(万円)','本賞金','賞金','出走奨励','内国産','距離別'])


import requests
from bs4 import BeautifulSoup

url = ["https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=1","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=2","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=3","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=4","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=5","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=6","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=7","https://umanity.jp/racedata/database_trainer_2.php?code=01148&mode=0&page=8"]

df = pd.DataFrame()
for i in range(len(url)):
    time.sleep(3)
    page = requests.get(url[i])

    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.findAll("table")[11]

    rows = table.find_all('tr')
    columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]

    dfs = pd.DataFrame(columns=columns)

    for i in range(len(rows)):
        tds = rows[i].find_all('td')

        if len(tds) == len(columns):
            values = [ td.text.replace('\n', '').replace('\xa0', ' ') for td in tds ]
            dfs = dfs.append(pd.Series(values, index=columns), ignore_index= True)
    
    df=df.append(dfs,ignore_index=True)
    
dfh=df['馬齢']
dfn=df['母']

df['馬齢']=[dfh[i].replace('歳','') for i in range(len(dfh))]
df['馬齢']=[dfh[i].replace('年産','') for i in range(len(dfh))]
df['馬齢']=df['馬齢'].astype(int)
date = dt.date.today()
df['馬齢']=[(date.year)-df['馬齢'][i] if df['馬齢'][i]>=1000 else dfh[i] for i in range(len(dfh))]
df['馬齢']=df['馬齢'].astype(int)
df_horses=df.drop(columns=['毛色','戦績','父','母父','母'],axis=1)
df['母']=[dfn[i].replace('...','') if '...' in dfn[i] else dfn[i] for i in range(len(dfn))]
df['産地']= ['外国' if dfn[i].isascii() else '内国' for i in range(len(dfh))]
df['総賞金']=[df['総賞金'][i].replace('万','') for i in range(len(dfh))]
df['戦績']=[df['戦績'][i].replace(' ','') for i in range(len(dfh))]
df['戦績']=[df['戦績'][i].split('[') for i in range(len(dfh))]
df['戦績']=[df['戦績'][i][1].split('-') for i in range(len(dfh))]
df['戦績']=[df['戦績'][i][0] for i in range(len(dfh))]
df['戦績']=df['戦績'].astype(int)
df['馬クラス']=['オープン' if df['戦績'][i]>=4 else '3勝クラス' if df['戦績'][i]==3 else '2勝クラス' if df['戦績'][i]==2 else '1勝クラス' if df['戦績'][i]==1 else '未勝利' for i in range(len(dfh))]
df_horses=df.reindex(columns=['馬名','馬齢','性別','産地','戦績','馬クラス'])

for i in range(len(dfr)):
    for j in range(len(dfh)):
        if df_race['馬名'][i] == df_horses['馬名'][j]:
            df_race.loc[[i],"馬齢"]=df_horses["馬齢"][j]
            df_race.loc[[i],"性別"]=df_horses["性別"][j]
            df_race.loc[[i],"産地"]=df_horses["産地"][j]
            df_race.loc[[i],"クラス"]=df_horses["馬クラス"][j]
        else:
            pass



a = pd.read_excel(r"C:\Users\kyomu\OneDrive\デスクトップ\g_race.xlsx",index_col=0)
a['1着賞金(万円)']=a['1着賞金(万円)'].astype(float)

df_g1=a.query("レース名.str.contains('G1')",engine='python')
df_g2=a.query("レース名.str.contains('G2')",engine='python')
df_g3=a.query("レース名.str.contains('G3')",engine='python')
df_g2=pd.concat([df_g2,df_g3])
df_g2=df_g2.reset_index(drop=True)

dfj=[['阪神スプリングJ(J.G2)',4100],['京都ハイジャンプ(J.G2)',4100],['東京ジャンプS(J.G3)',2900],['新潟ジャンプS(J.G3)',2900],['小倉サマージャンプ(J.G3)',2900],['阪神ジャンプS(J.G3)',2900],['東京ハイジャンプ(J.G2)',4100],['京都ジャンプS(J.G3)',2900]]
columns=['レース名','1着賞金(万円)']
dfj=pd.DataFrame(data=dfj,columns=columns)


pd.set_option('display.max_rows',None)

#本賞金

for i in range(len(df_race['グレード'])):
    if df_race['管轄'][i]=='地方':
        df_race.loc[[i],"本賞金"]=df_race["賞金(万円)"][i]
        #もらった賞金列を作る際にそれについても代入する
    else:
        if df_race['グレード'][i]=='G1':
            for j in range(len(df_g1['レース名'])):
                if df_race['レース名'][i]==df_g1['レース名'][j]:
                    df_race.loc[[i],"本賞金"]=df_g1["1着賞金(万円)"][j]
                    #df_race['本賞金'][i]=df_g1['1着賞金(万円)'][j]
                else:
                    pass
        elif (df_race['グレード'][i]=='G2' or df_race['グレード'][i]=='G3'):
            for j in range(len(df_g2['レース名'])):
                if df_race['レース名'][i]==df_g2['レース名'][j]:
                    df_race.loc[[i],"本賞金"]=df_g2["1着賞金(万円)"][j]
                else:
                    pass
        else:
            if df_race['馬齢'][i]==2:
                if df_race['競争条件'][i]=='一般':
                    if df_race['グレード'][i]=='オープン':
                        df_race.loc[[i],"本賞金"]=1150
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=750
                    elif df_race['グレード'][i]=='新馬':
                        df_race.loc[[i],"本賞金"]=700
                    elif df_race['グレード'][i]=='未勝利':
                        df_race.loc[[i],"本賞金"]=520
                    else:
                        pass
                else:
                    if df_race['グレード'][i]=='リステッド':
                        df_race.loc[[i],"本賞金"]=1700
                    elif df_race['グレード'][i]=='オープン':
                        df_race.loc[[i],"本賞金"]=1600
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=1030
                    else:
                        pass
            elif (df_race['馬齢'][i]==3 and df_race['季節'][i]=='春季'):
                if df_race['競争条件'][i]=='一般':
                    if df_race['グレード'][i]=='オープン':
                        df_race.loc[[i],"本賞金"]=1350
                    elif df_race['グレード'][i]=='2勝クラス':
                        df_race.loc[[i],"本賞金"]=1030
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=750
                    elif df_race['グレード'][i]=='新馬':
                        df_race.loc[[i],"本賞金"]=600
                    elif df_race['グレード'][i]=='未勝利':
                        df_race.loc[[i],"本賞金"]=520
                    else:
                        pass
                else:
                    if (df_race['グレード'][i]=='リステッド' and df_race['コース'][i]=='芝'):
                        df_race.loc[[i],"本賞金"]=2000
                    elif (df_race['グレード'][i]=='リステッド' and df_race['コース'][i]=='ダート'):
                        df_race.loc[[i],"本賞金"]=1900
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='芝'):
                        df_race.loc[[i],"本賞金"]=1900
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='ダート'):
                        df_race.loc[[i],"本賞金"]=1800
                    elif df_race['グレード'][i]=='2勝クラス':
                        df_race.loc[[i],"本賞金"]=1410
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=1030
                    else:
                        pass
            elif (df_race['馬齢'][i]==3 and df_race['季節'][i]=='夏季' or df_race['馬齢'][i]>=4):
                if df_race['競争条件'][i]=='一般':
                    if (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='芝'):
                        df_race.loc[[i],"本賞金"]=2100
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='ダート'):
                        df_race.loc[[i],"本賞金"]=2000
                    elif df_race['グレード'][i]=='3勝クラス':
                        df_race.loc[[i],"本賞金"]=1780
                    elif df_race['グレード'][i]=='2勝クラス':
                        df_race.loc[[i],"本賞金"]=1110
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=770
                    elif df_race['グレード'][i]=='未勝利':
                        df_race.loc[[i],"本賞金"]=520
                    else:
                        pass
                else:
                    if (df_race['グレード'][i]=='リステッド' and df_race['コース'][i]=='芝' and df_race['距離'][i]>=1800):
                        df_race.loc[[i],"本賞金"]=2600
                    elif (df_race['グレード'][i]=='リステッド' and df_race['コース'][i]=='芝' and df_race['距離'][i]<1800):
                        df_race.loc[[i],"本賞金"]=2500
                    elif (df_race['グレード'][i]=='リステッド' and df_race['コース'][i]=='ダート'):
                        df_race.loc[[i],"本賞金"]=2300
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='芝' and df_race['距離'][i]>=1800):
                        df_race.loc[[i],"本賞金"]=2400
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='芝' and df_race['距離'][i]<1800):
                        df_race.loc[[i],"本賞金"]=2300
                    elif (df_race['グレード'][i]=='オープン' and df_race['コース'][i]=='ダート'):
                        df_race.loc[[i],"本賞金"]=2200
                    elif df_race['グレード'][i]=='3勝クラス':
                        df_race.loc[[i],"本賞金"]=1840
                    elif df_race['グレード'][i]=='2勝クラス':
                        df_race.loc[[i],"本賞金"]=1510
                    elif df_race['グレード'][i]=='1勝クラス':
                        df_race.loc[[i],"本賞金"]=1070
                    else:
                        pass
            elif df_race['平or障'][i]=='障害':
                if df_race['競争条件'][i]=='一般':
                    if df_race['グレード'][i]=='オープン':
                        df_race.loc[[i],"本賞金"]=1350
                    elif df_race['グレード'][i]=='未勝利':
                        df_race.loc[[i],"本賞金"]=790
                    else:
                        pass
                else:
                    df_race.loc[[i],"本賞金"]=1650
            else:
                if df_race['グレード'][i]=='未勝利':
                    df_race.loc[[i],"本賞金"]=520

dft=df_race['着順']
#もらった賞金

for i in range(len(df_race['本賞金'])):
    if (df_race['競争条件'][i]=='一般' or df_race['競争条件'][i]=='特別' and dft[i]>=4):
            df_race.loc[[i],"賞金"]=df_race["賞金(万円)"][i]
    else:
        if dft[i]==1:
            df_race.loc[[i],"賞金"]=df_race["本賞金"][i]
        elif dft[i]==2:
            df_race.loc[[i],"賞金"]=(df_race['本賞金'][i]*0.4)
            df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_FLOOR))
            if df_race['賞金'][i]>=1000:
                df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1E2'),rounding=decimal.ROUND_HALF_UP))
            else:
               df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1E1'),rounding=decimal.ROUND_HALF_UP))
        elif dft[i]==3:
            df_race.loc[[i],"賞金"]=(df_race['本賞金'][i]*0.25)
            df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_FLOOR))
            if df_race['賞金'][i]>=1000:
                df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1E2'),rounding=decimal.ROUND_HALF_UP))
            else:
                df_race.loc[[i],"賞金"]=float(decimal.Decimal(df_race['賞金'][i]).quantize(decimal.Decimal('1E1'),rounding=decimal.ROUND_HALF_UP))
        else:
            pass


#出走奨励(三歳初出走、特別奨励含)

for i in range(len(df_race['本賞金'])):
    if df_race['グレード'][i]=='G1' or df_race['グレード'][i]=='G2' or df_race['グレード'][i]=='G3' or (df_race['平or障'][i]=='平地' and df_race['グレード'][i]=='オープン'):
        if dft[i]==6:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.08
        elif dft[i]==7:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.07
        elif dft[i]==8:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.06
        elif dft[i]==9:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.03
        elif dft[i]==10:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.02
        else:
            pass
    else:
        if dft[i]==6:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.08
        elif dft[i]==7:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.07
        elif dft[i]==8:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.06
        elif dft[i]==9:
            df_race.loc[[i],"出走奨励"]=df_race['本賞金'][i]*0.03
        else:
            pass

#特別奨励金（1800以上g2とグランプリのやつ）
g1_200=['大阪杯(G1)','天皇賞(春)(G1)','宝塚記念(G1)','天皇賞(秋)(G1)','ジャパンカップ(G1)','有馬記念(G1)']
g1_150=['フェブラリーS(G1)','高松宮記念(G1)','ヴィクトリアマイル(G1)','安田記念(G1)','スプリンターズS(G1)','エリザベス女王杯(G1)','マイルCS(G1)','チャンピオンズカップ(G1)']

for i in range(len(df_race['本賞金'])):
    if (df_race['馬齢'][i]>=3 and df_race['グレード'][i]=='G1' and dft[i]>=11):
        for j in range(len(g1_200)):
            if df_race['レース名'][i]==g1_200[j]:
                df_race.loc[[i],"出走奨励"]=df_race['出走奨励'][i]+200
            elif df_race['レース名'][i]==g1_150[j]:
                df_race.loc[[i],"出走奨励"]=df_race['出走奨励'][i]+150
            else:
                pass
    else:
        pass

#1800以上G2

for i in range(len(df_race['本賞金'])):
    if (df_race['馬齢'][i]>=3 and df_race['グレード'][i]=='G2' and dft[i]>=11 and df_race['コース'][i]=='芝' and df_race['距離'][i]>=1800):
        if df_race['クラス'][i]=='オープン':
            df_race.loc[[i],"出走奨励"]=df_race['出走奨励'][i]+100
        elif df_race['クラス'][i]=='3勝クラス':
            df_race.loc[[i],"出走奨励"]=df_race['出走奨励'][i]+50
        else:
            pass
    else:
        pass


#距離別

l=[0,1,0.4,0.25,0.15,0.1,0.08,0.07,0.06,0.03,0.02]

for i in range(len(df_race['本賞金'])):
    if (df_race['馬齢'][i]>=3 and df_race['コース'][i]=='芝' and df_race['距離'][i]>=1800 and dft[i]<=10 and df_race['平or障'][i]=='平地'):
        if (df_race['距離'][i]==1800 and df_race['グレード'][i]=='オープン') or (df_race['距離'][i]==1800 and df_race['グレード'][i]=='3勝クラス') or (df_race['距離'][i]==1800 and df_race['グレード'][i]=='2勝クラス') or (1800<=df_race['距離'][i]<=2000 and df_race['競争条件'][i]=='特別' and df_race['グレード'][i]=='1勝クラス'):
            df_race.loc[[i],"距離別"]=140*l[dft[i]]
        elif (df_race['距離'][i]>=2000 and df_race['競争条件'][i]=='特別' and df_race['グレード'][i]=='1勝クラス'):
            df_race.loc[[i],"距離別"]=200*l[dft[i]]
        elif (1800<=df_race['距離'][i]<=2000 and df_race['グレード'][i]=='オープン') or (1800<=df_race['距離'][i]<=2000 and df_race['グレード'][i]=='3勝クラス') or (1800<=df_race['距離'][i]<=2000 and df_race['グレード'][i]=='2勝クラス'):
            df_race.loc[[i],"距離別"]=260*l[dft[i]]
        elif (df_race['距離'][i]>=2000 and df_race['グレード'][i]=='オープン') or (df_race['距離'][i]>=2000 and df_race['グレード'][i]=='3勝クラス') or (df_race['距離'][i]>=2000 and df_race['グレード'][i]=='2勝クラス') :
            df_race.loc[[i],"距離別"]=380*l[dft[i]]
        elif (df_race['距離'][i]==1800) and (df_race['競争条件'][i]=='特別') and (df_race['グレード'][i]=='1勝クラス'):
            df_race.loc[[i],"距離別"]=80*l[dft[i]]
        else:
            pass



#内国産

dfg=df_race['グレード']
t=[0,1,0.4,0.25,0.15,0.1]
for i in range(len(df_race['本賞金'])):
    if (df_race['産地'][i]=='内国' and df_race['平or障'][i]=='平地' and dft[i]<=5):
        if dfg[i]=='新馬':
            if df_race['馬齢'][i]==2:
                df_race.loc[[i],"内国産"]=190*t[dft[i]]
            elif df_race['馬齢'][i]==3:
                df_race.loc[[i],"内国産"]=150*t[dft[i]]
            else:
                pass
        elif dfg[i]=='未勝利':
            if df_race['馬齢'][i]==2:
                df_race.loc[[i],"内国産"]=150*t[dft[i]]
            elif (df_race['馬齢'][i]==3 and df_race['季節'][i]=='夏季'):
                df_race.loc[[i],"内国産"]=60*t[dft[i]]
            elif (df_race['馬齢'][i]==3 and df_race['季節'][i]=='春季'):
                df_race.loc[[i],"内国産"]=110*t[dft[i]]
            else:
                pass
        else:
            if dfg[i]=='G1':
                df_race.loc[[i],"内国産"]=350*t[dft[i]]
            elif dfg[i]=='G2':
                df_race.loc[[i],"内国産"]=250*t[dft[i]]
            elif dfg[i]=='G3':
                df_race.loc[[i],"内国産"]=250*t[dft[i]]
            elif dfg[i]=='リステッド':
                df_race.loc[[i],"内国産"]=220*t[dft[i]]
            elif dfg[i]=='オープン':
                df_race.loc[[i],"内国産"]=200*t[dft[i]]
            elif dfg[i]=='3勝クラス':
                df_race.loc[[i],"内国産"]=160*t[dft[i]]
            elif dfg[i]=='2勝クラス':
                df_race.loc[[i],"内国産"]=130*t[dft[i]]
            elif (dfg[i]=='1勝クラス' and df_race['馬齢'][i]==2 or dfg[i]=='1勝クラス' and df_race['馬齢'][i]==3 and df_race['季節'][i]=='春季'):
                df_race.loc[[i],"内国産"]=110*t[dft[i]]
            elif (dfg[i]=='1勝クラス' and df_race['馬齢'][i]>=4 or df_race['馬齢'][i]==3 and dfg[i]=='1勝クラス'):
                df_race.loc[[i],"内国産"]=80*t[dft[i]]
            else:
                pass


#内国牝馬


for i in range(len(df_race['本賞金'])):
    if (df_race['グレード'][i]=='新馬' and dft[i]<=5 and df_race['産地'][i]=='内国' and df_race['性別'][i]=='牝' or '未勝利' and dft[i]<=5 and df_race['産地'][i]=='内国' and df_race['性別'][i]=='牝'):
        if dfg[i]=='新馬':
            if df_race['馬齢'][i]==2:
                df_race.loc[[i],"内国産"]=df_race['内国産'][i]+160*t[dft[i]]
            elif df_race['馬齢'][i]==3:
                df_race.loc[[i],"内国産"]=df_race['内国産'][i]+100*t[dft[i]]
            else:
                pass
        elif dfg[i]=='未勝利':
            if df_race['馬齢'][i]==2:
                df_race.loc[[i],"内国産"]=df_race['内国産'][i]+100*t[dft[i]]
            elif (df_race['馬齢'][i]==3 and df_race['季節'][i]=='春季'):
                df_race.loc[[i],"内国産"]=df_race['内国産'][i]+50*t[dft[i]]
            else:
                pass
        else:
            pass

df_race['日付']=df_race['日付'].astype(str)
df_race['内国産']=[(float(decimal.Decimal(df_race['内国産'][i]).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_HALF_UP)))*10000 for i in range(len(df_race['内国産']))]
df_race['出走奨励']=[(float(decimal.Decimal(df_race['出走奨励'][i]).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_HALF_UP)))*10000 for i in range(len(df_race['出走奨励']))]
df_race['距離別']=[(float(decimal.Decimal(df_race['距離別'][i]).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_HALF_UP)))*10000 for i in range(len(df_race['距離別']))]
df_race['賞金']=[df_race['賞金'][i]*10000 for i in range(len(df_race['賞金']))]


print(df_race)
df_race.to_excel(r"C:\Users\kyomu\OneDrive\デスクトップ\race_data.xlsx",index=None)
