import win32com.client as win32,pythoncom
# outlook = win32.Dispatch('outlook.application')
# for accounts in outlook.Session.Accounts:
#     print('Available email accounts: %s'%(accounts))
#
# import getpass
# user = getpass.getuser()
# print(user)


pythoncom.CoInitialize()
outlook = win32.Dispatch('outlook.application').GetNameSpace("MAPI")
username = outlook.Accounts.Item(1).DisplayName
print(username.lower())

project_leads = ["Mitali.Chopra@gds.ey.com", "varun.arora@gds.ey.com",
                     "prakhar.rastogi1@gds.ey.com"]

project_leads = [x.lower() for x in project_leads]

print(project_leads)

'''from flask import Flask, render_template,redirect
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'


with open('Access.json') as json_file:
    User= json.load(json_file)
    print(User)

@app.route('/',methods=['GET', 'POST'])
def validate_access(Level1,Level2,Level3):

    project_leads = ["Mitali.Chopra@gds.ey.com", "varun.arora@gds.ey.com",
                     "prakhar.rastogi1@gds.ey.com"]
    partners = ["Lucy.Tang1@parthenon.ey.com", "rupanshu.ahuja@gds.ey.com"]

    email_id = input("Enter Email id: ")
    if email_id in project_leads:
        Level1,Level2,Level3=True

    elif email_id in partners:
        Level1=True
        Level2=True
        Level3=False


    email_id = input("Enter Email id: ")

    if email_id in (project_leads and partners):
        return render_template('add_remove.html')
    else:
        return render_template('access_denied.html')

if __name__ == '__main__':
    app.run(debug=True)'''





