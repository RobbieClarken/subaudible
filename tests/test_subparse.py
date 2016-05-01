from subaudible.subparse import parse_srt


def test_subparser():
    lines = [
        '1',
        '00:00:01,990 --> 00:00:03,060',
        'First line...',
        'Second line',
        '',
        '2',
        '00:00:03,060 --> 00:00:06,560',
        'Second caption',
    ]
    first_caption, second_caption = parse_srt(lines)
    assert first_caption['start'] == 1.99
    assert first_caption['end'] == 3.06
    assert first_caption['text'] == 'First line...\nSecond line'
    assert second_caption['text'] == 'Second caption'
