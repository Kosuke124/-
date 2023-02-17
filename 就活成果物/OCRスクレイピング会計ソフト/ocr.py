def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    

    i = texts[0] #画像から抽出したテキストデータ
    t = i.description.replace(' ','')#スペースを消去
    str_list = t.split()
    
    l = str_list
    name=[]
    money=[]
    sonota=[]

    for i in range(len(l)):
        if "号"in l[i]:
            name.append(l[i])
        elif "¥"in l[i]:
            money.append(l[i])
        else:
            sonota.append(l[i])

    list = []

    for i in range(len(name)):
        list.append("{0}{1}".format(name[i],money[i]))
        l[i] = list[i].split("号")
    
    import pyodbc
    for i in range(len(l)):
        con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\kyomu\OneDrive\ドキュメント\prot.accdb;'
        conn = pyodbc.connect(con_string)

        cursor = conn.cursor()

    
        myuser = (
            (i,l[i][0],2),
            )

        cursor.executemany('INSERT INTO T_馬名 VALUES (?,?,?)',myuser)
        conn.commit()
        print("data inserted")
    
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    
            
detect_text(r"C:\Users\kyomu\Mypython2\sample.jpg")



