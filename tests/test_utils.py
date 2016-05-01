from pathlib import Path
from unittest.mock import patch, call

import pytest
from scipy.io import wavfile
import numpy as np

from subaudible.utils import (audio_search, caption_for_time_offset,
                              audio_sample_generator, hash_file,
                              convert_to_wav)


SAMPLE_RATE = 2000


def read_wav(filename):
    path = Path(__file__).parent / 'data' / filename
    return wavfile.read(str(path))[1]


@pytest.fixture(scope='module')
def source_audio():
    return read_wav('source.wav')


@pytest.fixture(scope='module')
def sample_audio():
    return read_wav('sample.wav')


def test_audio_search(source_audio, sample_audio):
    loc, strength = audio_search(source_audio, sample_audio, SAMPLE_RATE)
    assert int(loc) == 60


def test_strength_should_be_invariant_to_intensity(source_audio, sample_audio):
    weak_sample_audio = sample_audio * .5
    _, strength1 = audio_search(source_audio, sample_audio, SAMPLE_RATE)
    _, strength2 = audio_search(source_audio, weak_sample_audio, SAMPLE_RATE)
    assert strength1 == strength2


def test_caption_for_time_offset():
    captions = [
        {'start': 1, 'end': 3, 'text': 'First caption'},
        {'start': 5, 'end': 10, 'text': 'Second caption'},
    ]
    caption = caption_for_time_offset(captions, 5)
    assert caption['text'] == 'Second caption'


def test_caption_for_time_offset_returns_none_if_offset_is_inbetween():
    captions = [
        {'start': 1, 'end': 3, 'text': 'First caption'},
        {'start': 5, 'end': 10, 'text': 'Second caption'},
    ]
    caption = caption_for_time_offset(captions, 4)
    assert caption is None


@patch('subaudible.utils.sounddevice')
def test_audio_sample_generator(sounddevice_mock):
    sounddevice_mock.rec.return_value = np.array([[1], [2], [3]])
    gen = audio_sample_generator(duration=5, sample_rate=4000)
    sample = next(gen)
    assert np.array_equal(sample, np.array([1, 2, 3]))
    assert sounddevice_mock.rec.call_args == call(20000, samplerate=4000,
                                                  channels=1, dtype='int16')
    assert sounddevice_mock.wait.called is True


def test_hash_file():
    path = Path(__file__).parent / 'data' / 'source.aac'
    with path.open('rb') as file:
        hash_digest = hash_file(file)
    assert hash_digest == '2b8a282ae880dcbd4b2263d710f9d345'


@patch('subprocess.run')
def test_convert_to_wav(run_mock):
    in_path = Path(__file__).parent / 'data' / 'source.aac'
    filename = '2b8a282ae880dcbd4b2263d710f9d345_3000.wav'
    out_path = Path.home() / '.cache' / 'subaudible' / filename
    result = convert_to_wav(in_path, sample_rate=3000)
    assert run_mock.call_args == call([
        'ffmpeg', '-i', str(in_path), '-ac', '1', '-ar', '3000', str(out_path)
    ])
    assert result == out_path


@patch('subprocess.run')
def test_convert_to_wav_skips_conversion_if_file_exists(run_mock, monkeypatch):
    monkeypatch.setattr('pathlib.Path.exists', lambda *args, **kwargs: True)
    in_path = Path(__file__).parent / 'data' / 'source.aac'
    convert_to_wav(in_path)
    assert run_mock.called is False
