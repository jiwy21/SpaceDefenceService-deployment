
# -*- coding:utf-8 -*-

import numpy as np
import config as cfg
import random


def mdl(l, b, n, k):
    """
    :param l:
    :param b:
    :param n:
    :param k:
    :return: 返回mdl函数值
    """

    back = 1/2 * l * (2 * n - l) * np.log(k)

    sum_bi = 0
    for i in range(l, n):
        sum_bi += b[i]

    sum_logbi = 0
    for i in range(l, n):
        sum_logbi += np.log(b[i])

    front = (n - l) * k * np.log(sum_bi / (n - l)) - k * sum_logbi

    return front + back


def argmin_mdl(b, n, k):
    """
    :param b:
    :param n:
    :param k:
    :return: 返回使得mdl最小的l值
    """
    l = 0
    val = mdl(0, b, n, k)

    for i in range(1, n):
        val_new = mdl(i, b, n, k)
        if val_new < val:
            l = i
            val = val_new

    return l


def snr_estimate(signal, n=cfg.N_SNR, k=cfg.K_SNR):
    """
    :param signal: I + jQ(长度至少n*k)
    :param n: length of each signal
    :param k: number of signals
    :return: snr(dB)
    """

    rxx = np.zeros((n, n), dtype=complex)
    for i in range(k):
        r = np.array(signal[i*n:i*n+n])
        rxx += np.multiply(r.reshape(n, 1), r.reshape(1, n).conj())

    rxx /= k
    eigvals, eigvecs = np.linalg.eig(rxx)
    b = eigvals.real.tolist()
    b.sort(reverse=True)

    n_short = 0
    for i in range(n):
        if b[i] >= cfg.EIG_THRESHOLD:
            n_short += 1
        else:
            break

    p = argmin_mdl(b, n_short, k)

    # 噪声能量
    sigma2 = 0
    for i in range(p, n_short):
        sigma2 += b[i]
    sigma2 /= (n_short - p)
    pw = n_short * sigma2

    # 信号能量
    ps = 0
    for i in range(0, p):
        ps += (b[i] - sigma2)

    # 信噪比估计
    snr_ratio = ps / pw
    snr_dB = 10 * np.log(snr_ratio) / np.log(10)

    return snr_dB


def awgn(x, snr, seed=7):
    '''
    加入高斯白噪声 Additive White Gaussian Noise
    :param x: 原始信号
    :param snr: 信噪比
    :return: 加入噪声后的信号
    '''
    np.random.seed(seed)  # 设置随机种子
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(x ** 2) / len(x)
    npower = xpower / snr
    noise = np.random.randn(len(x)) * np.sqrt(npower)
    return x + noise


def sin_wave(A, f, fs, phi, t):
    '''
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params phi:  相位
    :params t:    时间长度
    '''
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1/fs
    n = t / Ts
    n = np.arange(n)
    y = A*np.sin(2*np.pi*f*n*Ts + phi*(np.pi/180))
    return y


if __name__ == '__main__':

    # f = 50
    # t = 1
    # fs = 500000
    # Ts = 1 / fs
    # n = np.arange(t / Ts)
    # y = np.sin(2 * np.pi * f * n * Ts)

    N = 50
    bit_rate = 1
    fc = 2
    fs = 100

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

    # 加入高斯白噪声(dB)
    snr = 40
    I_noise = awgn(np.array(I_carrier), snr)
    Q_noise = awgn(np.array(Q_carrier), snr + 100)

    # plt.plot(y_noise)
    # plt.show()

    # 生成复信号
    sig = []
    for i in range(len(I_noise)):
        sig.append(complex(I_noise[i], Q_noise[i]))

    print(snr_estimate(sig))

























