from orcasound_processing import convert2wav
from matplotlib import pyplot as plt
from scipy import ndimage
import tensorflow as tf
import librosa
import os
import numpy as np
import subprocess


LOCAL_LOADING = False

if LOCAL_LOADING:
    
    humpback_path = 'models/humpback_whale_1/'
    humpback_model = hub.load(humpback_path)
    
else:
    # load models from tensorflow hub
    vggish_model = hub.load('https://tfhub.dev/google/vggish/1')
    yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
    humpback_model = hub.load('https://tfhub.dev/google/humpback_whale/1')


def score_signal(waveform, model):
    "Assumes the waveform has the correct sample rate"
    waveform = tf.Variable(waveform.reshape([-1, 1]), dtype=tf.float32)
    waveform = tf.expand_dims(waveform, 0)  # makes a batch of size 1
    pcen_spectrogram = model.front_end(waveform)

    # zero pad if lenght not a multiple of 128
    w_size = 128  # 3.84 seconds context window

    if pcen_spectrogram.shape[1] % w_size != 0:
        even_n = w_size - pcen_spectrogram.shape[1] % w_size
        pcen_spectrogram = tf.concat([pcen_spectrogram, tf.zeros([1, even_n, 64])], axis=1)

    n_frames = int(pcen_spectrogram.shape[1]/w_size)

    batch_pcen_spectrogram = tf.reshape(pcen_spectrogram, shape=(n_frames, w_size, 64)) 
    logits = model.logits(batch_pcen_spectrogram)
    probability = tf.nn.sigmoid(logits)

    return probability


def get_time_from_filename(filename):
    return f"{filename[11:19]}"


def generate_scores(input_dirs, output_dirs, humpback_model):
    """
    input_dirs is a list containing the timestamp folder names that you want to sync from S3
    output_dirs is a list containing folder paths to your .wav files that will be generated from .ts files
    input_dirs and output_dirs correspond in a one-to-one relationship
    e.g.
    input_dirs = ['1604457019', '1604478619', '1604500219', '1604521819']
    output_dirs = ['o1', 'o2', 'o3', 'o4']
    """
    for i, o in zip(input_dirs, output_dirs):
        subprocess.run(['mkdir', f'{o}'])
        subprocess.run(['aws', 's3', 'sync', f's3://streaming-orcasound-net/rpi_orcasound_lab/hls/{i}', f'{i}'])
        convert2wav(input_dir=f'{i}', output_dir=f'{o}')

    scores, times = [], []
    for wav_dir in output_dirs:
        wav_files = sorted(os.listdir(wav_dir))
        times.extend([get_time_from_filename(file) for file in wav_files])
        for wav_file in wav_files:
            x_pos, _ = librosa.load(os.path.join(wav_dir, wav_file), sr=10000)
            pos_prob = np.max(score_signal(x_pos, model).numpy())
            scores.append(pos_prob)
        print(f"{wav_dir} done!")
    return scores, times


def make_plot(scores: np.ndarray,
              times: np.ndarray,
              threshold: float,
              title: str,
              ylabel: str,
              xlabel: str):
    results = ndimage.median_filter(scores, size=5)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax.plot(times, results)
    ax.axhline(y=threshold, xmin=0, xmax=3, c="red", linewidth=0.5, zorder=0)
    ax.set_xticks(ax.get_xticks()[::420])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    plt.show()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s:%(message)s", stream=sys.stdout, level=logging.INFO
    )
    parser = argparse.ArgumentParser(
        description="applies humpback prediction algorithm to wav file"
    )
    parser.add_argument(
        "input_dir",
        help="Path to wav files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output scores. Default is `input_dir`.",
    )

    args = parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s:%(message)s", stream=sys.stdout, level=logging.INFO
    )
    parser = argparse.ArgumentParser(
        description="Creates spectrogram for each .ts file in the input directory."
    )
    parser.add_argument(
        "input_dirs",
        help="Path to the input directory with `.m3u8` playlist and `.ts` files. Should contain Unix timestamp of the stream start.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output directory for spectrograms. Default is `input_dir`.",
    )
    args = parser.parse_args()
    
    generate_scores(input_dirs, ['prediciton_plot'])
    
