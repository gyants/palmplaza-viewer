def sort_by(dict_list, key, descending=True):
    '''
    Sort data in a list by a key in the dictionaries 
    '''
    try:
        sorted_data = sorted(
            dict_list, key=lambda x: x[key], reverse=descending)
    except Exception as e:
        print(e)
    return sorted_data


def extract_field(dict_list, field_name):
    '''
    Extract values of a certain key from dictionaries
    '''
    field = []
    try:
        for i in dict_list:
            field.append(i[field_name])
    except Exception as e:
        print(e)
    return field


def extract_topics_id(dict_list):
    '''
    Extract the ID numbers of the topics from dictionaries
    '''
    ids = []
    for i in dict_list:
        fields = {'topic': '',
                  'id': ''}
        fields['topic'] = i['topic']
        cut_url = i['url'].split(
            'https://www.palm-plaza.com/CCforum/DCForumID4/')[1].split('.')[0]
        fields['id'] = cut_url
        ids.append(fields)

    return ids
