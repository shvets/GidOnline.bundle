def push_to_history(item):
    history = Data.LoadObject(common.KEY_HISTORY)

    if not history:
        history = {}

    history[item['path']] = {
        'path': item['path'],
        'title': item['title'],
        'thumb': item['thumb'],
        'season': item['season'],
        'episode': item['episode'],
        'time': Datetime.TimestampFromDatetime(Datetime.Now()),
    }

    # Trim old items
    if len(history) > common.HISTORY_SIZE:
        items = sorted(
            history.values(),
            key=lambda k: k['time'],
            reverse=True
        )[:common.HISTORY_SIZE]

        history = {}

        for item in items:
            history[item['path']] = item

    Data.SaveObject(common.KEY_HISTORY, history)
