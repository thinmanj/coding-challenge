from datetime import datetime
import pytz
from sets import Set


def _clean_escape(source):
    return source.replace('\n', ' ').replace('\t', ' ')


def detect_remove_unicode(source, remove=True):
    try:
        source.decode('ascii')
    except UnicodeEncodeError:
        return (True, _clean_escape(source.encode('ascii', 'ignore').decode('ascii'))) if remove else (True, source)
    else:
        return (False, _clean_escape(source))


def _get_text_cannonical(source, key='text'):
    return source[key].upper()


def get_timestamp_hashtags_text(source):
        text = detect_remove_unicode(source.get("text", ""))

        try:
            timestamp = source["created_at"]
            date_ts = datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        except KeyError:
            raise KeyError

        try:
            hashtags = source["entities"]["hashtags"]
            hashtags = map(_get_text_cannonical, hashtags)
        except KeyError:
            hashtags = []

        return {"unicode_removed": text[0], "clean_text": text[1], "timestamp": timestamp, "datetime": date_ts, "hashtags": hashtags, "id": source.get("id")}


def format_output_cleanup(source):
    return "{0[clean_text]} ({0[timestamp]})".format(source)


def calculate_average(source):
    tags_map = {}
    for work_unit in source:
        hashtags = work_unit['hashtags']
        size = len(hashtags) - 1
        if size > 0:
            for tag in hashtags:
                try:
                    tags_map[tag].update(hashtags)
                except KeyError:
                    tags_map[tag] = Set(hashtags)
    return (sum(map(lambda x: len(x) - 1, tags_map.values()))*1.0, len(tags_map))
