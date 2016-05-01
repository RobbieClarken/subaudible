from scipy import signal
import numpy as np
import sounddevice


def audio_search(source, sample, sample_rate):
    """
    Locate an audio sample with a source audio track.

    Args:
        source (numpy array): Audio data that will be searched
        sample (numpy array): Audio data to be located inside source
        sample_rate (int): The sample rate in Hz of the audio data

    Returns: Tuple of match time in seconds and strength of the correlation

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
