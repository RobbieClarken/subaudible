from pathlib import Path

import pytest
from scipy.io import wavfile

from subaudible.utils import audio_search


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
