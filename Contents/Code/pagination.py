import constants

def append_controls(oc, response, page, callback, **params):
    page = int(page)

    if 'pagination' in response:
        pagination = response['pagination']

        next_callback = Callback(callback, page=page+1, **params)
        previous_callback = Callback(callback, page=page-1, **params)

        if pagination['page'] and pagination['pages']:
            previous_pagination_message = '%d / %d' % (int(pagination['page']-1), int(pagination['pages']))
            next_pagination_message = '%d / %d' % (int(pagination['page']), int(pagination['pages']))
        else:
            previous_pagination_message = ''
            next_pagination_message = ''

        if not pagination['has_previous']:
            previous_message = ''
        else:
            previous_message = 'Back (' + previous_pagination_message + ')'

        if not pagination['has_next']:
            next_message = ''
        else:
            next_message = 'Next (' + next_pagination_message + ')'

        if pagination['has_previous']:
            oc.add(DirectoryObject(
                key=previous_callback,
                title=unicode(previous_message),
                thumb=R(constants.BACK_ICON)
            ))

        if pagination['has_next']:
            oc.add(DirectoryObject(
                key=next_callback,
                title=unicode(next_message),
                thumb=R(constants.NEXT_ICON)
            ))
