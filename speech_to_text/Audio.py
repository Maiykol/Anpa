import numpy as np
import scipy.io.wavfile as wave
from scipy import signal
import matplotlib.pyplot as plt
import math


class Audio:
    """Represents audio data with its necessary attributes
    !!! AUDIO DATA SAMPLING RATE = 441000Hz !!!
    !!! ONLY TAKES SINGLE CHANNEL AUDIO ATM !!!"""
    # stft constants
    SEGMENTS_PER_SEC = 10
    OVERLAP_PERCENT = 0.75
    # makes a time length per data of 0.025s    <-- calculated by looking at spectrogram
    DATA_LEN_TIME_FRAME = 0.025


    # neural net input length in sec
    NN_INPUT_LEN_IN_SEC = 0.3



    def __init__(self, file):
        # init attribs and get data
        self.channels = None
        self.sample_rate = None
        self.data = self.__load_wav(file)
        self.nn_input = None

        # selecting best possible sound data from input
        #self.__select_best_data()

        # creating the spectrogram
        self.frequencies, self.time_stamps, self.stft = self.__create_spectrogram()

        # preparing neural net input
        self.__create_nn_input()


    def __load_wav(self, file):
        """Loads a .wav audio file to attributes"""
        # sampling rate --> samples per second, data --> sound data as np.array
        self.sample_rate, data = wave.read(file)

        return data


    def __select_best_data(self):
        """Selects best audio data from multiple channels"""
        #####################################################
        #                -- NOT IMPLEMENTED --              #
        #####################################################


    def __create_spectrogram(self):
        """Takes a 1-channel audio data input and creates the spectrogram"""
        # atm we are using default params for stft and not variables so they just get assigned here
        window = "hann"
        segment = self.sample_rate // self.SEGMENTS_PER_SEC         # 10 segments per sec
        overlap = int(segment * self.OVERLAP_PERCENT)               # 75% overlap based on [Allen, et. al. 1977]    --> 0.025sec per segment of speech

        # get 3D short time fourier transform
        frequencies, time_stamps, stft = signal.stft(self.data, self.sample_rate, window=window, nperseg=segment, noverlap=overlap)

        print("FREQ:\n", len(frequencies))
        print("TIME:\n", len(time_stamps))
        print("STFT\n", stft, len(stft), len(stft[0]))

        return frequencies, time_stamps, stft


    def show_spectrogram(self, cmap="coolwarm"):
        """Shows audio spectrogram as a plot"""
        plt.pcolormesh(self.time_stamps, self.frequencies, np.abs(self.stft), cmap=cmap)
        plt.ylabel("Frequency [Hz]")
        plt.xlabel("Time [sec]")
        plt.show()


    def __create_nn_input(self):
        """Slices the spectrogram data into chunks readable for a RNN"""
        # calculate chunk len by using constants
        # rounding needs to be done, otherwise float division failure
        stft_data_per_chunk = int(round(self.NN_INPUT_LEN_IN_SEC / self.DATA_LEN_TIME_FRAME, 0))
        # calculate array len by
        # rounding up the data is preference
        n_chunk = math.ceil(len(self.stft[0]) / stft_data_per_chunk)

        # creating array    --> data arrays per chunk * data per array * number of chunks
        self.nn_input = np.empty(stft_data_per_chunk * len(self.stft) * n_chunk, dtype="c16")

        # iterate data effectivly
        it = np.nditer(self.stft, order="F", flags=["f_index"])
        for data in it:
            self.nn_input[it.index] = data

        # shaping the array to fit NN
        self.nn_input.reshape(n_chunk, stft_data_per_chunk * len(self.stft))



audio = Audio("44100hz_16bit.wav")
audio.show_spectrogram()









