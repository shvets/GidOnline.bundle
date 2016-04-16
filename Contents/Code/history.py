KEY_HISTORY = 'history'
HISTORY_SIZE = 60

def push_to_history(**params):
    history = Data.LoadObject(KEY_HISTORY)

    if not history:
        history = {}

    history[params['path']] = {
        'path': params['path'],
        'title': params['title'],
        'thumb': params['thumb'],
        'season': params['season'],
        'episode': params['episode'],
        'time': Datetime.TimestampFromDatetime(Datetime.Now()),
    }

    # Trim old items
    if len(history) > HISTORY_SIZE:
        items = sorted(
            history.values(),
            key=lambda k: k['time'],
            reverse=True
        )[:HISTORY_SIZE]

        history = {}

        for item in items:
            history[item['path']] = item

    Data.SaveObject(KEY_HISTORY, history)

def load_history():
    return Data.LoadObject(KEY_HISTORY)