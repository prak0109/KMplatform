from flask import Flask, render_template, request, url_for,flash,get_flashed_messages,redirect,send_file
from flask import jsonify,json
import model as m1
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import win32com.client as win32,pythoncom

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

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
    print(email_id)
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
    options=m1.get_level2()
    partners=m1.get_partners()
    leads=m1.get_leads()
    accounts=m1.get_accounts()
    team_members = m1.get_team_members()
    options=json.dumps(options,ensure_ascii = False)
    projectDataJson=json.dumps(projectData,ensure_ascii = False)
    return render_template('admin_v1.html', sectors=sectors, options=options,partners=partners,leads=leads,accounts=accounts,projects=projectDataJson,teammembers=team_members)

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

        if request.form.get('sub-category') == 'partners' and request.form.get('add_show') == 'add':
            Partner = data['partners']
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
            print(acc_name)

        elif request.form.get('category')=='industry' and request.form.get('add_show') == 'add':
            if request.form.get('subcateind')=='sector':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_input, industry_subsec_input,industry_seg_input)
            elif request.form.get('subcateind') == 'sub-sector':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_input,industry_seg_input)
            elif request.form.get('subcateind') == 'segment':
                data['sectors']=m1.add_industry(request.form.get('subcateind'), industry_sec_dropdown, industry_subsec_dropdown,industry_seg_input)


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
                ,"Project Name": project_projname, "Project Partner": project_partner,
                            "Project Account": project_account, "Project Lead": project_projlead}
            Project_data.append(project_dict)

            m1.send_mail_project(project_dict)

        elif request.form.get('category') == 'project' and request.form.get('add_show') == 'update':
            for tmp in projectData['projects']:
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

        flash('Added Successfully')

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
    partners = m1.get_partners()
    leads = m1.get_leads()
    options = m1.get_level2()
    accounts = m1.get_accounts()
    options = json.dumps(options, ensure_ascii=False)
    names = m1.get_names()
    datatypes = m1.get_datatype()
    years = m1.get_years()
    geographys = m1.get_geography()
    tops = m1.get_top()

    return render_template('search_v2.html', sectors=sectors, options=options, partners=partners, leads=leads,
                           accounts=accounts, projectNames=names, datatypes=datatypes,
                           years=years, geographys=geographys, tops=tops)

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

        if not Keyword:
            outcome = m1.filter_results(Geography, Sector, Subsector, Segments, Year)
            if outcome == []:
                flash('No results Found')
                return redirect(url_for('search'))
            print(outcome)

        elif Keyword and not any([Geography, Sector, Subsector, Segments, Year]):
            outcome = m1.get_results(Keyword, data)
            if outcome == []:
                flash('No results Found')
                return redirect(url_for('search'))
            print(outcome)

        elif (any(v is not '' or [] for v in [Geography, Sector, Subsector, Segments, Year]) and Keyword):
            filter_json = m1.filter_results(Geography, Sector, Subsector, Segments, Year)
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
    print(email_id,'email id')
    validate_leads = m1.validate_access_leads()
    validate_leads = [x.lower() for x in validate_leads]
    validate_partners = m1.validate_access_partners()
    validate_partners = [x.lower() for x in validate_partners]
    validate_members = m1.validate_access_teammembers()
    validate_members = [x.lower() for x in validate_members]

    print(validate_members)
    print(email_id.lower(),'lower case email')
    if not email_id.lower() in validate_members:
        if not email_id.lower() in validate_partners:
            if not email_id.lower() in validate_leads:
                return render_template('admin_auth_failure.html')


    sectors = m1.get_level1()
    options = m1.get_level2()
    options = json.dumps(options, ensure_ascii=False)
    geographys = m1.get_geography()
    years = m1.get_years()
    datatypes = m1.get_datatype()
    names = m1.get_names()
    return render_template('upload_v2.html',sectors=sectors, options=options, projectNames=names, datatypes=datatypes,years=years, geographys=geographys)
    #return render_template('upload_v2.html')

@app.route('/upload_results', methods=['GET', 'POST'])
def upload_results():
    Geography = request.form.getlist('geo')
    Sector = request.form.get('sec')
    Subsector = request.form.get('Subsec')
    Segments = request.form.get('seg')
    Year = request.form.getlist('year')
    Filename = request.form.get('file')
    keyword = request.form.getlist('keyword')
    project_name=request.form.get('projname')

    path = r'C:\Data\KM\KMtree' + '\\' + Sector + '\\' + Subsector + '\\' + Segments
    #print(path, 'path')

    UPLOAD_FOLDER = path
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.doc', '.docx', '.odt', '.pdf', '.txt', '.htm', '.html',
                                       '.js', '.xls', '.xlsx', '.csv', '.xml', '.zip','xlsm','.pptx','.yxmd','.pbix','.twb','.twbx']

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

                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                filepath = os.path.join(app.config['UPLOAD_FOLDER']) # for passing to dict
                with open('Metadata_new.json') as json_file:
                    data = json.load(json_file, strict=False)
                    temp = data
                    metadata_dict = {'Filename': filename, 'Geography': Geography, 'Sector': Sector, 'Sub-Sector': Subsector,
                                     'Segments': Segments, 'Year': Year, 'Filepath': filepath,'Keyword':keyword,'Project Name':project_name}
                    print(metadata_dict)
                    temp.append(metadata_dict)

                m1.send_mail_upload(metadata_dict)

                with open('Metadata_new.json', 'w') as f:
                    json.dump(data, f, indent=4)
                flash('File Uploaded Successfully')
                return redirect(url_for('upload'))

    return redirect(url_for('upload'))


@app.route('/download_file',methods=['GET'])
def file_download():
    filename= request.args.get('fname')
    filepath = request.args.get('fpath')
    File_path = filepath +'\\'+ filename
    return send_file(File_path, as_attachment=True, attachment_filename=os.path.basename(File_path))

if __name__ == '__main__':
    app.run(debug=True)