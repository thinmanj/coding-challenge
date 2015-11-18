import json
import argparse

from tweets_support import get_timestamp_hashtags_text, format_output_cleanup

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('tweets', help='Input tweets')
parser.add_argument('output', help='Output file')

args = parser.parse_args()

unicode_count = 0

with open(args.tweets, 'r') as tweets_source:
    with open(args.output, 'w') as output_file:
        for line in tweets_source:
            try:
                work_unit = get_timestamp_hashtags_text(json.loads(line))
            except KeyError:
                continue
            if work_unit["unicode_removed"]:
                unicode_count += 1
            output_file.write(format_output_cleanup(work_unit))
            output_file.write("\n")
        output_file.write("\n")
        output_file.write("%d tweets contained unicode." % unicode_count)
