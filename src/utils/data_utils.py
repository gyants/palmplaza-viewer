from datetime import datetime, timedelta

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

def time_ago(dt):
    delta = datetime.now() - dt
    if delta < timedelta(minutes=1):
        return 'just now'
    elif delta < timedelta(hours=1):
        minutes = delta.seconds // 60
        if minutes == 1:
            return '1 minute ago'
        else:
            return f'{minutes} minutes ago'
    elif delta < timedelta(days=1):
        hours = delta.seconds // 3600
        if hours == 1:
            return '1 hour ago'
        else:
            return f'{hours} hours ago'
    else:
        days = delta.days
        if days == 1:
            return '1 day ago'
        else:
            return f'{days} days ago'