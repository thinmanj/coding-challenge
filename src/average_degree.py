import json
import argparse
import datetime

from tweets_support import get_timestamp_hashtags_text, calculate_average

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('tweets', help='Input tweets')
parser.add_argument('output', help='Output file')

args = parser.parse_args()

delta_time = datetime.timedelta(seconds=60)
tweets_list = []

with open(args.tweets, 'r') as tweets_source:
    with open(args.output, 'w') as output_file:
        for line in tweets_source:
            try:
                work_unit = get_timestamp_hashtags_text(json.loads(line))
            except KeyError:
                continue
            tweets_list.append(work_unit)
            init_date = work_unit['datetime'] - delta_time
            tweets_list = filter(lambda x: x['datetime'] > init_date, tweets_list)
            average = calculate_average(tweets_list)
            try:
                average_value = average[0]/average[1]
            except ZeroDivisionError:
                average_value = 0

            output_file.write("{0:0.2f}".format(average_value))
            output_file.write("\n")
