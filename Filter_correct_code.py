
myDict = [
    {
        "Geography": ["US"],
        "Keyword": "chai",
        "Sector": "CPR",
        "Segments": "E-Commerce",
        "Sub-Sector": "Retail",
        "Year": [
            "2013",
            "2018"
        ]
    },
    {
        "Geography": ["US"],
        "Keyword": "Coffee",
        "Sector": "CPR",
        "Segments": "E-Commerce",
        "Sub-Sector": "Retail",
        "Year": [
            "2013-2018",
            "2018"
        ]
    },
    {
        "Geography": ["US"],
        "Keyword": "Green Tea",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "Retail",
        "Year": [
            "2020"
        ]
    },
{
        "Geography": ["US"],
        "Keyword": "T-Tea",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "Retail",
        "Year":
            ["2018"]

    },
    {
        "Geography": ["US"],
        "Keyword": 'M Tea',
        "Sector": "CPR",
        "Segments": "Convenience Store",
        "Sub-Sector": "Retail",
        "Year": [
            "2020"
        ]
    },
    {
        "Geography": ["UK"],
        "Keyword": "water",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "F&B",
        "Year": [
            "2020"
        ]
    },

    {
        "Geography": ["US","UK"],
        "Keyword": "BEAR",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "F&B",
        "Year": [
            "2021"
        ]
    }


]

values = [['US'],"",'',[],'CPR',['2020']]

result=[]
for i in myDict:
    for k,v in i.items():
        if v in values:
            result.append(i)
            if isinstance(v,list):
                for item in v:
                    match = any(item in sublist for sublist in values)
                    #print(match)
                    if match:
                        result.append(i)
            #else:
                #result.append(i)

final_result=[]
for dicts in result:
    flag = []
    #for key,vals in dicts.items():
        #print(vals,'Printing vals')
    for d in values:
        lst=list(dicts.values())
        #print(lst)
        #print(type(lst))
        if d ==[]:
            continue
        if d == '':
            continue
        #print(values.values())
        if d in lst:
            flag.append(True)
        else:
            flag.append(False)
            #print(dicts.values())

    #print(flag,'Flag')            #print(True)
    if all(flag):
        final_result.append(dicts)

#print(final_result)

lst2= [i for n, i in enumerate(final_result) if i not in final_result[n + 1:]]
#print(lst2)
for a in lst2:
    print(a)

