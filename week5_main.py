from collections import deque

# import math
import matplotlib.animation as anm
import matplotlib.pyplot as plt
import numpy as np
import pyaudio


# 
# 音のコンスタレーションの取得
#
class AudioConstellation(object):

    # PyAudioとNumpyののフォーマット．同じデータ型にしておく
    FORMAT_PA = pyaudio.paFloat32
    FORMAT_NP = np.float32

    # CHUNK / RATE が UPDATE_M_SECONDを超えると
    # （他の処理の計算量によっては近づくと）
    # 取得しきれないデータが発生してうまくコンスタレーションが
    # 計算できなくなるので注意
    RATE = 44100  # サンプルレート
    CHUNK = 2048  # 一度の読み込みで入ってくる音のサンプル数
    UPDATE_M_SECOND = 5  # 更新頻度
    CHANNELS = 1

    HISTORY = 10  # 何サンプルデータを描画するか
    GRAPH_SIZE = 5  # コンスタレーションのグラフの軸幅

    def __init__(self, frequency):
        # 音声の読み込み用ストリームを開く
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=self.FORMAT_PA, channels=self.CHANNELS, rate=self.RATE,
            input=True, output=False, frames_per_buffer=self.CHUNK)
        self.lo_frequency = frequency
        self.phase_start_index = 0

    def audioinput(self):
        '''PyAudioのstreamから波形を読み込んでnp.arrayにして返す'''

        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        wave = np.frombuffer(data, dtype=self.FORMAT_NP)
        return wave
    
    def real_img_part(self, wave):
        lo_wave_sin = [
            np.sin(-2 * np.pi * self.lo_frequency * x / self.RATE)
            for x in range(self.phase_start_index, \
            self.phase_start_index + self.CHUNK)
        ]
        img = np.dot(lo_wave_sin, wave)
        lo_wave_cos = [
            np.cos(-2 * np.pi * self.lo_frequency * x / self.RATE)
            for x in range(self.phase_start_index, \
            self.phase_start_index + self.CHUNK)
        ]
        real = np.dot(lo_wave_cos, wave)
        self.phase_start_index = (self.phase_start_index + self.CHUNK) \
        % self.RATE
        return real, img

    def show(self):
        fig = plt.figure()
        # 描画データのプレースホルダ
        im, = plt.plot([0] * self.HISTORY, [0] * self.HISTORY, 'o')

        # グラフ幅の設定
        plt.xlim(-self.GRAPH_SIZE, self.GRAPH_SIZE)
        plt.ylim(-self.GRAPH_SIZE, self.GRAPH_SIZE)

        real_queue = deque([0] * self.HISTORY, maxlen=self.HISTORY)
        img_queue = deque([0] * self.HISTORY, maxlen=self.HISTORY)

        def update(frame):
            wave = self.audioinput()
            real, img = self.real_img_part(wave)
            real_queue.append(real)
            img_queue.append(img)

            # plotのプレースホルダに値を突っ込む
            im.set_data(real_queue, img_queue)

            # プレースホルダを返すことで高速な描画が可能
            return im

        ani = anm.FuncAnimation(fig, update, interval=self.UPDATE_M_SECOND)
        plt.show()


def main():
    ai = AudioConstellation(1000)
    ai.show()


if __name__ == '__main__':
    main()
