import pyaudio
import numpy as np
import math

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
VOLUME = 0.1


def make_frequence(musical_scale):
    # 音階を入力するとその周波数を返してくれる関数
    # musical＿scale:音階

    scale_name = 'cxdxefxgxaxb'
    for i in range(12):
        if musical_scale[0] == scale_name[i]:
            base_frequence = 55 * math.pow(2.0, (i - 9) / 12.0)
    if musical_scale[1] == "d":
        base_frequence *= math.pow(2.0, (1 / 12.0))

    frequence = base_frequence * math.pow(2.0, int(musical_scale[-1]) - 1)

    return frequence


def tone(lst, BPM):
    '''generate tone wave
    周波数と長さの情報を入れた配列からsin波を生成する関数
    '''
    if len(lst) == 1:
        wave = np.zeros(int(lst[0] * (60 / BPM) * RATE))
        wave *= np.linspace(1.5, 0.3, len(wave))
        return wave

    else:
        # 和音だった場合それを足し合わせている
        wave = np.sin(0 * np.arange(float(lst[-1]) * (60 / BPM) * RATE))
        for scale in lst[:-1]:
            if len(scale) == 2 or len(scale) == 3:
                freq = make_frequence(scale)
                step = (2 * math.pi) * freq / RATE  # 2πf*(1/rate)
                single_wave = np.sin(
                    step * np.arange(float(lst[-1]) *
                                     (60 / BPM) * RATE))  # sin(2πft)
                wave += single_wave  # wavesにある各周波数のwaveを合計する
                wave *= np.linspace(1.5, 0.3, len(wave))
            else:
                wave += notes(scale, BPM)

        return wave


def notes(lst, BPM):
    '''楽譜のlistから連符をつくる関数
    notes : list of scale
    lst = [音階1,長さ1,音階2,長さ2,・・・]という構成
    '''
    wave = []
    for i in range(int(len(lst) / 2)):
        freq = make_frequence(lst[2 * i])
        step = (2 * math.pi) * freq / RATE  # 2πf*(1/rate)
        single_wave = np.sin(
            step * np.arange(float(lst[2 * i + 1]) *
                             (60 / BPM) * RATE))  # sin(2πft)
        wave.append(single_wave)
    wave = np.concatenate(wave, axis=0)

    return wave


def connect_song(song1, song2):
    # いくつかの曲を連続させる関数
    wave = np.append(song1, song2)
    return wave


def make_song(musical_score):
    # 楽譜の配列から曲を生成する関数
    BPM = musical_score[0]
    wave = []
    for i in range(len(musical_score) - 1):
        wave.append(tone(musical_score[i + 1], BPM))
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME
    return wave


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    '''
    楽譜は一つ目の要素がBPMであり、その後は楽譜となるようになっている。
    要素は配列となっており、同じ配列内の要素が同時に鳴らす音となっている。
    配列内の配列は連符を表している。
    '''
    # 楽譜（Amazing grace）
    Amazing_grace = [
        120, ["b4", "d5", "1"], ["b4", "g5", "2"],
        ["d5", ["b5", "0.5", "g5", "0.5"], "1"], ["d5", "b5", "2"],
        ["c5", "a5", "1"], ["b4", "g5", "2"], ["c5", "e5",
                                               "1"], ["b4", "d5", "2"]
    ]

    # 楽譜（Canon_in_D）
    Canon_in_D = [
        90,
        ["d5", "fd4", ["d3", "1", "fd3", "1"], "2"],
        ["cd5", "a4", ["a3", "1", "g3", "1"], "2"],
        ["b4", "d4", ["fd3", "1", "d3", "1"], "2"],
        ["a4", "fd4", ["fd3", "1", "e3", "1"], "2"],
        ["g4", "b3", ["d3", "1", "b2", "1"], "2"],
        ["fd4", "d4", ["d3", "1", "a2", "1"], "2"],
        ["g4", "b3", ["g2", "1", "b2", "1"], "2"],
        ["a4", "cd4", ["cd3", "1", "a2", "1"], "2"]
    ]

    wave1 = make_song(Amazing_grace)
    wave2 = make_song(Canon_in_D)
    wave = connect_song(wave1, wave2)

    stream.write(wave.astype(np.float32).tostring())
    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる


if __name__ == '__main__':
    main()
