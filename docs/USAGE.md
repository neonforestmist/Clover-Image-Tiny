# Running Clover locally

[Back to the README](../README.md).

## 2. Install

Python 3.11 or 3.12 is recommended. Install the PyTorch build suited to your
platform, then install the pinned application dependencies.

### 2.1 macOS or Linux

```bash
git clone https://github.com/neonforestmist/Clover-Image-Tiny.git
cd Clover-Image-Tiny

python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2.2 Windows PowerShell

```powershell
git clone https://github.com/neonforestmist/Clover-Image-Tiny.git
cd Clover-Image-Tiny

py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Keep room for the 1.67 GB model, the Python environment, and the Hugging Face
cache. CUDA uses an NVIDIA GPU, MPS uses Apple Silicon, and CPU works more
slowly in float32.

## 3. Local web app

```bash
python app.py --device auto
```

Open `http://127.0.0.1:7860`. The app exposes:

- prompt and negative prompt;
- Clover, Monet, Pointillism, and Watercolor Anime styles;
- 4–100 inference steps and guidance from 0–20;
- seed, width, height, and five schedulers;
- CUDA, Apple MPS, or CPU selection;
- generation metadata and packaged safety-checker results.

The model loads only when the first image is requested. A selected style LoRA
also downloads only when it is first used. To require previously cached files
and prevent network access, launch with `--local-files-only`.

## 4. Command-line example

```bash
python generate.py \
  --prompt "a tiny glass greenhouse glowing in a moonlit garden" \
  --negative-prompt "blurry, distorted, low detail" \
  --device auto \
  --steps 50 \
  --guidance-scale 7.5 \
  --scheduler pndm \
  --seed 1337 \
  --output clover-image-tiny.png
```

The runner defaults to `neonforestmist/Clover-Image-Tiny`; pass `--model` only
to use another Hub ID or a downloaded local folder. Every run writes a PNG and
a JSON sidecar containing resolved settings, seeds, checksums, runtime details,
and the safety result. Existing planned outputs are never overwritten.

### 4.1 Offline after the first download

```bash
python generate.py \
  --local-files-only \
  --prompt "a quiet library with arched windows" \
  --output library.png
```

## 5. Generation controls

| Flag | Range or choices | Default |
|---|---|---|
| `--steps` | 4–100 | `50` |
| `--guidance-scale` | 0–20 | `7.5` |
| `--scheduler` | `pndm`, `ddim`, `euler`, `euler-a`, `dpmpp-2m` | `pndm` |
| `--width`, `--height` | 256–768, multiples of 64 | `512` |
| `--num-images` | 1–4 | `1` |
| `--seed` | 0–2⁶³−1 | `1337` |
| `--device` | `auto`, `cuda`, `mps`, `cpu` | `auto` |

The validated reference recipe is 50-step PNDM, guidance 7.5, 512×512, and
one image. More steps take longer and do not guarantee a better result.
