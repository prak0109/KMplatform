import json
from fuzzywuzzy import fuzz
from flask import flash
import keyboard
import pandas as pd
import win32com.client as win32,pythoncom

def show_names(keyword):
    result = []
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
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
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    result = []
    #keyword = input('Enter some keyword: ')
    for k, v in dataAdmin.items():
        if k == keyword:
            for i in v:
                result.append(i)

    return result

def get_level1():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    level1=[""]
    for i in dataAdmin['sectors']:
        level1.append(i)
    return level1

def get_partners():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    partners=[]
    for i in dataAdmin['partners']:
        partners.append(i)
    return partners

def get_leads():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    leads=[]
    for i in dataAdmin['project_leads']:
        leads.append(i)
    return leads

def get_accounts():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    accounts=[]
    for i in dataAdmin['accountname']:
        accounts.append(i['Account_name'])
    return accounts

def get_level2():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)

    level2subsectors = {"-1": ""}
    for k in dataAdmin['sectors'].keys():
        sub = []
        for k1 in dataAdmin['sectors'][k].keys():
            sub.append(k1)
        level2subsectors[k] = sub
    return level2subsectors

def get_level3():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
        level3segments = {"-1": ""}
        for k in dataAdmin['sectors'].keys():
            for k1 in dataAdmin['sectors'][k].keys():
                level3segments[k1] = dataAdmin['sectors'][k][k1]

        return level3segments

def add_industry(keyword, sector, subsector, segment):
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    lst= dataAdmin['sectors']
    if keyword == 'sector':
        allsectors = []
        for i in lst:
            allsectors.append(i)
        print(allsectors)
        sector_names = [item.lower() for item in allsectors]
        if (sector.lower() in sector_names):
            flash('Sector already exist')
        else:
            lst[sector] = {subsector: [segment]}

    elif keyword == 'sub-sector':
        subsectors=[]
        for i in lst[sector].keys():
            subsectors.append(i)
        subsector_names=[item.lower() for item in subsectors]
        #if subsector in lst[sector].keys():
        if subsector.lower() in subsector_names:
            flash('Subsector already exist')
        else:
            lst[sector][subsector] = [segment]

    elif keyword == 'segment':
        segments=[item.lower() for item in lst[sector][subsector]]
        #if segment in lst[sector][subsector]:
        if segment in segments:
            flash('Segment already exist')
        else:
            lst[sector][subsector].append(segment)

    return lst

def show_industry():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)

    level1 = []
    for i in dataAdmin['sectors'].keys():
        for k, v in dataAdmin['sectors'][i].items():
            ind_dict = {'Sectors': i, 'Sub-Sectors': k, 'Segments': v}
            level1.append(ind_dict)

    return level1

def show_projects():
    with open('projects.json') as json_file:
        projectData = json.load(json_file)
    return projectData['projects']

def get_names():
    with open('projects.json') as json_file:
        projectData = json.load(json_file)
    names=[]
    for i in projectData['projects']:
        names.append(i['Project Name'])
    return names

def get_geography():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    geograghy=[]
    for i in dataAdmin['Geography']:
        geograghy.append(i)
    return geograghy

def get_years():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    years=[]
    for i in dataAdmin['Years']:
        years.append(i)
    return years

def get_datatype():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    datatype=[]
    for i in dataAdmin['DataTypes']:
        datatype.append(i)
    return datatype

def get_top():
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
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
    with open('Metadata_new.json') as jsondata:
        searchdata = json.load(jsondata)
    filename = [x['Filename'] for x in searchdata]
    geography = [x['Geography'] for x in searchdata]
    sector = [x['Sector'] for x in searchdata]
    subsector = [x['Sub-Sector'] for x in searchdata]
    segments = [x['Segments'] for x in searchdata]
    year = [x['Year'] for x in searchdata]
    datatype= [x['Datatype'] for x in searchdata]
    project_name=[x['Project Name'] for x in searchdata]
    partner=[x['Partner'] for x in searchdata]
    project_type = [x['Project Type'] for x in searchdata]
    project_lead = [x['Project Lead'] for x in searchdata]
    project_account = [x['Project Account'] for x in searchdata]
    Team_member = [x['Team Member'] for x in searchdata]
    Key_word=[x['Keyword'] for x in searchdata]

    get_filename=fuzzy_match(term,filename)
    get_sector= fuzzy_match(term,sector)
    get_segments=fuzzy_match(term,segments)
    get_year=fuzzy_match(term,year)
    get_geo=fuzzy_match(term,geography)
    get_subsec=fuzzy_match(term,subsector)
    get_datatype=fuzzy_match(term,datatype)
    get_project_name=fuzzy_match(term,project_name)
    get_partner=fuzzy_match(term,partner)
    get_project_type=fuzzy_match(term,project_type)
    get_project_lead=fuzzy_match(term,project_lead)
    get_team_member=fuzzy_match(term,Team_member)
    get_project_account=fuzzy_match(term,project_account)
    get_keyword=fuzzy_match(term,Key_word)


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

    if len(get_subsec) > 0:
        for i in get_subsec:
            result = (list(filter(lambda x: x["Sub-Sector"] == i, searchdata)))
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

    if len(get_datatype)>0:
        for i in get_datatype:
            if isinstance(i,list):
                for item in i:
                    match= any(item in sublist for sublist in get_datatype)
                    if match:
                        result= (list(filter(lambda x: x["Datatype"] == i, searchdata)))
                        final_lst.append(result)
            else:
                result= (list(filter(lambda x: x["Datatype"] == i, searchdata)))
                final_lst.append(result)

    if len(get_project_name)>0:
        for i in get_project_name:
            result = (list(filter(lambda x: x["Project Name"] == i, searchdata)))
            final_lst.append(result)

    if len(get_partner)>0:
        for i in get_partner:
            if isinstance(i,list):
                for item in i:
                    match= any(item in sublist for sublist in get_datatype)
                    if match:
                        result= (list(filter(lambda x: x["Partner"] == i, searchdata)))
                        final_lst.append(result)
            else:
                result= (list(filter(lambda x: x["Partner"] == i, searchdata)))
                final_lst.append(result)

    if len(get_project_type)>0:
        for i in get_project_type:
            result = (list(filter(lambda x: x["Project Type"] == i, searchdata)))
            final_lst.append(result)

    if len(get_project_lead)>0:
        for i in get_project_lead:
            result = (list(filter(lambda x: x["Project Lead"] == i, searchdata)))
            final_lst.append(result)

    if len(get_team_member)>0:
        for i in get_team_member:
            if isinstance(i,list):
                for item in i:
                    match= any(item in sublist for sublist in get_team_member)
                    if match:
                        result= (list(filter(lambda x: x["Team Member"] == i, searchdata)))
                        final_lst.append(result)
            else:
                result= (list(filter(lambda x: x["Team Member"] == i, searchdata)))
                final_lst.append(result)

    if len(get_keyword)>0:
        for i in get_keyword:
            if isinstance(i,list):
                for item in i:
                    match= any(item in sublist for sublist in get_keyword)
                    if match:
                        result= (list(filter(lambda x: x["Keyword"] == i, searchdata)))
                        final_lst.append(result)
            else:
                result= (list(filter(lambda x: x["Keyword"] == i, searchdata)))
                final_lst.append(result)

    if len(get_project_account)>0:
        for i in get_project_account:
            result = (list(filter(lambda x: x["Project Account"] == i, searchdata)))
            final_lst.append(result)

    print(final_lst)
    keyword_result = []
    for lists in final_lst:
        for vals in lists:
            keyword_result.append(vals)

    return keyword_result

def filter_results(Geography,Sector,Segments,Subsector,Year,datatype,project_name,partner,project_type,project_lead,project_account):
    with open('Metadata_new.json') as jsondata:
        searchdata = json.load(jsondata)
    result = []
    filters_lst = [Geography, Sector, Segments, Subsector, Year,datatype,project_name,partner,project_type,project_lead,project_account]
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
    with open('admin.json') as json_file:
        dataAdmin = json.load(json_file)
    for i in dataAdmin['team_members']:
        members.append(i)
    return members

def send_mail_project(dict,teammember):
    df = pd.DataFrame.from_dict(dict,orient='index')
    html = df.to_html(header=False)
    #print(html)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    leads=[dict['Project Lead']]
    emailid = []
    for i in leads:
        str = i.split('<', 1)
        email = str[1][:-1]
        emailid.append(email)

    #mail.To = (';').join(emailid)+';'+(';').join(teammember)+';'+'EY_GDS_KMAdmin.GID@ey.net'
    mail.To = (';').join(emailid)+';'+(';').join(teammember)
    #print(mail.To)
    #mail.CC='Varun.Arora1@gds.ey.com'
    mail.CC = 'EY_GDS_KMAdmin.GID@ey.net'
    mail.Subject = "KM Platform | New Project has been Created"
    # mail.Body = 'Testing for KM Platform'
    mail.HTMLBody = 'Hi All,' + '<br>' + '<br>' + 'A new project id has been created for review,please find the details below:' + '<br>' + '<br>' + html
    mail.display(False)
    #keyboard.press_and_release('alt + s')
    #keyboard.press_and_release('alt + s')

def send_mail_project_update(dict,teammember):
    df = pd.DataFrame.from_dict(dict,orient='index')
    html = df.to_html(header=False)
    #print(html)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    #leads=get_leads()
    leads = [dict['Project Lead']]
    emailid = []
    for i in leads:
        str = i.split('<', 1)
        email = str[1][:-1]
        emailid.append(email)

    mail.To = (';').join(emailid)+';'+(';').join(teammember)
    #print(mail.To)
    mail.CC='EY_GDS_KMAdmin.GID@ey.net'
    mail.Subject = "KM Platform | New Project has been Created"
    # mail.Body = 'Testing for KM Platform'
    mail.HTMLBody = 'Hi All,' + '<br>' + '<br>' + 'Project has been updated for review,please find the details below:' + '<br>' + '<br>' + html
    mail.display(False)
    #keyboard.press_and_release('alt + s')
    #keyboard.press_and_release('alt + s')

#def send_mail_upload(dict,path):
def send_mail_upload(dict):
    # df = pd.DataFrame(dict)
    df = pd.DataFrame.from_dict(dict,orient='index')
    html = df.to_html(header=False)
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    leads=[dict['Project Lead']]
    #leads=get_leads()
    emailid = []
    for i in leads:
        string = i.split('<', 1)
        email = string[1][:-1]
        emailid.append(email)
    #print(emailid)
    mail.To = (';').join(emailid)
    #mail.CC = 'Varun.Arora1@gds.ey.com'+';'+'EY_GDS_KMAdmin.GID@ey.net'
    mail.Subject = "KM Platform | New File has been uploaded"
    #mail.Attachments.Add(path)
    # mail.Body = 'Testing for KM Platform'
    mail.HTMLBody = 'Hi All,' + '<br>' + '<br>' + 'A new file has been uploaded for review,please find the details below:' + '<br>' + '<br>' + html
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


