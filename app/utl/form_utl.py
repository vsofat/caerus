import datetime


def strtodate(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d') if len(string) > 0 else None


def link_check(link):
    if link[:7] != 'http://' and link[:8] != 'https://':
        link = 'http://' + link
    return link


def link_parse(form):
    links = list()
    for key in form.keys():
        if "link" in key:
            link = form[key].strip()
            if len(link) > 0:
                link = link_check(link)
                links.append(link)
    return links


def create_opportunity_body(f):
    links = link_parse(f)
    grades = f['grades'].split(",")
    location = f["location"]
    location = location if len(location) > 0 else None
    return {'title': f['title'],
            'description': f['description'],
            'field': f['field'],
            'gender': f['gender'],
            'location': location,
            'startDate': strtodate(f['start']),
            'endDate': strtodate(f['end']),
            'deadline': strtodate(f['deadline']),
            'cost': f['cost'],
            'grades': grades,
            'links': links
            }


def create_scholarship_body(f):
    links = link_parse(f)
    return {
        'title': f['title'],
        'description': f['description'],
        'amount': f['amount'],
        'deadline': strtodate(f['deadline']),
        'eligibility': f['eligibility'],
        'links': links
    }


def create_resource_body(f):
    link = f['link'].strip()
    link = link_check(link)
    return {
        'title': f['title'],
        'description': f['description'],
        'link': link
    }


def create_preference_body(f, userid):
    body = {
            'userID': userid,
            'preferences': list()
        }
    maxCost = f['maximum-cost']
    if maxCost != '':
        body['preferences'].append(
            {'type': 'COST_PREFERENCE', 'value': float(maxCost)})
    for key in f.keys():
        if 'field' in key:
            body['preferences'].append(
                {'type': 'FIELD_PREFERENCE', 'value': f[key]})
        if 'grade' in key:
            body['preferences'].append(
                {'type': 'GRADE_PREFERENCE', 'value': f[key]})
        if 'gender' in key:
            body['preferences'].append(
                {'type': 'GENDER_PREFERENCE', 'value': f[key]})
    return body, maxCost == ''