import pyaudio
import wave
import math
import time
import struct
from kaldi.asr import NnetLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.nnet3 import NnetSimpleComputationOptions
from kaldi.util.table import SequentialMatrixReader, CompactLatticeWriter
from train_chatterbot import chatbot
import os

# LISTENING PART

# listen's if someone's speaking


def listen():

    # record configuration

    # samples
    chunk = 1024

    # bits per sample
    sample_format = pyaudio.paInt16

    # samples per sec
    fs = 44100

    channels = 1

    # RMS threshold for silence detection
    threshold = 5

    # time limit for listening
    timeout = 10

    # per how many secs
    seconds = 2

    # don't understand yet
    short_normalize = (1.0 / 32768.0)

    # create an interface to PortAudio
    recorder = pyaudio.PyAudio()

    stream = recorder.open(format=sample_format,
                           channels=channels,
                           rate=fs,
                           frames_per_buffer=chunk,
                           input=True)

    print('Слушаю...')
    while True:
        input_signal = stream.read(chunk)
        rms_value = calculate_rms(input_signal, seconds, short_normalize)
        if rms_value > threshold:
            listening = record(timeout, threshold, stream, recorder, short_normalize, channels, fs, sample_format, chunk, seconds)
            if not listening:
                break

# record a speech


def record(timeout, threshold, stream, recorder, short_normalize, channels, fs, sample_format, chunk, seconds):

    frames=[]
    current_time = time.time()
    end_time = time.time() + timeout

    while current_time <= end_time:
        data = stream.read(chunk)
        if calculate_rms(data, seconds, short_normalize) >= threshold:
            end_time = time.time() + timeout
        current_time = time.time()
        frames.append(data)
    write_to_file(b''.join(frames), channels, fs, sample_format, recorder)

    # stop and close the stream
    #stream.stop_stream()
    #stream.close()
    # terminate the PortAudio interface
    #recorder.terminate()

    print('Секундочку...')
    return False

# calculate rms for noise level detection


def calculate_rms(frame, seconds, short_normalize):

    count = len(frame) / seconds
    formatted = '%dh' % count
    shorts = struct.unpack(formatted, frame)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * short_normalize
        sum_squares += n * n
    rms = math.pow(sum_squares / count, 0.5)

    return rms * 1000


def write_to_file(recording, channels, fs, sample_format, recorder):

    filename = '../utt1.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(recorder.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(recording)
    wf.close()

# RECOGNITION PART

# doesn't work properly


def recognize():

    # specify paths
    scp = '../wav.scp'
    spk2utt = '../spk2utt'
    model = '../model/final.mdl'
    graph = '../model/HCLG.fst'
    symbols = '../model/words.txt'
    conf = '../model/conf/mfcc.conf'
    iconf = '../conf/ivector_extractor.conf'
    feats_rspec = ('ark:compute-mfcc-feats --config=' + conf + ' scp:' + scp + ' ark:- |')
    ivectors_rspec = (feats_rspec + ' ivector-extract-online2 '
                      '--config=' + iconf + ' ark:' + spk2utt + ' ark:- ark:- |')
    lat_wspec = 'ark:| gzip -c > lat.gz'

    # instantiate the recognizer
    decoder_opts = LatticeFasterDecoderOptions()
    decoder_opts.beam = 13
    decoder_opts.max_active = 7000
    decodable_opts = NnetSimpleComputationOptions()
    decodable_opts.acoustic_scale = 1.0
    decodable_opts.frame_subsampling_factor = 3
    asr = NnetLatticeFasterRecognizer.from_files(model, graph, symbols,
        decoder_opts=decoder_opts, decodable_opts=decodable_opts)

    speaker_speech = 'Привет, как дела?'

    # extract the features, decode and write output lattices
    with SequentialMatrixReader(feats_rspec) as feats_reader, \
         SequentialMatrixReader(ivectors_rspec) as ivectors_reader, \
         CompactLatticeWriter(lat_wspec) as lat_writer:
        for (fkey, feats), (ikey, ivectors) in zip(feats_reader, ivectors_reader):
            print('ya tut')
            assert(fkey == ikey)
            out = asr.decode((feats, ivectors))
            lat_writer[fkey] = out['lattice']
            speaker_speech = out['text']
            print('Вы сказали: {}'.format(speaker_speech))
    return speaker_speech

# ANSWER GENERATION PART

def respond(speaker_speech):
    answer = chatbot.get_response(speaker_speech)
    print(speaker_speech)

    return answer

# VOICING PART

def speak(answer):

    os.system('echo -n \"{}\"; echo {} | spd-say -o rhvoice -l ru -e -t male1'.format('Мой ответ: ', answer))

def run():
    while True:
        #listen()
        speech_text = recognize()
        #bot_answer = respond(speech_text)
        #speak(bot_answer)
        #listen()

run()