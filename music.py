import pyaudio
import numpy as np
import math

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
NOTE_FREQ = {  # 音の周波数
    "d6": 1174.659,  #レ
    "c6": 1046.502,  #ド
    "d#5": 622.254,  #レ＃
    "b5": 987.767,  #シ
    "a5": 880.000,  #ラ
    "g5": 783.991,  #ソ
    "f#5": 739.989,  #ファ＃
    "f5": 698.456,  #ファ
    "e5": 659.255,  #ミ
    "d5": 587.330,  #レ
    "c#5": 554.365,  #ド＃
    "c5": 523.251,  #ド
    "b4": 493.883,  #シ
    "g4": 391.995,  #ソ
}
BPM = 120
VOLUME = 0.1


def tone(lst):
    '''generate tone wave

    周波数と長さからsin波を作成する関数
    scale  : frequency [Hz]
    length : length (quater note is 1)
    '''
    if len(lst) == 1:
        wave = np.zeros(int(lst[0] * (60 / BPM) * RATE))
        return wave

    elif len(lst) == 2:
        step = (2 * math.pi) * NOTE_FREQ[lst[0]] / 44100  # 2πf*(1/rate)
        wave = np.sin(step * np.arange(float(lst[1]) *
                                       (60 / BPM) * RATE))  # sin(2πft)
        return wave

    else:
        step1 = (2 * math.pi) * NOTE_FREQ[lst[0]] / 44100  # 2πf*(1/rate)
        step2 = (2 * math.pi) * NOTE_FREQ[lst[1]] / 44100
        wave1 = np.sin(step1 * np.arange(float(lst[2]) *
                                         (60 / BPM) * RATE))  # sin(2πft)
        wave2 = np.sin(step2 * np.arange(float(lst[2]) * (60 / BPM) * RATE))
        wave = wave1 + wave2
        return wave


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    # 波形を作成する（星に願いを）
    wave = []
    lst = np.array([["b4", "d5", "1"], ["b4", "g5", "2"], ["d5", "b5", "0.5"],
                    ["d5", "g5", "0.5"], ["d5", "b5", "2"], ["c5", "a5", "1"],
                    ["b4", "g5", "2"], ["c5", "e5", "1"], ["b4", "d5", "2"]])

    for i in range(len(lst[:, 0])):
        wave.append(tone(lst[i,]))

    # 全部のsin波をつなげる
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
