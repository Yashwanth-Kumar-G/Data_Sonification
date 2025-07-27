# CSV → RGB Image → Sound → Decode → Download

This project converts a numeric CSV matrix into a **colorful RGB image**, generates **audio** representing the data, and allows decoding it back into the numeric matrix. Users can visualize their data as an image, listen to its sonification, and download the reconstructed values.

---

## Features
- Upload a numeric CSV file (square matrix values)
- Generate an **RGB image** based on custom value-to-color mapping
- Convert the numeric data into **audio tones** (frequency mapped)
- Download the **generated audio** and **metadata**
- Decode audio back to numeric values (currently simulated decoding)
- Download the **decoded matrix** as a CSV file

---

## How It Works
1. The numeric values in the CSV are mapped to **specific RGB colors**.
2. The matrix is converted to an **RGB image** and displayed in the app.
3. Each numeric value is mapped to a unique **sound frequency**.
4. These tones are concatenated to create an **audio file**.
5. Decoding reconstructs the numeric matrix (simulated using original values).
6. Both **audio** and **decoded CSV** can be downloaded.

---

## Requirements
- Python 3.8+
- Streamlit
- NumPy
- Pillow (PIL)
- Pydub
- FFmpeg (must be installed and added to PATH)

---

## Installation & Setup

1. **Clone this repository**:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create and activate a virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On Linux/Mac
```

3. **Install required dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install FFmpeg**:
- Download from https://www.gyan.dev/ffmpeg/builds/
- Extract and add the bin folder to your system PATH.

## Run

```bash
streamlit run app.py
```
Then open the given local URL in your browser

---

## Tech Stack
- Streamlit – Web UI
- NumPy – Array operations
- Pillow (PIL) – Image processing
- Pydub – Audio generation
- FFmpeg – Required for audio handling
