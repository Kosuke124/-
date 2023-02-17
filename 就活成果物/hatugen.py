#発言テーブル作成
files = os.listdir(r"C:\Users\kyomu\Kansai University\NATORI,Ryota - ゼミ\H30ゼミデータ\01.議事録DL\28.兵庫県\三田市")
for filename in files:
    #テキストファイルを入れる
    path = fr"C:\Users\kyomu\Kansai University\NATORI,Ryota - ゼミ\H30ゼミデータ\01.議事録DL\28.兵庫県\三田市\{filename}"
    #s=path.split('\\')
    #last=s[-1]
    kaigiID=filename[:13]

    with open(path) as f:
        tex = f.read()

    #print(tex)
    tex=tex.strip()
    hatugen = re.split('[◎○◆]',tex)



    for i in range(len(hatugen)):
        hatugen[i] = hatugen[i].split()


    #議員テーブルを入れる
    #dfの1と2の日付の間indfhの日付を取得したものを比べて1と2の日付の間だった場合のみ通す
    #df＝の形にしてここでDFの中から必要データのみを抽出してdfに入れておく
    import datetime
    df = pd.read_excel(r"C:\Users\kyomu\Kansai University\NATORI,Ryota - ゼミ\H30ゼミデータ\03.委員会テーブル\28219三田市.xlsx")


    #データ型を日付型に変換
    df['date_start_nendo']=pd.to_datetime(df['date_start_nendo'], format='%Y%m%d')
    df['date_last_nendo']=pd.to_datetime(df['date_last_nendo'], format='%Y%m%d')

    str=kaigiID[:8]


    dft= pd.DataFrame(columns=['date'])
    dft = dft.append({'date': str}, ignore_index=True)

    dft['date']=pd.to_datetime(dft['date'], format='%Y%m%d')
    #後でｄｆを作る元の辞書を作成
    series_dict = {}
    # 行を作る
    for i in range(len(df['name_senkyo'])):
        if df['date_start_nendo'][i] <= dft['date'][0] <= df['date_last_nendo'][i]:
            tmp_se = pd.Series( [df['ID_giin_teirei'][i],df['ID_giin_senkyo'][i],df['new_and_old'][i],df['kaiha'][i],df['party'][i],df['gender'][i],df['age'][i],df['date_senkyo'][i],df['shicho_or_giin'][i],df['name_gikai'][i],df['date_start_nendo'][i],df['date_last_nendo'][i],df['jis_code'][i],df['year'][i]],index=['ID_giin_teirei','ID_giin_senkyo','new_and_old','kaiha','party','gender','age','date_senkyo','shicho_or_giin','name_gikai','date_start_nendo','date_last_nendo','jis_code','year'])
            series_dict[i] = tmp_se #辞書に追加


    df = pd.DataFrame.from_dict(series_dict, orient="index")
    df = df.reset_index(drop=True)

    #dfs=df[df['shicho_or_giin'] == 1]#市長テーブル
    #dfs = dfs.reset_index(drop=True)
    #名前が外国人だった場合にスペースに変更する

    for i in range(len(df['name_gikai'])):
        if '・' in df['name_gikai'][i]:
            df['name_gikai'][i].replace('・',' ')
        else:
            pass

    #名前を苗字と名前に分けて苗字をnameに入れる
    df['name_gikai']=df['name_gikai'].str.split(' ')  

    for i in range(len(df['name_gikai'])):
        df.loc[[i],['name1']]=df['name_gikai'][i][0]
    #発言データ（氏名と発言）の作成

    hatu_n=[]
    hatu_h=[]



    for i in range(len(hatugen)):
        if i==0:
            pass
        else:
            hatu_n.append(hatugen[i][0])
            h=hatugen[i]
            l=len(hatugen[i])+1
            hatu_h.append("".join(h[1:l:1]))

    dfh = pd.DataFrame(
        data={'氏名':hatu_n, 
              '発言':hatu_h,}
    )
    Id=[]
    for i in range(len(dfh['氏名'])):
        Id.append(np.nan)
    

    #発言の氏名に一致する苗字のnameを入れる。また、

    for i in range(len(dfh['氏名'])):
        print(hatugen[i][0])
        for j in range(len(df['name_gikai'])):
            if '市長' in hatugen[i][0]:
                dfh.loc[[i],['status']]=1
            elif '議長' in hatugen[i][0]:
                dfh.loc[[i],['status']]=2
            elif '議員' in hatugen[i][0]:
                dfh.loc[[i],['status']]=3
            else:
                dfh.loc[[i],['status']]=4
            if df['name1'][j] in dfh['氏名'][i]:
                dfh.loc[[i],['氏名']]="".join(df['name_gikai'][j])
                Id[i]=df['date_senkyo'][j]
                dfh.loc[[i],['age']]=df['age'][j]
                dfh.loc[[i],['gender']]=df['gender'][j]
                dfh.loc[[i],['party']]=df['party'][j]
                dfh.loc[[i],['kaiha']]=df['kaiha'][j]
                dfh.loc[[i],['new_and_old']]=df['new_and_old'][j]
                dfh.loc[[i],['ID_giin_senkyo']]=df['ID_giin_senkyo'][j]
                dfh.loc[[i],['ID_giin_teirei']]=df['ID_giin_teirei'][j]
                dfh.loc[[i],['jis_code']]=df['jis_code'][j]
                dfh.loc[[i],['year']]=df['year'][j]
            else:
                pass
    dfh.loc[[0],['status']]=2
    dfh['ID']=Id
    dfh['会議ID']=kaigiID

    #発言の必要ない記号などをカットする
    for i in range(len(dfh['発言'])):
        pos = dfh['発言'][i].find('－－')
        dfh.loc[[i],['発言']]=dfh['発言'][i][:pos]
        po = dfh['発言'][i].find('P.')
        dfh.loc[[i],['発言']]=dfh['発言'][i][:po]
        dfh.loc[[i],['発言']]=dfh['発言'][i].replace('－','')
        dfh.loc[[i],['発言']]=dfh['発言'][i].replace('―','')
        dfh.loc[[i],['発言']]=re.sub("\<.+?\>", "", dfh['発言'][i])
        dfh.loc[[i],['発言']]=re.sub("\（.+?\）", "", dfh['発言'][i])
        dfh.loc[[i],['発言']]=re.sub("\(.+?\)", "", dfh['発言'][i])
        if '（' in dfh['発言'][i]:
            pos = dfh['発言'][i].rfind('（')
            dfh.loc[[i],['発言']]=dfh['発言'][i][:pos]
        if '〔' in dfh['発言'][i]:
            dfh.loc[[i],['発言']]=dfh['発言'][i][:dfh['発言'][i].find('〔')]
        elif '～' in dfh['発言'][i]:
            dfh.loc[[i],['発言']]=dfh['発言'][i][:dfh['発言'][i].find('～')]
        elif len(dfh['発言'])-1==i:
            dfh.loc[[i],['発言']]=dfh['発言'][i][:dfh['発言'][i].find('午')]

    dfh['文字数']=[len(dfh['発言'][i]) for i in range(len(dfh['発言']))]
    #↓もし一行目にいらない文字が混ざる場合にコメントを外す
    #dfh=dfh[1:]

    dfh=dfh.reindex(columns=['会議ID','発言回数','氏名','発言','ID','文字数','age','gender','party','kaiha','new_and_old','ID_giin_senkyo','ID_giin_teirei','status','ID_teireikai','jis_code','year'])
    dfh=dfh.set_axis(['ID_kaigi','連番','speaker','statement','ID_giin_senkyo','発言数カウント','age','gender','party','kaiha','new_and_old','ID_giin_senkyo','ID_giin_teirei','status','ID_teireikai','jis_code','year'], axis=1)

    dfh['ID_giin_senkyo']=dfh['ID_giin_senkyo'].fillna(0) 
    dfh['連番']=pd.RangeIndex(start=1, stop=len(dfh.index) + 1, step=1)
    dfh=dfh.drop(['連番' , '発言数カウント','ID_giin_senkyo'] , axis = 1)
    dfk = pd.read_csv(r"C:\Users\kyomu\Documents\kaigitable_sanda.csv")
    dfk['id_kaigi']=dfk['id_kaigi'].astype('str')
    for i in range(len(dfk['id_kaigi'])):
        if kaigiID == dfk['id_kaigi'][i]:
            dfh['ID_teireikai']=dfk['id_teireikai'][i]
    #偶数行を削除
    dfh = dfh[[i%2==1 for i in range(len(dfh.index))]]

    #出力先
    dfh.to_csv(fr"C:\Users\kyomu\Documents\natorizemi\三田の完成\{kaigiID}.csv", encoding='utf_8_sig')#フォーマットを利用してテーブル名をpathの一部を切り取ったものにする。    else:
    