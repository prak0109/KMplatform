
myDict = [
    {
        "Geography": ["US"],
        "Keyword": "Tea",
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
        "Keyword": "Green Tea",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "Retail",
        "Year":
            ["2018"]

    },
    {
        "Geography": ["US"],
        "Keyword": 'TEA',
        "Sector": "CPR",
        "Segments": "Convenience Store",
        "Sub-Sector": "Retail",
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
            "2020"
        ]
    },

    {
        "Geography": ["UK"],
        "Keyword": "BEAR",
        "Sector": "CPR",
        "Segments": "Food",
        "Sub-Sector": "F&B",
        "Year": [
            "2021"
        ]
    }


]

values = [[], 'CPR', '-1', '-1', []]
for n,i in enumerate(values):
    if isinstance(values[n],list):
        continue
    else:
        if (values[n] == None or values[n] == '-1'):
            values[n]=''

print(values)
#l = list(map(lambda x: {k:v for k, v in x.items() if v in values}, myDict))
#print(l)

#l1 = [{myDict[i] for k, v in i.items() if v in values} for i in myDict]

#print(l1)
result=[]
for i in myDict:
    for k,v in i.items():
        if isinstance(v,list):
            for item in v:
                match=any(item in sublist for sublist in values)
                if match:
                    result.append(i)
        elif v in values:
            result.append(i)

#print(result)

final_result=[]
for dicts in result:
    flag = []
    #for key,vals in dicts.items():
        #print(vals,'Printing vals')
    for d in values:
        lst=list(dicts.values())
        print(lst)
        print(type(lst))
        if d ==[]:
            continue
        if d == '':
            continue
        if d == None:
            continue
        #print(values.values())
        if d in lst:
            flag.append(True)
        else:
            flag.append(False)
            #print(dicts.values())

    print(flag,'Flag')
    if all(flag):
        final_result.append(dicts)

print(final_result)


#for a in final_result:
    #print(a)
