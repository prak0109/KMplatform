
mydict = {
    "Partners": [
        "Prakhar Rastogi<prakhar.rastogi1@gds.ey.com>"
    ],
    "Project_Leads": [
        "Mitali Chopra<Mitali.Chopra@gds.ey.com>"
    ],
    "Team_members": [
        "Sanya Singla<Sanya.Singla@gds.ey.com>",
        "Priya Sharma<Priya.Sharma5@gds.ey.com>"
    ]
}

result=[]
keyword = input('Enter some keyword: ')
for k,v in mydict.items():
    if k ==keyword:
        for i in v:
            result.append(i)

final_res=[]
for item in result:
    #print(item)
    str = item.split('<',1)
    name=str[0]
    email= str[1][:-1]
    #print({'Name':name,'Email id':email})
    final_res.append({'Name':name,'Email id':email})

print(final_res)








