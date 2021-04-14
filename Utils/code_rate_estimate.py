

# -*- coding:utf-8 -*-

from pywt import cwt
from scipy import signal
from numpy.fft import fft
import config as cfg
import random
import numpy as np
from scipy.signal import butter, lfilter


def code_rate_estimate(iq, a, fs, n_fft=cfg.N_FFT):
    """
    :param iq: original signal
    :param fs: sample rate
    :return:
    """
    iq = np.real(np.array(iq, dtype=complex))
    X = np.abs(cwt(iq, a, 'cgau8', len(iq))[0][0])

    max_points = signal.argrelextrema(X, np.greater)[0]
    min_points = signal.argrelextrema(-X, np.greater)[0]
    extreme_points = max_points.tolist() + min_points.tolist()
    extreme_points.sort()

    # 求极大极小值点
    # 基于极值点求微分
    diff_points = np.zeros(len(X))
    if extreme_points[0] == max_points[0]:
        diff_points[max_points[0]] = X[max_points[0]]
    else:
        diff_points[min_points[0]] = -X[min_points[0]]

    for i in range(1, len(extreme_points)):
        diff_points[extreme_points[i]] = X[extreme_points[i]] - X[extreme_points[i - 1]]

    # 对微分结果进行fft变换
    diff_fft = np.abs(fft(diff_points, n_fft)[:n_fft // 2])
    # diff_fft -= np.mean(diff_fft)
    # diff_fft_hilbert = np.abs(hilbert(diff_fft))
    #
    # plt.plot(diff_fft)
    # plt.plot(diff_fft_hilbert)
    # plt.show()

    # 求取第一个极大峰值
    p_points = signal.argrelextrema(diff_fft, np.greater, order=cfg.MAX_ORDER)[0]
    K = p_points[0]

    # 查找对应位置序号
    # K = np.argmax(diff_fft)

    # 计算波特率
    baud_rate = K * fs / n_fft

    return baud_rate


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

    N = 40000
    bit_rate = 40
    fc = 40
    fs = 1000

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
    t_bit = np.linspace(0, 1 / bit_rate, int(1 / bit_rate * fs), endpoint=False)
    for i in range(0, N // 2):
        I_carrier.extend((I[i] * np.cos(2 * np.pi * fc * t_bit)).tolist())
        Q_carrier.extend((Q[i] * np.cos(2 * np.pi * fc * t_bit + np.pi / 2)).tolist())

    # 生成复信号并进行频谱搬移
    n = len(I_carrier)
    sigs = []
    t = np.linspace(0, n // fs, n, endpoint=False)
    for i in range(n):
        sig = complex(I_carrier[i], Q_carrier[i])
        # sig *= np.exp(complex(0, 2 * np.pi * fc * t[i]))
        sigs.append(sig)

    # sigs_filtered = butter_lowpass_filter(sigs, fc, fs)

    code_rate = code_rate_estimate(sigs, 20, fs, 50000)
    print(code_rate)

    # fs = 900000
    # a = 30
    # DIR = 'D:/36Data/IQ_Data/2020-06-18/0x24022420_2020-06-18-00_01/'
    # # DIR = 'D:/Program/PycharmProject/IntermediateFreq/test/'
    #
    # code_rates = []
    # for file in os.listdir(DIR):
    #
    #     print(file)
    #
    #     file_path = DIR + file
    #     iq = np.load(file_path)
    #     I = iq[0]
    #     Q = iq[1]
    #
    #     sig = []
    #     for i in range(len(I)):
    #         sig.append(complex(I[i], Q[i]))
    #
    #     code_rate = code_rate_estimate(sig, a, fs)
    #     code_rates.append(code_rate)
    #     print(code_rate)
    #
    # df = pd.DataFrame({'code_rates': code_rates})
    # df.to_csv('test_fs_3.csv', index=False)



















































































