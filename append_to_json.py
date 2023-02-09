
import json

with open('data.json') as json_file:
    data = json.load(json_file)

    temp = data['emp_details']

    # python object to be appended
    y = {"emp_name": 'Nikhil',
         "email": "nikhil@geeksforgeeks.org",
         "job_profile": "Full Time"
         }

    # appending data to emp_details
    temp.append(y)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

#write_json(data)
