from flask import Flask, render_template, request, url_for,flash,redirect,send_file
import model as m1
import json
import os
import re
from werkzeug.utils import secure_filename
from pathlib import Path
import io
import zipfile36 as zipfile
import win32com.client as win32,pythoncom
from filelock import FileLock
import sys

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

#os.chdir(r'\\Ingurusrfl010.ey.net\\010gru00044\\U\\UKI_CAS\\KMTool')  # for remote

with open('admin.json') as json_file:
    data= json.load(json_file)

with open('projects.json') as json_file:
    projectData= json.load(json_file)

with open('Metadata_new.json') as json_file:
    metadata= json.load(json_file)

@app.route('/')
def home():
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
    email_id = outlook.Accounts.Item(1).DisplayName
    #print(email_id)
    validate_leads=m1.validate_access_leads()
    validate_partners= m1.validate_access_partners()
    validate_members=m1.validate_access_teammembers()
    if email_id in validate_leads:
        leads=True
    if email_id in validate_partners:
        partners=True
    if email_id in validate_members:
        members = True
    return render_template('home.html', leads=validate_leads,partners=validate_partners,members=validate_members)

@app.route('/admin', methods=['GET','POST'])
def index():
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
    email_id = outlook.Accounts.Item(1).DisplayName
    validate_leads = m1.validate_access_leads()
    validate_leads = [x.lower() for x in validate_leads]
    validate_partners = m1.validate_access_partners()
    validate_partners = [x.lower() for x in validate_partners]

    if not email_id.lower() in validate_partners:
        if not email_id.lower() in validate_leads:
            return render_template('admin_auth_failure.html')
    #print(email_id)
    sectors=m1.get_level1()
    subsectors = m1.get_level2()
    segments = m1.get_level3()
    #options=m1.get_level2()
    partners=m1.get_partners()
    leads=m1.get_leads()
    accounts=m1.get_accounts()
    team_members = m1.get_team_members()
    tops=m1.get_top()
    #options=json.dumps(options,ensure_ascii = False)
    projectDataJson=json.dumps(projectData,ensure_ascii = False)
    subsectors=json.dumps(subsectors,ensure_ascii = False)
    segments=json.dumps(segments,ensure_ascii = False)
    return render_template('admin_v1.html', sectors=sectors,partners=partners,leads=leads,accounts=accounts,projects=projectDataJson,teammembers=team_members,
                           subsectors=subsectors,segments=segments,tops=tops)

@app.route('/admin_results', methods = ['GET','POST'])
def admin_results():
    outcome = []

    if request.method == 'POST' and request.form.get('add_show')=='show':

        if request.form.get('sub-category')=='partners' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=m1.show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('sub-category')=='project_leads' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=m1.show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('sub-category')=='team_members' and request.form.get('add_show')=='show' and request.form.get('category')=='strategy':
            outcome=m1.show_names(request.form.get('sub-category'))
            print(outcome)

        elif request.form.get('category')=='accountname' and request.form.get('add_show')=='show':
            outcome=m1.show_accounts(request.form.get('category'))
            print(outcome)

        elif request.form.get('category')=='industry' and request.form.get('add_show')=='show':
            outcome=m1.show_industry()
            print(outcome)

        elif request.form.get('category')=='project' and request.form.get('add_show')=='show':
            outcome=m1.show_projects()
            print(outcome)

        outcome = json.dumps(outcome, ensure_ascii=False)
        return render_template('admin_results_v1.html', outcome=outcome)

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
        project_teammember = request.form.getlist('teammember')
        domain_lst = ['gds.ey.com', 'parthenon.ey.com', 'in.ey.com','ey.com']

        if request.form.get('sub-category') == 'partners' and request.form.get('add_show') == 'add':
            filtered_email = []
            for i in data['partners']:
                string = i.split('<', 1)
                email = string[1][:-1]
                filtered_email.append(email)
            output = re.split(r'[@]', email_id)
            if email_id.lower() in [x.lower() for x in filtered_email]:
                flash('ID Already Exist in Partners')
            elif output[1] not in domain_lst:
                flash('Please enter valid EY Email ID')
            else:
                data['partners'].append(comp_name)
                flash('Partner Added Successfully')


        elif request.form.get('sub-category') == 'project_leads' and request.form.get('add_show') == 'add':
            filtered_email = []
            for i in data['project_leads']:
                string = i.split('<', 1)
                email = string[1][:-1]
                filtered_email.append(email)
            output = re.split(r'[@]', email_id)
            if email_id.lower() in [x.lower() for x in filtered_email]:
                flash('ID Already Exist in Project Leads')
            elif output[1] not in domain_lst:
                flash('Please enter valid EY Email ID')
            else:
                data['project_leads'].append(comp_name)
                flash('Project Lead Added Successfully')


        elif request.form.get('sub-category') == 'team_members' and request.form.get('add_show') == 'add':
            filtered_email = []
            for i in data['team_members']:
                string = i.split('<', 1)
                email = string[1][:-1]
                filtered_email.append(email)
            output = re.split(r'[@]', email_id)
            if email_id.lower() in [x.lower() for x in filtered_email]:
                flash('ID Already Exist in Team Members')
            elif output[1] not in domain_lst:
                flash('Please enter valid EY Email ID')
            else:
                data['team_members'].append(comp_name)
                flash('Team Member Added Successfully')

        elif request.form.get('category')=='accountname' and request.form.get('add_show') == 'add':
            accountNames = [item['Account_name'].lower() for item in data['accountname']]
            #print(accountNames)
            if (account_name.lower() in accountNames):
                flash('Account Name Already Exist')
            else:
                acc_name= data['accountname']
                acct_dict={"Account_name":account_name ,"Capital_iq":capital_iq_link}
                acc_name.append(acct_dict)
                flash('Account Added Successfully')

        elif request.form.get('category')=='industry' and request.form.get('add_show') == 'add':

            if request.form.get('subcateind')=='sector':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_input, industry_subsec_input,industry_seg_input)
                flash('Sector,Sub-Sector and Segment added successfully')
            elif request.form.get('subcateind') == 'sub-sector':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_input,industry_seg_input)
                flash('Sub-Sector and Segment added successfully')
            elif request.form.get('subcateind') == 'segment':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_dropdown,industry_seg_input)
                flash('Segment added successfully')

        elif request.form.get('category')=='project' and request.form.get('add_show')=='add':
            rmt_projNames = [item['RMT Project Name'].lower() for item in projectData["projects"]]
            # print(accountNames)
            if (project_rprojname.lower() in rmt_projNames):
                flash('RMT Project Name Already Exist')
            else:
                Project_data = projectData["projects"]
                #print(Project_data)
                lastItem = Project_data[-1]
                if ("Project ID" in lastItem.keys()):
                    lastItemId = lastItem["Project ID"]
                    id = int(lastItemId.split(".")[-1])
                    print(id)
                    project_id = project_sec[0:2].upper() + "." + project_subsec[0:2].upper() + "." + str(id+1)
                else:
                    project_id = project_sec[0:2].upper() + "." + project_subsec[0:2].upper() + "." + str(1)

                member_id = []
                for i in project_teammember:
                    mail = i.split('<', 1)
                    email = mail[1][:-1]
                    member_id.append(email)
                #print(member_id)

                project_dict = {"Project ID": project_id, "Project Sector": project_sec,
                                "Project Sub Sector": project_subsec, "Project Segment": project_seg,
                                "Project Type": project_top, "Project Start Date": project_startdate,
                                "RMT Project Name": project_rprojname,"Project Name": project_projname, "Project Partner": project_partner,
                                "Project Account": project_account, "Project Lead": project_projlead,"Project Team Member":project_teammember}
                Project_data.append(project_dict)
                flash('Project Added Successfully')
                #print(project_dict)
                m1.send_mail_project(project_dict, member_id)
                #m1.send_mail_project(project_dict,member_id)

        elif request.form.get('category') == 'project' and request.form.get('add_show') == 'update':
            for tmp in projectData['projects']:
                if tmp["Project Name"] == projectname_dropdown:
                    tmp["Project Name"] = request.form.get('projname')
                    tmp["Project Lead"] = request.form.get('projlead')
                    tmp["Project Start Date"]= request.form.get('startdate')
                    tmp["RMT Project Name"]=request.form.get('rprojname')
                    tmp["Project Partner"]=request.form.getlist('partner')
                    tmp["Project Account"] = request.form.get('account')
                    tmp["Project Team Member"]=request.form.getlist('teammember')
                    tmp["Project Type"]=request.form.get('top')

            for tmp in metadata:
                if tmp["Project Name"] == projectname_dropdown:
                    tmp["Project Name"] = request.form.get('projname')
                    tmp["Project Lead"] = request.form.get('projlead')
                    #tmp["Project Start Date"]= request.form.get('startdate')
                    #tmp["RMT Project Name"]=request.form.get('rprojname')
                    tmp["Partner"]=request.form.getlist('partner')
                    tmp["Project Account"] = request.form.get('account')
                    tmp["Team Member"]=request.form.getlist('teammember')
                    tmp["Project Type"]=request.form.get('top')

            teammember_id = []
            for i in request.form.getlist('teammember'):
                mailt = i.split('<', 1)
                emailt = mailt[1][:-1]
                teammember_id.append(emailt)
            #print(teammember_id)

            proj_dict = {"Project Name": projectname_dropdown, "Project Sector": project_sec,
                            "Project Sub Sector": project_subsec, "Project Segment": project_seg,"Project Type": project_top, "Project Start Date": request.form.get('startdate'),
                            "RMT Project Name": request.form.get('rprojname'),"Project Partner": request.form.getlist('partner'),"Project Account": request.form.get('account'), "Project Lead": request.form.get('projlead'),
                            "Project Team Member": request.form.getlist('teammember')}
            flash('Project Updated Successfully')
            m1.send_mail_project_update(proj_dict,teammember_id)

        # f1 = 'Metadata_new.json'
        # lockfile1 = f1 + ".lock"
        # if os.path.exists(lockfile1):
        #     flash('File is in use by another user,please upload the file again after sometime.')
        #     return redirect(url_for('index'))
        #
        # f2 = 'admin.json'
        # lockfile2 = f2 + ".lock"
        # if os.path.exists(lockfile2):
        #     flash('File is in use by another user,please upload the file again after sometime.')
        #     return redirect(url_for('index'))
        #
        # f3 = 'projects.json'
        # lockfile3 = f3 + ".lock"
        # if os.path.exists(lockfile3):
        #     flash('File is in use by another user,please upload the file again after sometime.')
        #     return redirect(url_for('index'))
        #
        with FileLock('admin.json' + '.lock'):
            with open('admin.json', 'w') as f:
                json.dump(data, f, indent=4)

        with FileLock('projects.json' + '.lock'):
            with open('projects.json', 'w') as f:
                json.dump(projectData, f, indent=4)

        with FileLock('Metadata_new.json' + '.lock'):
            with open('Metadata_new.json','w') as f:
                json.dump(metadata, f, indent=4, sort_keys=False)

        return redirect(url_for('index'))

@app.route('/search')
def search():
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
    email_id = outlook.Accounts.Item(1).DisplayName
    validate_leads = m1.validate_access_leads()
    validate_leads = [x.lower() for x in validate_leads]
    validate_partners = m1.validate_access_partners()
    validate_partners = [x.lower() for x in validate_partners]
    validate_members = m1.validate_access_teammembers()
    validate_members = [x.lower() for x in validate_members]
    if not email_id.lower() in validate_members:
        if not email_id.lower() in validate_partners:
            if not email_id.lower() in validate_leads:
                return render_template('admin_auth_failure.html')

    sectors = m1.get_level1()
    subsectors = m1.get_level2()
    segments = m1.get_level3()
    partners = m1.get_partners()
    leads = m1.get_leads()
    #options = m1.get_level2()
    accounts = m1.get_accounts()
    #options = json.dumps(options, ensure_ascii=False)
    names = m1.get_names()
    datatypes = m1.get_datatype()
    years = m1.get_years()
    geographys = m1.get_geography()
    tops = m1.get_top()
    subsectors = json.dumps(subsectors, ensure_ascii=False)
    segments = json.dumps(segments, ensure_ascii=False)

    return render_template('search_v2.html', sectors=sectors,partners=partners, leads=leads,
                           accounts=accounts, projectNames=names, datatypes=datatypes,
                           years=years, geographys=geographys, tops=tops,subsectors=subsectors,segments=segments)

@app.route('/search_results', methods = ['GET','POST'])
def search_results():
    outcome=[]
    if request.method=='POST':
        Keyword = request.form.get('search2')
        Geography=request.form.getlist('geo')
        Sector = request.form.get('sec')
        Subsector = request.form.get('Subsec')
        Segments = request.form.get('seg')
        Year = request.form.getlist('year')
        Datatype= request.form.getlist('datatype')
        Project_name= request.form.get('projname')
        Partner_name=request.form.getlist('partner')
        Project_type= request.form.get('top')
        Project_lead=request.form.get('projlead')
        Project_account=request.form.get('account')

        if not Keyword:
            outcome = m1.filter_results(Geography, Sector, Subsector, Segments, Year,Datatype,Project_name,Partner_name,Project_type,Project_lead,Project_account)
            if outcome == []:
                flash('No results Found')
                return redirect(url_for('search'))
            print(outcome)

        elif Keyword and not any([Geography, Sector, Subsector, Segments, Year,Datatype,Project_name,Partner_name,Project_type,Project_lead,Project_account]):
            outcome = m1.get_results(Keyword, data)
            if outcome == []:
                flash('No results Found')
                return redirect(url_for('search'))
            print(outcome)

        elif (any(v is not '' or [] for v in [Geography, Sector, Subsector, Segments, Year,Datatype,Project_name,Partner_name,Project_type,Project_lead,Project_account]) and Keyword):
            filter_json = m1.filter_results(Geography, Sector, Subsector, Segments, Year,Datatype,Project_name,Partner_name,Project_type,Project_lead,Project_account)
            outcome=m1.get_results(Keyword,filter_json)
            if outcome == []:
                flash('No results Found')
                return redirect(url_for('search'))
            print(outcome)

    outcome = json.dumps(outcome,ensure_ascii = False)
    return render_template('results.html', outcome=outcome)

@app.route('/upload')
def upload():
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
    email_id = outlook.Accounts.Item(1).DisplayName
    #print(email_id,'email id')
    validate_leads = m1.validate_access_leads()
    validate_leads = [x.lower() for x in validate_leads]
    validate_partners = m1.validate_access_partners()
    validate_partners = [x.lower() for x in validate_partners]
    validate_members = m1.validate_access_teammembers()
    validate_members = [x.lower() for x in validate_members]

    if not email_id.lower() in validate_members:
        if not email_id.lower() in validate_partners:
            if not email_id.lower() in validate_leads:
                return render_template('admin_auth_failure.html')


    sectors = m1.get_level1()
    subsectors = m1.get_level2()
    segments = m1.get_level3()
    geographys = m1.get_geography()
    years = m1.get_years()
    datatypes = m1.get_datatype()
    projectnames = m1.get_names()
    teammembers=m1.get_team_members()
    subsectors = json.dumps(subsectors, ensure_ascii=False)
    segments = json.dumps(segments, ensure_ascii=False)
    projectDataJson = json.dumps(projectData, ensure_ascii=False)
    return render_template('upload_v2.html',sectors=sectors, projectNames=projectnames, datatypes=datatypes,years=years, geographys=geographys,projects=projectDataJson,
                           subsectors=subsectors,segments=segments,teammembers=teammembers)

@app.route('/upload_results', methods=['GET', 'POST'])
def upload_results():
    pythoncom.CoInitialize()
    outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
    user = outlook.Accounts.Item(1).DisplayName

    Geography = request.form.getlist('geo')
    Sector = request.form.get('sec')
    Subsector = request.form.get('Subsec')
    Segments = request.form.get('seg')
    Year = request.form.getlist('year')
    Filename = request.form.get('file')
    keyword = request.form.getlist('keyword')
    project_name=request.form.get('projname')
    comments= request.form.get('comments')
    datatype=request.form.getlist('datatype')
    team_member = request.form.getlist('teammember')

    #path = r'C:\Data\KM\KMtree' + '\\' + Sector + '\\' + Subsector + '\\' + Segments
    #path = r'\\Ingurusrfl010.ey.net\\010gru00044\\U\\UKI_CAS\\KMTool\\KMtree' + '\\' + Sector + '\\' + Subsector + '\\' + Segments
    path = r'C:\Data\KM\KMtree' # for local system
    #path = r'\\\\Ingurusrfl010.ey.net\\010gru00044\\U\\UKI_CAS\\KMTool\\KMtree'
    #path = r'\\Ingurusrfl010.ey.net\010gru00044\U\UKI_CAS\KMTool\KMtree'  # for remote directory
    UPLOAD_FOLDER = path
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.doc', '.docx', '.odt', '.pdf', '.txt', '.htm', '.html',
                                       '.js', '.xls', '.xlsx', '.csv', '.xml', '.zip','xlsm','.pptx','.yxmd','.pbix','.twb','.twbx','.ppt','.py','.PNG']

    if request.method == 'POST':
        f = request.files['file']
        filename = (secure_filename(f.filename))
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash("Invalid File Type")
            else:
                levels = [Sector, Subsector, Segments]
                levels = list(filter(None, levels))
                save_sub_dir = '\\'.join(x for x in levels if x not in ("*","", "-1"))
                save_dir = os.path.join(UPLOAD_FOLDER, save_sub_dir)

                if not os.path.exists(save_dir):
                    Path(save_dir).mkdir(parents=True, exist_ok=True)  # Create path if not exists

                #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                f.save(os.path.join(save_dir, filename))

                filepath = os.path.join(app.config['UPLOAD_FOLDER'],save_dir) # for passing to dict
                with open('Metadata_new.json') as json_file:
                    data = json.load(json_file, strict=False)
                    temp = data

                    Project_data = projectData["projects"]
                    for i in Project_data:
                        if i['Project Name'] == project_name:
                            Partner_name = i["Project Partner"]
                            Project_type = i["Project Type"]
                            Project_Lead = i["Project Lead"]
                            Project_account = i["Project Account"]

                    metadata_dict = {'Project Name': project_name, 'Datatype': datatype, 'Filename': filename,
                                     'Sector': Sector, 'Sub-Sector': Subsector, 'Segments': Segments,
                                     'Year': Year, 'Geography': Geography, 'Keyword': keyword,
                                     'Project Type': Project_type, 'Partner': Partner_name,
                                     'Project Lead': Project_Lead, 'Project Account': Project_account,
                                     'Team Member': team_member, 'Comments': comments, 'Uploaded By': user,
                                     'Filepath': filepath}

                    # print(metadata_dict)
                    temp.append(metadata_dict)
                    # comp_path=os.path.join(filepath,filename)

                    # m1.send_mail_upload(metadata_dict,comp_path)
                #m1.send_mail_upload(metadata_dict)

                filename = 'Metadata_new.json'
                lockfile = filename + ".lock"
                if os.path.exists(lockfile):
                    #print(os.path.exists(lockfile),'Printing lock file path')
                    flash('File is in use by another user,please upload the file again after sometime.')
                    return redirect(url_for('upload'))
                try:
                    with FileLock('Metadata_new.json' + '.lock'):
                        with open('Metadata_new.json', 'w') as f:
                            json.dump(data, f, indent=4, sort_keys=False)
                    flash('File Uploaded Successfully')
                    m1.send_mail_upload(metadata_dict)
                except:
                    flash('File is in use by another user,please upload the file again after sometime.')
                return redirect(url_for('upload'))

            return redirect(url_for('upload'))

@app.route('/download_file',methods=['GET'])
def file_download():
    try:

        filename= request.args.get('fname')
        filepath = request.args.get('fpath')

        #File_path = filepath +'\\'+ filename # for local system
        File_path = filepath[2:] + '\\\\' + filename  # for accessing from remote shared drive
        print(File_path,'Printing file path')
        return send_file(File_path, as_attachment=True, attachment_filename=os.path.basename(File_path))
    except:
        flash('File not found at the location')
        return redirect(url_for('search'))


@app.route('/contact_admin',methods=['GET'])
def contact_admin():
    try:
        pythoncom.CoInitialize()
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = 'EY_GDS_KMAdmin.GID@ey.net'
        mail.Subject = "KM Platform | Contact Admin"
        mail.Body = 'Please input queries/issues below'
        # mail.HTMLBody = 'Hi All,' + '<br>' + '<br>' + 'A new project id has been created for review,please find the details below:' + '<br>' + '<br>' + html
        mail.display(False)
        return redirect(url_for('home'))
    except:
        flash('Unable to contact KM Admin')
        return redirect(url_for('home'))

@app.route('/download_zip',methods=['POST'])
def download_zip():
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w',compression=zipfile.ZIP_DEFLATED) as zf:
        files = request.json.get('a')
        for individualFile in files:
            #zf.write(individualFile, individualFile.split("\\\\")[-1]) # for local system
            zf.write(individualFile[2:], individualFile.split("\\")[-1])
    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')

@app.route('/dashboard',methods=['GET','POST'])
def Dashboard():
    return render_template('Dashboard.html')
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port='8080')
    app.run(debug=True)