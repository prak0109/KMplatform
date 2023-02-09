from flask import Flask, render_template, request, url_for,flash,redirect
from werkzeug.utils import secure_filename
import os
from flask import jsonify,json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'


with open('admin.json') as json_file:
    dataAdmin= json.load(json_file)

with open('projects.json') as json_file:
    projectData= json.load(json_file)


def get_level1():
    level1=[""]
    for i in dataAdmin['sectors']:
        for k,v in i.items():
            level1.append(k)
    return level1

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

@app.route('/')
def index():
    sectors = get_level1()
    #partners = get_partners()
    #leads = get_leads()
    options = get_level2()
    #accounts = get_accounts()
    options = json.dumps(options, ensure_ascii=False)
    names = get_names()
    datatypes = get_datatype()
    years = get_years()
    geographys = get_geography()
    #tops = m1.get_top()

    return render_template('Upload_v1.html', sectors=sectors,options=options,projectNames=names, datatypes=datatypes,years=years, geographys=geographys)

@app.route('/test', methods = ['GET','POST'])
def test():
    Geography=request.form.get('geo')
    Sector = request.form.get('sec')
    Subsector = request.form.get('Subsec')
    Segments = request.form.get('seg')
    Year = request.form.getlist('year')
    filename = request.form.get('file')
    print(Year,'Printing Years')

    path = r'C:\Data\KM\KMtree' + '\\' + Sector + '\\' + Subsector + '\\' + Segments
    print(path)
    levels = [Sector,Subsector,Segments]

    UPLOAD_FOLDER = path
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.doc','.docx','.odt','.pdf','.txt','.htm','.html','.js','.xls','.xlsx','.csv','.xml','.zip']

    if request.method == 'POST':
        f = request.files['file']
        filename=(secure_filename(f.filename))
        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        save_sub_dir = '\\'.join(x for x in levels if x not in ("*", "", "-1"))
        print(save_sub_dir)
        path = r'C:\Data\KM\KMtree'
        UPLOAD_FOLDER = path
        save_dir = os.path.join(UPLOAD_FOLDER, save_sub_dir)
        print(save_dir)

        if not os.path.exists(save_dir):
            Path(save_dir).mkdir(parents=True, exist_ok=True)  # Create path if not exists
        f.save(os.path.join(save_dir, filename))

        flash('File uploaded successfully')
        print('File uploaded successfully')
        filepath =os.path.join(app.config['UPLOAD_FOLDER'])
        with open('Metadata_new.json') as json_file:
            data = json.load(json_file,strict=False)
            temp = data
            metadata_dict={'Filename':filename,'Geography':Geography,'Sector':Sector,'Sub-Sector':Subsector,'Segments':Segments,'Year':Year,'Filepath':filepath}
            print(metadata_dict)
            temp.append(metadata_dict)


        with open('Metadata_new.json', 'w') as f:
            json.dump(data, f, indent=4)

    return render_template('form_submitted.html')

if __name__ == '__main__':
    app.run(debug=True)



