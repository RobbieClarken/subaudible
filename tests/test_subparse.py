from subaudible.subparse import parse_srt


def test_subparser():
    lines = [
        '1\n',
        '00:00:01,990 --> 00:00:03,060\n',
        'First line...\n',
        'Second line\n',
        '\n',
        '2\n',
        '00:00:03,060 --> 00:00:06,560\n',
        'Second caption\n',
    ]
    first_caption, second_caption = parse_srt(lines)
    assert first_caption['start'] == 1.99
    assert first_caption['end'] == 3.06
    assert first_caption['text'] == 'First line...\nSecond line'
    assert second_caption['text'] == 'Second caption'
