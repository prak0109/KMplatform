import win32com.client as win32
import pythoncom,keyboard,json
import pandas as pd

with open('Metadata_new.json') as jsondata:
  data = json.load(jsondata)
  print(data)

df = pd.DataFrame(data)
print(df)

html = df.to_html(index=False)

# write html to file
#text_file = open("df.html", "w")
#text_file.write(html)
#text_file.close()

pythoncom.CoInitialize()
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'rupanshu.ahuja@gds.ey.com'
mail.Subject = "KM Platform | New Project has been Created"
#mail.Body = 'Testing for KM Platform'

mail.HTMLBody ='Hi,'+'<br>'+'<br>'+ 'A new project id has been created for review'+'<br>'+'<br>'+html
# To attach a file to the email (optional):
#attachment  = "Path to the attachment"
#mail.Attachments.Add(attachment)
mail.display(False)
#mail.Send
#keyboard.press_and_release('alt + s')
#keyboard.press_and_release('alt + s')

