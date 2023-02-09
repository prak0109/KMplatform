from flask import Flask, render_template, request, url_for,flash,get_flashed_messages,redirect
from flask import jsonify,json




app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

with open('admin.json') as json_file:
    data= json.load(json_file)

with open('projects.json') as json_file:
    projectData= json.load(json_file)


def show_names(keyword):
    result = []
    #keyword = input('Enter some keyword: ')
    for k, v in data.items():
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
    for k, v in data.items():
        if k == keyword:
            for i in v:
                result.append(i)

    return result


def get_level1():
    level1=[""]
    for i in data['sectors']:
        for k,v in i.items():
            level1.append(k)
    return level1

def get_partners():
    partners=[]
    for i in data['partners']:
        partners.append(i)
    return partners    

def get_leads():
    leads=[]
    for i in data['project_leads']:
        leads.append(i)
    return leads    

def get_accounts():
    accounts=[]
    for i in data['accountname']:
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
    for i in data['sectors']:
        for k, v in i.items():
            level2subsectors.append({k : v["Subsector"]})
            level2segments.append({k:v["Segments"]})
    return [level2subsectors, level2segments]

def add_industry(keyword, sector, subsector, segment):
    lst= data['sectors']
    if keyword == 'sector':
        allsectors = []
        for i in range(len(lst)):
            allsectors+=list(lst[i].keys())

        print(allsectors)

        if (sector in allsectors):
            flash('Sector already exist','Sector already exist')
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
    return data["sectors"]

def show_projects():
    return projectData['projects']

def get_team_members():
    members = []
    for i in data['team_members']:
        members.append(i)
    return members

@app.route('/', methods=['GET','POST'])
def index():
    sectors=get_level1()
    options=get_level2()
    partners=get_partners()
    leads=get_leads()
    accounts=get_accounts()
    options=json.dumps(options,ensure_ascii = False)
    projectDataJson=json.dumps(projectData,ensure_ascii = False)
    team_members=get_team_members()
    return render_template('admin_updated.html', sectors=sectors, options=options,partners=partners,leads=leads,accounts=accounts,projects=projectDataJson,teammembers=team_members)

@app.route('/test', methods = ['GET','POST'])
def test():
    outcome = []
    if request.method == 'POST' and request.form.get('add_show')=='show':

        if request.form.get('sub-category')=='partners' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('sub-category')=='project_leads' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('sub-category')=='team_members' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('category')=='accountname' and request.form.get('add_show')=='show':
            outcome=show_accounts(request.form.get('category'))
            print(outcome)

        elif request.form.get('category')=='industry' and request.form.get('add_show')=='show':
            outcome=show_industry()
            print(outcome)

        elif request.form.get('category')=='project' and request.form.get('add_show')=='show':
            outcome=show_projects()
            print(outcome)

        outcome = json.dumps(outcome, ensure_ascii=False)
        return render_template('admin_page_results.html', outcome=outcome)

    elif request.method =="POST" and (request.form.get('add_show')=='add' or request.form.get('add_show') == 'update'):

        email_id = request.form.get('emailmem')
        name = request.form.get('memname')
        project_sec = request.form.get('sec')
        project_subsec = request.form.get('Subsec')
        project_seg = request.form.get('seg')
        project_top = request.form.get('top')
        project_startdate = request.form.get('startdate')
        project_rprojname = request.form.get('rprojname')
        project_projname = request.form.get('projname')
        project_partner = request.form.getlist('partner')
        #project_legalacc = request.form.get('legalacc')
        #project_capiq = request.form.get('capiq')
        project_account = request.form.get('account')
        project_projlead = request.form.get('projlead')
        comp_name = name + '<' + email_id + '>'
        account_name= request.form.get('legalacc')
        capital_iq_link= request.form.get('capiq')
        industry_sec_input = request.form.get('indSectorVal')
        industry_subsec_input = request.form.get('indSubSecVal')
        industry_seg_input = request.form.get('indSegmentVal')
        industry_sec_dropdown = request.form.get('sectordropdown')
        industry_subsec_dropdown = request.form.get('subsectordropdown')
        projectname_dropdown = request.form.get('projectNames')

        #print (1)
        if request.form.get('sub-category') == 'partners' and request.form.get('add_show') == 'add':
            Partner = data['partners']
            #sub-partner = Partner['sub-partner']
            #if ((comp_name in Partner) == false) {
            Partner.append(comp_name)

        elif request.form.get('sub-category') == 'project_leads' and request.form.get('add_show') == 'add':
            Project_lead = data['project_leads']
            Project_lead.append(comp_name)

        elif request.form.get('sub-category') == 'team_members' and request.form.get('add_show') == 'add':
            Team_member = data['team_members']
            Team_member.append(comp_name)

        elif request.form.get('category')=='accountname' and request.form.get('add_show') == 'add':
            acc_name= data['accountname']
            acct_dict={"Account_name":account_name ,"Capital_iq":capital_iq_link}
            acc_name.append(acct_dict)

        elif request.form.get('category')=='industry' and request.form.get('add_show') == 'add':
            if request.form.get('subcateind')=='sector':
                data['sectors']=add_industry(request.form.get('subcateind'), industry_sec_input, industry_subsec_input,industry_seg_input)
            elif request.form.get('subcateind') == 'sub-sector':
                data['sectors']=add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_input,
                             industry_seg_input)
            elif request.form.get('subcateind') == 'segment':
                data['sectors']=add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_dropdown,
                             industry_seg_input)


        elif request.form.get('category')=='project' and request.form.get('add_show')=='add':
            Project_data = projectData["projects"]
            print(Project_data)
            lastItem = Project_data[-1]
            if ("Project ID" in lastItem.keys()):
                lastItemId = lastItem["Project ID"]
                id = int(lastItemId.split(".")[-1])
                print(id)
                project_id = project_sec[0:2].upper() + "." + project_subsec[0:2].upper() + "." + str(id + 1)
            else:
                project_id = project_sec[0:2].upper() + "." + project_subsec[0:2].upper() + "." + str(1)

            project_dict = {"Project ID": project_id, "Project Sector": project_sec,
                            "Project Sub Sector": project_subsec, "Project Segment": project_seg,
                            "Project Type": project_top, "Project Start Date": project_startdate,
                            "RMT Project Name": project_rprojname
                , "Project Name": project_projname, "Project Partner": project_partner,
                            "Project Account": project_account, "Project Lead": project_projlead}
            Project_data.append(project_dict)


        elif request.form.get('category') == 'project' and request.form.get('add_show') == 'update':
            for tmp in projectData['projects']:
                #tmp=i.copy()
                #for k, v in tmp.items():
                if tmp["Project Name"] == projectname_dropdown:
                    tmp["Project Name"] = request.form.get('projname')
                    tmp["Project Lead"] = request.form.get('projlead')
                    tmp["project_startdate"]= request.form.get('startdate')
                    tmp["RMT Project Name"]=request.form.get('rprojname')
                    tmp["Project Partner"]=request.form.getlist('partner')

                print(projectData['projects'])

        with open('admin.json', 'w') as f:
            json.dump(data, f, indent=4)

        with open('projects.json', 'w') as f:
            json.dump(projectData, f, indent=4)

        #flash('Added Successfully', 'Add')
        return ('Json modified Sucessfully')


if __name__ == '__main__':
    app.run(debug=True)


