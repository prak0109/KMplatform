from flask import Flask, render_template, request, url_for,flash,redirect
from werkzeug.utils import secure_filename
import os
from flask import jsonify,json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

@app.route('/')
def index():
    return render_template('Upload_v1.html')

@app.route('/test', methods = ['GET','POST'])
def test():
    Geography=request.form.get('geo')
    Sector = request.form.get('sec')
    Subsector = request.form.get('Subsec')
    Segments = request.form.get('seg')
    Year = request.form.getlist('year')
    filename = request.form.get('file')
    print(Year,'Printing Years')

    #lst = [Geography,Sector, Subsector, Segments,filename]
    #print(lst)
    #path = r'C:\Data\KM\KMtree'+'\\'+ Geography+'\\'+ Sector+ '\\'+Subsector+'\\'+ Segments
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

        #print(filename,'Printing File name')
        #print(os.path.join(app.config['UPLOAD_FOLDER']),'path...........')

        #with open('Metadata.json') as json_file:
        with open('Metadata_new.json') as json_file:
            data = json.load(json_file,strict=False)
            temp = data

            metadata_dict={'Filename':filename,'Geography':Geography,'Sector':Sector,'Sub-Sector':Subsector,'Segments':Segments,'Year':Year,'Filepath':filepath}

            print(metadata_dict)
            temp.append(metadata_dict)

        #with open('Metadata.json', 'w') as f:
        with open('Metadata_new.json', 'w') as f:
            json.dump(data, f, indent=4)

    else:
        return '',204

    return render_template('form_submitted.html')

if __name__ == '__main__':
    app.run(debug=True)



