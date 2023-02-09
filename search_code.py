from fuzzywuzzy import fuzz
import json

with open('Metadata_new.json') as jsondata:
  data = json.load(jsondata)

  filename = [x['Filename'] for x in data]
  geography = [x['Geography'] for x in data]
  sector = [x['Sector'] for x in data]
  subsector = [x['Sub-Sector'] for x in data]
  segments = [x['Segments'] for x in data]
  Year = [x['Year'] for x in data]


def fuzzy_match(keyword,lst):
    l1=[]
    for i in lst:
        if fuzz.partial_ratio(keyword.lower(),str(i).lower())>=80:
            l1.append(i)
    #l2=list(set(l1))
    #print(l1)
    filter = []
    for ele in l1:
        if set(ele) not in [set(x) for x in filter]:
            filter.append(ele)
    #print(filter)
    return filter

def get_results():
    term = input('Please enter a keyword: ')
    get_filename=fuzzy_match(term,filename)
    get_sector= fuzzy_match(term,sector)
    get_segments=fuzzy_match(term,segments)
    get_year=fuzzy_match(term,Year)

    final_lst = []

    if len(get_filename) > 0:
        for i in get_filename:
            result = (list(filter(lambda x: x["Filename"] == i, data)))
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
                result = (list(filter(lambda x: x["Year"] == i, data)))
                final_lst.append(result)

    if len(get_segments) > 0:
        for i in get_segments:
            result = (list(filter(lambda x: x["Segments"] == i, data)))
            final_lst.append(result)

    if len(get_sector) > 0:
        for i in get_sector:
            result = (list(filter(lambda x: x["Sector"] == i, data)))
            final_lst.append(result)

    #print(final_lst)
    keyword_result=[]
    for lists in final_lst:
        for vals in lists:
            keyword_result.append(vals)

    print(keyword_result)
    return keyword_result


    #for k in final_lst:
       # print(k)

get_results()

#result =(list(filter(lambda x: x["Year"] == '2018', data)))
#print(result)
