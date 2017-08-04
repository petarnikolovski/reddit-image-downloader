#!/usr/bin/python3


"""
Logging tools.
"""


from datetime import datetime


def write_log(post):
    """
    Write to a log file.
    """
    with open('download.log', 'a') as f:
        f.write(''.join(['-'*15, ' ', str(datetime.now()), ' ', '-'*15, '\n']))
        f.write(''.join(['Post URL -> ', post['url'], '\n']))
        f.write(''.join(['Post Comments -> ', post['link_to_comments'], '\n']))
        f.write(''.join(['Last HTTP status -> ', str(post['last_html_status']), '\n']))
        f.write('\n')
