from hashlib import md5
from pathlib import Path
import subprocess

from scipy import signal
import numpy as np
import sounddevice


def audio_search(source, sample, sample_rate):
    """
    Locate an audio sample with a source audio track.

    Args:
        source (numpy array): Audio data that will be searched.
        sample (numpy array): Audio data to be located inside source.
        sample_rate (int): The sample rate in Hz of the audio data.

    Returns: Tuple of match time in seconds and strength of the correlation.

    """
    correlation = np.abs(signal.fftconvolve(source, sample[::-1]))
    match_idx = correlation.argmax()
    match_time = (match_idx - len(sample)) / sample_rate
    strength = correlation[match_idx] / np.sum(correlation)
    return match_time, strength


def caption_for_time_offset(captions, offset):
    """
    Returns the caption for a given time offset.

    Args:
        captions: A list of caption dicts.
        offset (float): Time offset.

    Returns: The caption dict where offset lies between start and end. If no
        caption fits these requirements, returns None.

    """
    return next((c for c in captions if c['start'] <= offset <= c['end']), None)


def audio_sample_generator(duration=10, sample_rate=2000):
    """
    Yields a series of audio recordings from the system microphone.

    Args:
        duration (float): Time in seconds for each recording.
        sample_rate (float): Sample rate in Hz.

    Yields:
        numpy array: 1-d numpy array of audio data as int16 samples.

    """
    samples = int(duration * sample_rate)
    while True:
        recording = sounddevice.rec(samples, samplerate=sample_rate,
                                    channels=1, dtype='int16')
        sounddevice.wait()
        yield recording[:, 0]


def hash_file(file):
    """
    Calculate the md5 hash digest of a file.

    Args:
        file: A file object.

    Returns:
        str: The hex digest.

    """
    hasher = md5()
    chunksize = 100 * 1024
    for chunk in iter(lambda: file.read(chunksize), b''):
        hasher.update(chunk)
    return hasher.hexdigest()


def convert_to_wav(path, sample_rate=2000):
    """
    Convert a video or audio file into a single channel wav audio file.
    The converted file is cached and if this function is called a second time
    with the same sample rate argument the conversion is skipped.

    Args:
        path (str or pathlib.Path): Path to the media file.
        sample_rate (int): Sample rate of output audio in Hz.

    Returns:
        pathlib.Path: Path to wav file.

    """
    path = Path(path)
    with path.open('rb') as file:
        hash_digest = hash_file(file)
    out_filename = '%s_%s.wav' % (hash_digest, sample_rate)
    out_path = Path.home() / '.cache' / 'subaudible' / out_filename
    if not out_path.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = ['ffmpeg', '-i', str(path), '-ac', '1',
               '-ar', str(sample_rate), str(out_path)]
        subprocess.run(cmd)
    return out_path
