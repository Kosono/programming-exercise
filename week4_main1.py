import pyaudio
import numpy as np
import math


class Note(object):
    """音の波形を作るクラス"""

    def __init__(self, scale, length=1):
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

    volume = 0.5

    def __init__(self, bpm, rate=44100):
        self.bpm = bpm
        self.rate = rate
        self.lst = []  # 楽譜を入れるリスト

    def append_note(self, note):
        self.lst.append(note)

    def play(self):
        waves = [note.generate_wave(self.bpm, self.rate) for note in self.lst]
        # クラス内の楽譜から波に変換
        wave = np.concatenate(waves, axis=0)
        wave *= self.__class__.volume
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=1, rate=self.rate,
                         output=True)
        stream.write(wave.astype(np.float32).tostring())

    @classmethod
    def c_b_music(cls, bpm):
        music = cls(bpm=bpm)
        music.append_note(Note("c4"))
        music.append_note(Note("d4", 2))
        music.append_note(Note("e4"))
        music.append_note(Note("f4", 3))
        music.append_note(Note("g4"))
        music.append_note(Note("a4", 2))
        music.append_note(Note("b4"))
        return music


def main():
    music = SimpleMusic.c_b_music(120)
    music.play()
    SimpleMusic.volume = 1
    music.play()


if __name__ == '__main__':
    main()
