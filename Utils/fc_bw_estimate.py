
# -*- coding:utf-8 -*-

from numpy.fft import fft
import config as cfg
import random
import numpy as np
from scipy.signal import butter, lfilter


def fc_bw_estimate(iq, fs, n_fft=cfg.N_FFT):
    """
    :param iq: original signal
    :param fs: sample rate
    :return:
    """
    iq = np.real(np.array(iq, dtype=complex))

    fs = int(fs)
    fs -= fs % 2
    # n_fft = fs // cfg.FS_NFFT

    X = np.abs(fft(iq, n_fft))
    X2 = X**2 / n_fft
    X2_fft = X2[:n_fft // 2]

    power_spectrum = 10 * np.log10(X2_fft)

    # 载频估计
    argmax_power_spectrum = np.argmax(power_spectrum)
    fc = argmax_power_spectrum * fs / n_fft

    fc_mean = np.sum(X2_fft * np.linspace(0, n_fft // 2, n_fft // 2, endpoint=False)) / np.sum(X2_fft)
    bw = np.sum(X2_fft * np.abs(np.linspace(0, n_fft // 2, n_fft // 2, endpoint=False) - argmax_power_spectrum)) / np.sum(X2_fft)
    band_width = bw * fs / n_fft

    # 带宽边界值估计
    # kl = kr = argmax_power_spectrum
    # while (power_spectrum_filt[kl] > power_spectrum_filt[argmax_power_spectrum] - 3) and (kl >= 0):
    #     kl -= 1
    # while (power_spectrum_filt[kr] > power_spectrum_filt[argmax_power_spectrum] - 3) and (kr < len(power_spectrum_filt)):
    #     kr += 1
    # deltawidth = kr - kl
    # bw = deltawidth * fs / n_fft

    # plt.show()

    return [fc, band_width]


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y  # Filter requirements.

if __name__ == '__main__':

    # fs = 1024
    # num_fft = 2048
    #
    # t = np.arange(0, 2, 1 / fs)
    # f0 = 100
    # f1 = 200
    # # x = np.cos(2*np.pi*f0*t) + 3*np.cos(2*np.pi*f1*t) + np.random.randn(t.size)
    # x = np.cos(2 * np.pi * f0 * t) + np.random.randn(t.size)

    N = 2000
    bit_rate = 10000
    fc = 4000
    fs = 1000000

    # 生成比特流
    bit_stream = []
    for i in range(0, N):
        bit = random.randint(0, 1)
        bit = 2 * bit - 1
        bit_stream.append(bit)

    # 生成IQ两路数据
    I = []
    Q = []
    for i in range(0, N):
        if i % 2 == 0:
            I.append(bit_stream[i])
        else:
            Q.append(bit_stream[i])

    # 生成基带信号（加采样）
    bit_data = []
    for i in range(0, N):
        bit_data.append([bit_stream[i]] * (fs // bit_rate))
    I_data = []
    Q_data = []
    for i in range(0, N // 2):
        I_data.append([I[i]] * (2 * fs // bit_rate))
        Q_data.append([Q[i]] * (2 * fs // bit_rate))

    # 生成中频信号（加载波）
    I_carrier = []
    Q_carrier = []
    t_bit = np.linspace(0, 2 // bit_rate, 2 // bit_rate * fs, endpoint=False)
    for i in range(0, N // 2):
        I_carrier.extend((I[i] * np.cos(2 * np.pi * fc * t_bit)).tolist())
        Q_carrier.extend((Q[i] * np.cos(2 * np.pi * fc * t_bit + np.pi / 2)).tolist())

    # 生成复信号
    # sig = []
    # for i in range(len(I_carrier)):
    #     sig.append(complex(I_carrier[i], Q_carrier[i]))

    # 生成复信号并进行频谱搬移
    n = len(I_carrier)
    sigs = []
    t = np.linspace(0, n // fs, n, endpoint=False)
    for i in range(n):
        sig = complex(I_carrier[i], Q_carrier[i])
        sig *= np.exp(complex(0, 2 * np.pi * fc * 10 * t[i]))
        sigs.append(sig)

    fc_bw = fc_bw_estimate(sigs, fs, n_fft=2000)
    fc = fc_bw[0]
    bw = fc_bw[1]
    print(fc, bw)















