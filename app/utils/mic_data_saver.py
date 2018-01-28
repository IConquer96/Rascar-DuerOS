# -*- coding: utf-8 -*-
import Queue as queue
import threading
import wave
from pyaudio import PyAudio,paInt16

#define of params
NUM_SAMPLES = 2000
framerate = 16000
channels = 1
sampwidth = 2
#record time
TIME = 3

class MicDataSaver(object):
    '''
    录音数据保存工具类

    
    def __init__(self):
        # 保存录音数据文件名称
        self.file_name = 'mic_save_data.wav'
        self.queue = queue.Queue()
        self.wf = None

    def put(self, data):
        
        录音数据缓存
        :param data:录音pcm流
        :return:
        

        self.queue.put(data)

    def start(self):
        
        开始保存录音数据
        :return:
        
        self.wf = wave.open(self.file_name, 'wb')
        self.wf.setnchannels(1)
        self.wf.setsampwidth(2)
        self.wf.setframerate(16000)

        self.done = False
        thread = threading.Thread(target=self.__run)
        thread.daemon = True
        thread.start()

    def stop(self):
        
        停止录音数据保存
        :return:
        
        self.done = True

        self.wf.close()

    def __run(self):
        
        录音数据保存到文件中
        :return:
        
        while not self.done:
        chunk = self.queue.get()
        self.wf.writeframes(chunk)
    '''
    def  save_wave_file(filename,data):
        '''save the date to the wav file'''
        self.wf = wave.open(self.filename, 'wb')
        self.wf.setnchannels(channels)
        self.wf.setsampwidth(sampwidth)
        self.wf.setframerate(framerate)
        chunk = self.queue.get()
        wf.writeframes("".join(data))
        wf.close()  
    def record_wave(self):
        #open the input of wave
        pa = PyAudio()
        stream = pa.open(format = paInt16, channels = 1,
            rate = framerate, input = True,
            frames_per_buffer = NUM_SAMPLES)
        save_buffer = []
        count = 0
        while count<TIME*4:
            #read NUM_SAMPLES sampling data
            string_audio_data = stream.read(NUM_SAMPLES)
            save_buffer.append(string_audio_data)
            count += 1
            print '.'

        filename = file_name
        save_wave_file(filename, save_buffer)
        save_buffer = []
        print filename, "saved"
