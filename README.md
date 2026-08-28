# Clover Image Tiny

<p align="center">
  <img src="assets/banner.png" alt="Clover Image Tiny example gallery" width="1200">
</p>

<p align="center">
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny"><img alt="Hugging Face model" src="https://img.shields.io/badge/Hugging_Face-Model-FFD21E?logo=huggingface&logoColor=111"></a>
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint"><img alt="Inpainting model" src="https://img.shields.io/badge/Inpainting-Model-FFB000?logo=huggingface&logoColor=111"></a>
  <a href="https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo"><img alt="Live demo" src="https://img.shields.io/badge/Live-ZeroGPU_Demo-16A34A?logo=huggingface&logoColor=white"></a>
  <a href="https://github.com/neonforestmist/Clover-Image-Tiny-iOS"><img alt="iPhone app" src="https://img.shields.io/badge/iPhone-Core_ML-111111?logo=apple&logoColor=white"></a>
  <a href="https://github.com/neonforestmist/clover-image-tiny-lora-trainer"><img alt="LoRA trainer" src="https://img.shields.io/badge/LoRA-Visual_Trainer-7C3AED?logo=python&logoColor=white"></a>
  <a href="https://github.com/neonforestmist/Clover-Image-Tiny/actions/workflows/quality.yml"><img alt="Quality checks" src="https://github.com/neonforestmist/Clover-Image-Tiny/actions/workflows/quality.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="Apache 2.0 code license" src="https://img.shields.io/badge/Code-Apache_2.0-D22128?logo=apache&logoColor=white"></a>
</p>

The runnable-code home for **Clover Image Tiny**, a compact Stable Diffusion
1.4-class 512×512 model family for local Diffusers and on-device Core ML
generation and inpainting workflows.

This GitHub repository intentionally contains **no model weights**. The Python
examples download the approximately 1.67 GB checkpoint from
[Hugging Face](https://huggingface.co/neonforestmist/Clover-Image-Tiny) on first
use and reuse the normal local Hugging Face cache afterward.

For masked image editing, use the dedicated
[Clover Image Tiny Inpaint model](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint)
instead of the regular 4-channel checkpoint. Its optional
[Core ML bundle](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint-CoreML)
is published separately.

## 1. Choose how to run it

| Experience | Best for | Start here |
|---|---|---|
| Local web app | Visual prompting on macOS, Windows, or Linux | `python app.py` |
| Command line | Scripts, reproducibility, and batch workflows | `python generate.py --prompt "…"` |
| Live demo | Trying Regular generation or Inpainting without local setup | [ZeroGPU Space](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo) |
| Native iPhone app | Private on-device Core ML generation | [Clover Image Tiny iOS](https://github.com/neonforestmist/Clover-Image-Tiny-iOS) |
| LoRA studio | Training styles and exporting Core ML state | [Visual LoRA trainer](https://github.com/neonforestmist/clover-image-tiny-lora-trainer) |

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

## 6. Inpainting

[`Clover-Image-Tiny-Inpaint`](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint)
is the separate 9-channel SD 1.4-class adaptation. Its U-Net receives noisy
latents, a white-on-black mask, and masked-source latents. White pixels are
regenerated and black pixels are preserved. The companion
[`Core ML bundle`](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint-CoreML)
is an optional 1,670 MB download in the iOS app; it is not included in the app
or downloaded with Regular Clover.

```python
from diffusers import AutoPipelineForInpainting, DPMSolverMultistepScheduler
from diffusers.utils import load_image

pipe = AutoPipelineForInpainting.from_pretrained(
    "neonforestmist/Clover-Image-Tiny-Inpaint",
    torch_dtype="auto",
)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

result = pipe(
    prompt="a realistic orange cat sitting in the doorway, detailed photography",
    image=load_image("source.png"),
    mask_image=load_image("mask.png"),
    padding_mask_crop=64,
    num_inference_steps=20,
    guidance_scale=7.5,
).images[0]
result.save("inpainted.png")
```

DPM-Solver++ with 20 steps is the recommended starting point; interactive
inpainting is capped at 50 steps in Clover iOS and the hosted demo. Small masks
use a context crop before 512×512 inference and are composited back through the
exact mask. Existing Regular Clover LoRAs target a 4-channel U-Net and are not
interchangeable with this 9-channel model.

<p align="center">
  <img src="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/main/examples/result-cat.png" alt="A cat inpainted into a masked greenhouse doorway" width="512">
</p>

### 6.1 Example: add blue sunglasses

Prompt: `add blue sunglasses`

<p align="center">
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint"><img src="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/main/examples/sunglasses-source.png" alt="Cat source before adding sunglasses" width="360"></a>
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint"><img src="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/main/examples/sunglasses-result.png" alt="Cat after adding blue sunglasses" width="360"></a>
</p>
<p align="center"><em>Source image</em> &nbsp;→&nbsp; <em>Inpainted result</em></p>

## 7. Example outputs

<p align="center">
  <img src="assets/examples.png" alt="Nine Clover Image Tiny prompt examples" width="1000">
</p>

Nine 512×512 generations from the model's Hugging Face prompt gallery. See the
[Hugging Face model card](https://huggingface.co/neonforestmist/Clover-Image-Tiny)
for more examples, the exact evaluation recipe, training lineage, and data
provenance.

## 8. Complete Clover ecosystem

This repository is the central directory, while large artifacts remain on
Hugging Face and platform-specific source remains in focused GitHub projects.

| Project | Purpose |
|---|---|
| [Clover Image Tiny on Hugging Face](https://huggingface.co/neonforestmist/Clover-Image-Tiny) | Model weights, model card, provenance, and exact checkpoint files |
| [Clover Image Tiny Demo](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo) | Hosted ZeroGPU generation with named styles |
| [Clover Image Tiny iOS](https://github.com/neonforestmist/Clover-Image-Tiny-iOS) | SwiftUI/Core ML iPhone app and model downloader |
| [Clover Image Tiny Inpaint](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint) | 9-channel Diffusers inpainting checkpoint, examples, and citation |
| [Clover Image Tiny Inpaint Core ML](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint-CoreML) | Optional 1,670 MB compiled inpainting resources |
| [Clover Image Tiny LoRA Trainer](https://github.com/neonforestmist/clover-image-tiny-lora-trainer) | Visual training studio and stateful Core ML exporter |
| [Clover Image Tiny Core ML](https://huggingface.co/neonforestmist/Clover-Image-Tiny-CoreML) | Shared downloadable Core ML pipeline |

The full style and dataset directory is in [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md).

## 9. Repository contents

```text
Clover-Image-Tiny/
├── app.py                    # local Gradio interface
├── generate.py               # reproducible Diffusers command-line runner
├── requirements.txt          # pinned Python dependencies
├── docs/ECOSYSTEM.md         # every model, app, style, and dataset link
├── assets/                   # documentation images only
└── .github/workflows/        # lightweight source checks
```

Model checkpoints, LoRAs, compiled Core ML packages, generated outputs, and
local caches are excluded by `.gitignore`.

## 10. Safety and limitations

The packaged Stable Diffusion safety checker remains enabled in both runnable
examples. It can miss harmful material or over-filter benign content, so
applications still need controls appropriate to their audience.

Hands, anatomy, exact counts and relationships, and readable text can be
difficult. Results vary by prompt, seed, scheduler, device, and precision.
Do not use outputs for consequential decisions or identity claims.

## 11. Licenses

- Source code in this repository: [Apache-2.0](LICENSE).
- Downloaded Clover model and style weights: CreativeML Open RAIL-M; see the
  [model repository](https://huggingface.co/neonforestmist/Clover-Image-Tiny).
- Linked generated style datasets: Apache-2.0.

The code license does not replace the license attached to downloaded model
weights.
