# Audio Convolution and Analysis

This Python script performs audio convolution and analysis.

## Features

* **Convolution:**
    * Implements a custom convolution function (`benimKonvolusyon`)
    * Compares it with `numpy.convolve`.
* **Audio Recording:**
    * Records audio from the microphone using `sounddevice`.
    * Saves the recorded audio as a WAV file using `scipy.io.wavfile`.
* **Impulse Response:**
    * Generates an impulse response `h` based on a user-defined parameter `m`.
* **Convolution with Recorded Audio:**
    * Applies both the custom convolution and `numpy.convolve` to the recorded audio and the generated impulse response.
* **Audio Playback:**
    * Plays the convolved audio using `sounddevice`.
* **File Writing:**
    * Writes the convolved audio to a WAV file.

