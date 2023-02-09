import json
from fuzzywuzzy import fuzz
import keyboard
import pandas as pd
import win32com.client as win32,pythoncom

with open('admin.json') as json_file:
    dataAdmin= json.load(json_file)

with open('projects.json') as json_file:
    projectData= json.load(json_file)

with open('Metadata_new.json') as jsondata:
  searchdata = json.load(jsondata)

def show_names(keyword):
    result = []
    #keyword = input('Enter some keyword: ')
    for k, v in dataAdmin.items():
        if k == keyword:
            for i in v:
                result.append(i)

    final_res = []
    for item in result:
        # print(item)
        str = item.split('<', 1)
        name = str[0]
        email = str[1][:-1]
        # print({'Name':name,'Email id':email})
        final_res.append({'Name': name, 'Email id': email})

    return final_res

def show_accounts(keyword):
    result = []
    #keyword = input('Enter some keyword: ')
    for k, v in dataAdmin.items():
        if k == keyword:
            for i in v:
                result.append(i)

    return result

def get_level1():
    level1=[""]
    for i in dataAdmin['sectors']:
        for k,v in i.items():
            level1.append(k)
    return level1

def get_partners():
    partners=[]
    for i in dataAdmin['partners']:
        partners.append(i)
    return partners

def get_leads():
    leads=[]
    for i in dataAdmin['project_leads']:
        leads.append(i)
    return leads

def get_accounts():
    accounts=[]
    for i in dataAdmin['accountname']:
        accounts.append(i['Account_name'])
    return accounts

def get_related_subchilds(key):
    level2=get_level2()
    level2subsectors=[]
    level2subsegments=[]
    for i in level2[0]:
        for k,v in i.items():
            if(k == -1 or k == key):
                level2subsectors=level2subsectors+v

    for i in level2[1]:
        for k, v in i.items():
            if (k == -1 or k == key):
                level2subsegments=level2subsegments+v

def get_level2():
    level2subsectors= [{"-1": ""}]
    level2segments = [{"-1": ""}]
    for i in dataAdmin['sectors']:
        for k, v in i.items():
            level2subsectors.append({k : v["Subsector"]})
            level2segments.append({k:v["Segments"]})
    return [level2subsectors, level2segments]

def add_industry(keyword, sector, subsector, segment):
    lst= dataAdmin['sectors']
    if keyword == 'sector':
        allsectors = []
        for i in range(len(lst)):
            allsectors+=list(lst[i].keys())

        print(allsectors)

        if (sector in allsectors):
            #flash('Sector already exist','Sector already exist')
            print('Sector already exist','Sector already exist')
        else:
            lst.append({sector: {'Segments': [segment], 'Subsector': [subsector]}})
    elif keyword == 'sub-sector':
        for i in range(len(lst)):
            sectors=(list(lst[i].keys()))
            if sectors[0]==sector:
                for k,v in lst[i][sector].items():
                    if k =='Subsector':
                        v.append(subsector)
                    elif k=='Segments':
                        v.append(segment)

    elif keyword == 'segment':
        for i in range(len(lst)):
            sectors = (list(lst[i].keys()))
            if (sectors[0] == sector) and (subsector in lst[i][sector]['Subsector']):
               lst[i][sector]['Segments'].append(segment)

    return lst

def show_industry():
    return dataAdmin["sectors"]

def show_projects():
    return projectData['projects']

def get_names():
    names=[]
    for i in projectData['projects']:
        names.append(i['Project Name'])
    return names

def get_geography():
    geograghy=[]
    for i in dataAdmin['Geography']:
        geograghy.append(i)
    return geograghy

def get_years():
    years=[]
    for i in dataAdmin['Years']:
        years.append(i)
    return years

def get_datatype():
    datatype=[]
    for i in dataAdmin['DataTypes']:
        datatype.append(i)
    return datatype

def get_top():
    top=[]
    for i in dataAdmin['TOP']:
        top.append(i)
    return top

def fuzzy_match(keyword,lst):
    l1=[]
    for i in lst:
        if fuzz.partial_ratio(keyword.lower(),str(i).lower())>=80:
            l1.append(i)

    filter = []
    for ele in l1:
        if set(ele) not in [set(x) for x in filter]:
            filter.append(ele)

    return filter

def get_results(term,data):
    filename = [x['Filename'] for x in searchdata]
    geography = [x['Geography'] for x in searchdata]
    sector = [x['Sector'] for x in searchdata]
    subsector = [x['Sub-Sector'] for x in searchdata]
    segments = [x['Segments'] for x in searchdata]
    year = [x['Year'] for x in searchdata]

    get_filename=fuzzy_match(term,filename)
    get_sector= fuzzy_match(term,sector)
    get_segments=fuzzy_match(term,segments)
    get_year=fuzzy_match(term,year)
    get_geo=fuzzy_match(term,geography)

    final_lst = []

    if len(get_filename) > 0:
        for i in get_filename:
            result = (list(filter(lambda x: x["Filename"] == i, searchdata)))
            final_lst.append(result)

    if len(get_year) > 0:
        for i in get_year:
            if isinstance(i, list):
                for item in i:
                    match = any(item in sublist for sublist in get_year)
                    if match:
                        result = (list(filter(lambda x: x["Year"] == i, data)))
                        final_lst.append(result)
            else:
                result = (list(filter(lambda x: x["Year"] == i, searchdata)))
                final_lst.append(result)

    if len(get_segments) > 0:
        for i in get_segments:
            result = (list(filter(lambda x: x["Segments"] == i, searchdata)))
            final_lst.append(result)

    if len(get_sector) > 0:
        for i in get_sector:
            result = (list(filter(lambda x: x["Sector"] == i, searchdata)))
            final_lst.append(result)

    if len(get_geo)>0:
        for i in get_geo:
            if isinstance(i,list):
                for item in i:
                    match= any(item in sublist for sublist in get_geo)
                    if match:
                        result= (list(filter(lambda x: x["Geography"] == i, searchdata)))
                        final_lst.append(result)
            else:
                result= (list(filter(lambda x: x["Geography"] == i, searchdata)))
                final_lst.append(result)

    print(final_lst)
    keyword_result = []
    for lists in final_lst:
        for vals in lists:
            keyword_result.append(vals)

    return keyword_result

def filter_results(Geography,Sector,Segments,Subsector,Year):
    result = []
    filters_lst = [Geography, Sector, Segments, Subsector, Year]
    for n, i in enumerate(filters_lst):
        if isinstance(filters_lst[n], list):
            continue
        else:
            if (filters_lst[n] == None or filters_lst[n] == '-1'):
                filters_lst[n] = ''
    for i in searchdata:
        for k, v in i.items():
            if v in filters_lst:
                result.append(i)
                if isinstance(v,list):
                    for item in v:
                        match=any(item in sublist for sublist in filters_lst)
                        if match:
                            result.append(i)
            #elif v in filters_lst:
                #result.append(i)
    final_result = []
    for dicts in result:
        flag = []
        for d in filters_lst:
            lst = list(dicts.values())
            if d == []:
                continue
            if d == '':
                continue
            # print(values.values())
            if d in lst:
                flag.append(True)
            else:
                flag.append(False)

        if all(flag):
            final_result.append(dicts)

    lst2 = [i for n, i in enumerate(final_result) if i not in final_result[n + 1:]]
    return lst2

def get_team_members():
    members = []
    for i in dataAdmin['team_members']:
        members.append(i)
    return members

def send_mail_project(dict):
    df = pd.DataFrame(dict)
    html = df.to_html(index=False)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    leads=get_leads()
    emailid = []
    for i in leads:
        str = i.split('<', 1)

        email = str[1][:-1]
        emailid.append(email)
    print(emailid)
    mail.To = (';').join(emailid)
    mail.CC='prakhar.rastogi1@gds.ey.com'
    mail.Subject = "KM Platform | New Project has been Created"
    # mail.Body = 'Testing for KM Platform'
    mail.HTMLBody = 'Hi,' + '<br>' + '<br>' + 'A new project id has been created for review' + '<br>' + '<br>' + html
    mail.display(False)
    #keyboard.press_and_release('alt + s')
    #keyboard.press_and_release('alt + s')

def send_mail_upload(dict):
    df = pd.DataFrame(dict)
    html = df.to_html(index=False)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    leads=get_leads()
    emailid = []
    for i in leads:
        str = i.split('<', 1)

        email = str[1][:-1]
        emailid.append(email)
    print(emailid)
    mail.To = (';').join(emailid)
    mail.CC='prakhar.rastogi1@gds.ey.com'
    mail.Subject = "KM Platform | New File has been uploaded"
    # mail.Body = 'Testing for KM Platform'
    mail.HTMLBody = 'Hi,' + '<br>' + '<br>' + 'A new file has been uploaded for review' + '<br>' + '<br>' + html
    mail.display(False)
    #keyboard.press_and_release('alt + s')
    #keyboard.press_and_release('alt + s')

def validate_access_leads():
    leads = get_leads()
    proj_leads = []
    for i in leads:
        str = i.split('<', 1)
        email = str[1][:-1]
        proj_leads.append(email)
    return proj_leads

def validate_access_partners():
    part = get_partners()
    partners=[]
    for i in part:
        str = i.split('<', 1)
        email = str[1][:-1]
        partners.append(email)
    return partners

def validate_access_teammembers():
    members = get_team_members()
    team_members = []
    for i in members:
        str = i.split('<', 1)
        email = str[1][:-1]
        team_members.append(email)
    return team_members




















