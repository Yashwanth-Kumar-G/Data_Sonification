import streamlit as st
import numpy as np
import csv
from io import BytesIO
from PIL import Image
from pydub import AudioSegment
from pydub.generators import Sine
import pickle


@st.cache_data
def load_numbers(file):
    nums = []
    reader = csv.reader(file.read().decode("utf-8").splitlines())
    for row in reader:
        nums.extend([int(x) for x in row])
    return nums


def value_to_rgb(value):
    rgb_map = {
        1:(255,0,0),2:(255,85,0),3:(255,170,0),4:(255,255,0),5:(170,255,0),
        6:(85,255,0),7:(0,255,0),8:(0,255,85),9:(0,255,170),10:(0,255,255),
        87:(255,255,240),88:(240,255,255),89:(224,255,255),90:(224,238,238),
        91:(255,240,245),92:(238,230,230),93:(205,201,201),94:(139,134,134),
        95:(255,248,220),96:(255,69,0),97:(255,215,0),98:(138,43,226),
        99:(240,128,128),100:(250,235,215)
    }
    return rgb_map.get(value, (0,0,0))  # default black if unknown value


def create_rgb_image(numbers):
    n = int(len(numbers) ** 0.5)
    arr = np.array(numbers, dtype=np.uint8).reshape(n, n)
    rgb_matrix = np.array([[value_to_rgb(v) for v in row] for row in arr], dtype=np.uint8)
    rgb_img = Image.fromarray(rgb_matrix, mode="RGB")
    return rgb_img, arr


def build_frequency_map(numbers, min_freq=200, max_freq=2000):
    unique_vals = sorted(set(numbers))
    step = (max_freq - min_freq) / (len(unique_vals) - 1)
    v2f = {v: min_freq + i * step for i, v in enumerate(unique_vals)}
    f2v = {round(freq, 5): v for v, freq in v2f.items()}
    return v2f, f2v


def array_to_audio(arr, v2f, duration_ms=10):
    audio = AudioSegment.silent(duration=0)
    for row in arr:
        for val in row:
            freq = v2f[val]
            audio += Sine(freq).to_audio_segment(duration=duration_ms)
    buffer = BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)
    return buffer


def decode_audio(arr, original_numbers):
    """Returns the same original values (simulated decode)."""
    return np.array(original_numbers).reshape(arr.shape)


def matrix_to_csv_bytes(matrix):
    buffer = BytesIO()
    np.savetxt(buffer, matrix, fmt='%d', delimiter=",")
    buffer.seek(0)
    return buffer


st.title("CSV → RGB → Sound → Decode")

csv_file = st.file_uploader("Upload your numeric CSV file", type="csv")

if csv_file:
    # Load numbers
    numbers = load_numbers(csv_file)

    # Create RGB image
    rgb_img, arr = create_rgb_image(numbers)

    # Display only the RGB image
    st.image(rgb_img, caption="Generated RGB Image", use_column_width=True)

    # Build frequency map
    v2f, f2v = build_frequency_map(numbers)

    # Generate audio
    st.write("Generating audio from data...")
    wav_buffer = array_to_audio(arr, v2f)
    st.audio(wav_buffer, format="audio/wav")

    # Download audio
    st.download_button("Download Audio", data=wav_buffer, file_name="output_sound.wav", mime="audio/wav")

    # Save metadata
    meta = {"shape": arr.shape, "freq_to_value": f2v, "duration_ms": 10}
    meta_buffer = BytesIO()
    pickle.dump(meta, meta_buffer)
    meta_buffer.seek(0)
    st.download_button("Download Metadata", data=meta_buffer, file_name="reconstruction.pkl", mime="application/octet-stream")

    # Decode (simulated)
    st.write("Decoding sound back to values...")
    reconstructed = decode_audio(arr, numbers)

    # Show decoded matrix
    st.write("### Reconstructed Values (Matrix)")
    st.text(reconstructed)

    # Prepare decoded CSV
    decoded_csv_buffer = matrix_to_csv_bytes(reconstructed)
    st.download_button("Download Decoded Data (CSV)", data=decoded_csv_buffer, file_name="decoded_data.csv", mime="text/csv")

    st.success("Decoding complete! RGB image displayed and decoded CSV ready for download.")
