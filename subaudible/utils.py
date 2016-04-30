from scipy import signal
import numpy as np


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