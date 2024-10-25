import json
import sqlite3

with open("works.json", encoding='utf-8-sig') as j:
    d=json.load(j)

#with open("work.json",'w') as w:
#    w.write(json.dumps(d[0],ensure_ascii=False))
i=0
for j in d:
    i+=1

    #print(j['ОснованиеРаботы'])
    print(j['Исполнители'][0]['СтатусЗаявки'])
    print(j['Исполнители'][0]['Срочность'])
    print(j['Статус'])

    #print(j['Услуги'][0]['Номенклатура']['Наименование'])
    #print(j['Услуги'][0]['ЕдИзмерения'])



#con = sqlite3.connect("../works.db")
#cur = con.cursor()
#sql = "INSERT INTO works (number_work, date_,summ) VALUES (?,?,?)"

#for i in d:
#    print(i['СчетВыставлен'])
#    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

#con.commit()
#con.close()