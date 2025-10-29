import pyaudio,wave,random
import wave
import numpy as np
from scipy import fftpack
import os,time
from datetime import datetime
import os,sys
import librosa
import soundfile as sf



SAVE_FILE = "./dog_agent/myrec.wav"

# 录音参数 Recording parameters
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# RECORD_SECONDS = 600  # 最大录音时长 Maximum recording duration
# START_THRESHOLD = 100000  # 开始录音的音量阈值 Volume threshold for starting recording
# END_THRESHOLD = 40000  # 停止录音的音量阈值 Volume threshold for stopping recording
# ENDLAST = 30


# start_threshold = 60000
# end_threshold = 40000
# endlast = 10


# 关键词检测参数 Keyword detection parameters
PLAY_COMMAND = "aplay"  

def calculate_volume(data):
    rt_data = np.frombuffer(data, dtype=np.int16)
    fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
    fft_data = np.abs(fft_temp_data)[0: fft_temp_data.size // 2 + 1]
    return sum(fft_data) // len(fft_data)


# def start_recording(): 
#     p = pyaudio.PyAudio()
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     print("wait recording...")
#     frames = []
#     start_recording_flag = False
#     end_data_list = [0] * ENDLAST
#     pre_record_frames = []  # 预录音缓冲区
#     pre_record_length = int(RATE / CHUNK * 1)  # 预录音 1 秒
#     silence_duration = 0  # 静音持续时间
#     max_silence_duration = int(RATE / CHUNK * 4)  # 最大允许静音时长（4 秒）
#     recording_start_time = None  # 录音开始时间
#     no_sound_timeout = int(RATE / CHUNK * 6)  # 无声音超时（6秒）
#     no_sound_counter = 0  # 无声音计数器
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         volume = calculate_volume(data)
        
#         rt_data = np.frombuffer(data, dtype=np.int16)
#         fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
#         fft_data = np.abs(fft_temp_data)[0:fft_temp_data.size // 2 + 1]
#         vol = sum(fft_data) // len(fft_data)
#         if not start_recording_flag:
#             pre_record_frames.append(data)  # 保存到预录音缓冲区
#             if len(pre_record_frames) > pre_record_length:
#                 pre_record_frames.pop(0)  # 保持缓冲区大小
#             if volume > START_THRESHOLD:
#                 print("detected voice, start recording...")
#                 start_recording_flag = True
#                 recording_start_time = time.time()  # 记录录音开始时间
#                 frames.extend(pre_record_frames)  # 将预录音数据加入正式录音
#                 frames.append(data)
#                 no_sound_counter = 0  # 重置无声音计数器
#             else:
#                 no_sound_counter += 1
#                 # 如果6秒内没有检测到声音，结束录音
#                 if no_sound_counter >= no_sound_timeout:
#                     print("No sound detected for 6 seconds, ending recording")
#                     break
#         else:
#             end_data_list.pop(0)
#             end_data_list.append(volume)
#             frames.append(data)

#             # 检测静音
#             if volume < END_THRESHOLD:
#                 silence_duration += 1
#             else:
#                 silence_duration = 0

#             # 如果录音时间超过 2 秒且没有检测到有效声音，结束录音
#             if recording_start_time and (time.time() - recording_start_time) >= 2:
#                 if max(end_data_list) < START_THRESHOLD:
#                     print("No valid sound detected within 2 seconds, end recording")
#                     break

#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     wf = wave.open(SAVE_FILE, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()
#     print(f"The recording has been saved as: {SAVE_FILE}")


import threading
import time
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from mic_serial import SerialPort

#port_name = "/dev/ttyUSB0" #串口号,根据实际检测的进行更改
port_name = "/dev/myspeech"
serial_port = SerialPort(port=port_name, baudrate=115200)
serial_port.open()

receive_thread = threading.Thread(target=serial_port.receive_data)
receive_thread.daemon = True
receive_thread.start()

def detect_keyword():
    global serial_port
    serial_port.clean_asr()
    print("Waiting for keyword...")
    while True:
        if serial_port.xiaoya == True:
            now = datetime.now().strftime("%d.%b %Y %H:%M:%S")
            print(f"Keyword detected: {now}")
            serial_port.clean_asr()
            os.system(f"{PLAY_COMMAND} ./ding.wav")
            return True

def spectral_subtraction(y, sr, n_fft=2048, hop_length=512, noise_frames=10):
    """
    谱减法降噪 Spectral subtraction denoising
    y:输入的音频信号 Input audio signal
    sr:采样率 sampling rate
    
    n_fft:FFT窗口大小，通常为2的幂次(Fast Fourier Transform Window Size,Usually a power of 2)  
    作用:决定频率分辨率精细程度，较大的值提供更高的频率分辨率但较低的时间分辨率 Function: Determine the precision of frequency resolution, with larger values providing higher frequency resolution but lower time resolution
    计算公式：频率分辨率 = 采样率 / n_fft Calculation formula: Frequency resolution=Sampling rate/n_fft
    
    hop_length:帧移大小 (Frame Shift Size) 
    作用：连续帧之间的采样点数，决定时间分辨率的精细程度 Function: The number of sampling points between consecutive frames determines the level of temporal resolution refinement
    与n_fft的关系:通常设置为n_fft的1/4或1/2 (Relationship with N_FFT: usually set to 1/4 or 1/2 of N_FFT)
    计算公式: 帧持续时间 = hop_length / sr  (Calculation formula: Frame duration=hop_1ength/sr)
    
    noise_frames:用于噪声估计的帧数 Noise_frames: frames used for noise estimation
    噪声持续时间 = noise_frames × (hop_length / sr) 此处为:320ms (Noise duration=noise_frames × (hop_1ength/sr), here it is 320ms)
    
    """
    # STFT 快速傅里叶变换
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    magnitude, phase = librosa.magphase(stft)
    
    # 估计噪声谱（使用前几帧作为噪声参考） Estimate noise spectrum (using the first few frames as noise reference)
    noise_mag = np.mean(np.abs(stft[:, :noise_frames]), axis=1, keepdims=True)
    
    # 谱减法 Spectral subtraction
    magnitude_sub = np.maximum(magnitude - noise_mag, 0)
    
    # 重建音频 rebuild  audio
    stft_clean = magnitude_sub * phase
    y_clean = librosa.istft(stft_clean, hop_length=hop_length)
    
    return y_clean

def amplify_audio_librosa(input_file, output_file, gain_factor=5.0):
    
    y1, sr = librosa.load(input_file, sr=None)
    y = spectral_subtraction(y1, sr)
    
    amplified = y * gain_factor
    amplified = np.clip(amplified, -1.0, 1.0)
    sf.write(output_file, amplified, sr)
    
    #print(f"音频已放大 {gain_factor}倍 并保存至 {output_file}")

quitmark = 0
automark = True 
def start_recording(timel = 3,save_file=SAVE_FILE):
    global automark,quitmark
    start_threshold = 3000 #6000
    end_threshold = 1500 #3000
    endlast = 15
    max_record_time = 10 
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    WAVE_OUTPUT_FILENAME = save_file 

    
    if automark:
        p = pyaudio.PyAudio()       
        stream_a = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        start_luyin = False
        break_luyin = False
        data_list =[0]*endlast
        sum_vol=0
        start_time = None

        while not break_luyin:
            if not automark or quitmark == 1:
                break

            data = stream_a.read(CHUNK, exception_on_overflow=False)
            rt_data = np.frombuffer(data, dtype=np.int16)
            fft_temp_data = fftpack.fft(rt_data, rt_data.size, overwrite_x=True)
            fft_data = np.abs(fft_temp_data)[0 : fft_temp_data.size // 2 + 1]
            vol = sum(fft_data) // len(fft_data)
            
            data_list.pop(0)
            data_list.append(vol)
            
            print(f"Current volume: {vol}, boot threshold: {start_threshold}, End threshold: {end_threshold}")
            
            if vol > start_threshold:
                sum_vol += 1
                if sum_vol == 1:
                    print("start recording")
                    start_luyin = True
                    start_time = time.time()
            
            if start_luyin:
                elapsed_time = time.time() - start_time
                
                if all(float(i) < end_threshold for i in data_list) or elapsed_time > max_record_time:
                    print("Recording ends: Low volume or recording time exceeds the limit")
                    break_luyin = True
                    frames = frames[:-5]
            
            if start_luyin:
                frames.append(data)
            print(start_threshold, vol)
        print("auto end")


    if quitmark==0:
        try:
            stream_a.stop_stream()
            stream_a.close()
        except:
            pass
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"The recording has been saved as: {WAVE_OUTPUT_FILENAME}")

        amplify_audio_librosa("./dog_agent/myrec.wav", "./dog_agent/myrec.wav",gain_factor=5.0) #放大它 Enlarge it

    
