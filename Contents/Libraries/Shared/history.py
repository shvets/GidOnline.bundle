import library_bridge

Datetime = library_bridge.bridge.objects['Datetime']

KEY_HISTORY = 'history'
HISTORY_SIZE = 60

def push_to_history(Data, item):
    history = Data.LoadObject(KEY_HISTORY)

    if not history:
        history = {}

    id = item['id']

    hash = {}

    for key, value in item.iteritems():
        hash[key] = value

    hash['time'] = Datetime.TimestampFromDatetime(Datetime.Now())

    history[id] = hash

    # Trim old items
    if len(history) > HISTORY_SIZE:
        items = sorted(
            history.values(),
            key=lambda k: k['time'],
            reverse=True
        )[:HISTORY_SIZE]

        history = {}

        for it in items:
            history[it['id']] = it

    Data.SaveObject(KEY_HISTORY, history)

def load_history(Data):
    return Data.LoadObject(KEY_HISTORY)