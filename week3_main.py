import pyaudio
import numpy as np
import math

CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
VOLUME = 0.1


class Note(object):
    """音の波形を作るクラス"""

    def __init__(self, length, scale):
        key, octave = scale[0], int(scale[-1])

        # 音階の処理
        scale_name = 'cxdxefxgxaxb'
        key_index = scale_name.find(key)
        frequence = 55 * 2**((octave - 1) + (key_index - 9) / 12.0)
        # #の音を出すための処理
        if scale[1] == "d":
            frequence *= 2**(1 / 12.0)

        self.frequence = frequence
        self.length = length

    def generate_wave(self, bpm, rate):
        """単音の波形を生成する関数"""

        step = (2 * math.pi) * self.frequence / rate  # 2πf*(1/rate)
        wave = np.sin(step * np.arange(self.length *
                                       (60 / bpm) * rate))  # sin(2πft)
        return wave


class SimpleMusic(object):
    """曲を生成し鳴らすクラス"""

    def __init__(self, bpm, rate):
        self.bpm = bpm
        self.rate = rate
        self.lst = []  # 楽譜を入れるリスト

    def append_note(self, lst):
        self.lst.extend(lst)

    def play(self):
        wave = []
        # クラス内の楽譜から波に変換
        for scale in self.lst:
            note = Note(scale[0], scale[1])
            wave.append(note.generate_wave(self.bpm, self.rate))
        wave = np.concatenate(wave, axis=0)
        wave *= VOLUME
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=self.rate,
                         output=True)
        stream.write(wave.astype(np.float32).tostring())


def main():
    musical_score = [[1, "c4"], [2, "d4"], [1, "e4"], [3, "f4"], [1, "g4"],
                     [2, "a4"], [1, "b4"]]
    music = SimpleMusic(120, 44100)
    music.append_note(musical_score)
    music.play()


if __name__ == '__main__':
    main()
