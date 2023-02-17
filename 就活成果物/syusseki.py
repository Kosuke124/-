#出席テーブル
name=[]
d=[]
syuseki1=''.join(hatugen[0])
syuseki1=syuseki1.split("欠席")
syuseki=syuseki1[0]
for i in range(len(df['氏名'])):
    if df['氏名'][i] in syuseki:
        name.append(df['氏名'][i])
dfe = pd.DataFrame(data={'氏名':name})
for i in range(len(dfe['氏名'])):
    for j in range(len(df['氏名'])):
        if dfe['氏名'][i]==df['氏名'][j]:
            d.append(df['No'][j])
        else:
            pass
dfe['ID']=d
dfe['出席']=1

keseki=hatugen[0]

for i in range(len(keseki)):
    if '欠席' in keseki[i]:
        a=i+1
    elif '説明のため' in keseki[i]:
        b=i-1
    else:
        pass
keseki=keseki[a:b]
name_k=[]
z=[]

if 'なし' in keseki:
    pass
else:
    keseki=''.join(keseki)
    for i in range(len(df['氏名'])):
        if df['氏名'][i] in keseki:
            name_k.append(df['氏名'][i])
dff = pd.DataFrame(data={'氏名':name_k})
for i in range(len(dff['氏名'])):
    for j in range(len(df['氏名'])):
        if dff['氏名'][i]==df['氏名'][j]:
            z.append(df['No'][j])
        else:
            pass 

dff['ID']=z
dff['出席']=0

df_syusseki = dfe.append(dff,ignore_index=True)
df_syusseki['会議ID']=kaigiID
df_syusseki.to_csv(r"C:\Users\kyomu\OneDrive\デスクトップ\syusseki_T.csv", encoding='utf_8_sig')