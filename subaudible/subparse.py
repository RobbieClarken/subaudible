import re


def parse_srt(line_iter):
    """
    Parses SubRip text into caption dicts.

    Args:
        line_iter: An iterator that yields lines of a SubRip file.

    Yields:
        dict: Caption dicts with `start`, `end` and `text` keys.

    """
    line_iter = iter(line_iter)
    while True:
        next(line_iter)  # Skip counter
        start, end = parse_time_line(next(line_iter))
        text = '\n'.join(iter(line_iter.__next__, ''))
        yield {'start': start, 'end': end, 'text': text}


def parse_time_line(line):
    return (parse_time(time_str) for time_str in line.split('-->'))


def parse_time(time_str):
    time_str = time_str.replace(',', '.')
    match = re.search('(\d\d):(\d\d):(\d\d).(\d\d\d)', time_str)
    h, m, s, ms = (int(s) for s in match.groups())
    return 3600 * h + 60 * m + s + 1e-3 * ms
