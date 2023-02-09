from flask import Flask, render_template, request, url_for,flash,redirect
from werkzeug.utils import secure_filename
import os
from flask import jsonify,json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

@app.route('/')
def index():
    return render_template('search_v1.html')

@app.route('/test', methods = ['GET','POST'])
def test():
    if request.method=='POST':
        Keyword = request.form.get('search2')
        Geography=request.form.getlist('geo')
        Sector = request.form.get('sec')
        Subsector = request.form.get('Subsec')
        Segments = request.form.get('seg')
        Year = request.form.getlist('year')
        print(request.form)

        with open('search_test.json') as json_file:
            data = json.load(json_file,strict=False)

    #print(list(filter(lambda x: x["Keyword"] == Keyword, data)))
        result=[]
        filters_lst=[Geography,Sector,Segments,Subsector,Year]
        #print(filters_lst)
        for i in data:
            for k, v in i.items():
                if v in filters_lst:
                    result.append(i)
                if isinstance(v,list):
                    for item in v:
                        match = any(item in sublist for sublist in filters_lst)
                        if match:
                            result.append(i)
                #else:
                    #flash('No results found!', 'warning')
                    #return redirect('/test')
        print(result)

    return render_template('form_submitted.html')

if __name__ == '__main__':
    app.run(debug=True)