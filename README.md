<h1 align="center">Clover Image Tiny</h1>

<p align="center"><img src="https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/assets/clover-image-tiny-banner.png" alt="Clover Image Tiny original mosaic" width="1200"></p>

<p align="center">
  <strong>SD 1.4-class image generation in a compact model for local apps and offline use.</strong><br>
  512 × 512 output · 323.4M-parameter denoiser · LoRA styles · Diffusers and separate Core ML releases.
</p>

<table align="center" width="100%">
<tr>
<td align="center" width="25%"><a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny"><img src="assets/links/model.svg" alt="HF MODEL" width="100%"></a></td>
<td align="center" width="25%"><a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint"><img src="assets/links/inpaint.svg" alt="INPAINTING" width="100%"></a></td>
<td align="center" width="25%"><a href="https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo"><img src="assets/links/live-demo.svg" alt="LIVE DEMO" width="100%"></a></td>
<td align="center" width="25%"><a href="https://github.com/neonforestmist/Clover-Image-Tiny-iOS"><img src="assets/links/ios-app.svg" alt="IPHONE / CORE ML" width="100%"></a></td>
</tr>
<tr>
<td align="center" width="25%"><a href="https://github.com/neonforestmist/clover-image-tiny-lora-trainer"><img src="assets/links/trainer.svg" alt="LORA TRAINER" width="100%"></a></td>
<td align="center" width="25%"><a href="https://github.com/neonforestmist/Clover-Image-Tiny"><img src="assets/links/source.svg" alt="GITHUB SOURCE" width="100%"></a></td>
<td align="center" width="25%"><a href="https://github.com/neonforestmist/Clover-Image-Tiny/actions/workflows/quality.yml"><img src="assets/links/checks.svg" alt="QUALITY CHECKS" width="100%"></a></td>
<td align="center" width="25%"><a href="https://github.com/neonforestmist/Clover-Image-Tiny/blob/main/LICENSE"><img src="assets/links/license.svg" alt="CODE LICENSE" width="100%"></a></td>
</tr>
</table>

<p align="center"><a href="#models">Models</a> · <a href="#examples">Examples</a> · <a href="#styles">Styles</a> · <a href="https://github.com/neonforestmist/Clover-Image-Tiny#run-clover-locally">Run it</a> · <a href="#evaluation">Evaluation</a> · <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/docs/MODEL_DETAILS.md">Documentation</a></p>

---

## Models

Use the regular model to generate an image from text. Use Inpaint HQ to edit a masked
region of an existing image. Both run locally after the model and dependencies are downloaded.

| Clover Image Tiny | Clover Inpaint HQ |
|:---:|:---:|
| ![Regular Clover output: a bouquet of blue flowers](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_79.png) | ![Published Clover inpainting example: blue sunglasses added to a cat](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/3e22009fb6e61944f28b0389f775fc47e2c48724/examples/sunglasses-result.png) |
| **Text → image.** Compact SD 1.4-class generation with a 323.4M-parameter denoiser. | **Image + mask + text → edit.** SD 1.5-class inpainting with Clover's shared components. A larger, separate checkpoint. |

The regular Diffusers package is about **1.67 GB**, including its text encoder, VAE,
and safety checker. The 323.4M count describes the denoiser, not the complete pipeline.
Inpainting uses a separate checkpoint; neither download includes the Python environment.
The hosted demo runs remotely; local Python and Core ML workflows run on your hardware after setup.

## Examples

Selected outputs from the regular model, with their original prompts.

| Moonlit greenhouse | Blue flowers | Stained-glass night |
|:---:|:---:|:---:|
| ![Clover text-to-image output: a tiny greenhouse in a moonlit garden](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_74.png) | ![Clover text-to-image output: a bouquet of blue flowers](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_79.png) | ![Clover text-to-image output: a stained-glass starry night](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_78.png) |
| “a tiny glass greenhouse glowing in a moonlit garden” | “A bouquet of blue flowers” | “A stain glass window of a starry night” |

## Inpainting example

Inpainting regenerates the white area of a mask. Black marks the area to preserve.
This published before-and-after example uses the prompt **“add blue sunglasses.”**

| Before | After the masked edit |
|:---:|:---:|
| ![Original cat artwork before the masked sunglasses edit](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/3e22009fb6e61944f28b0389f775fc47e2c48724/examples/sunglasses-source.png) | ![Clover inpainting example: the cat with blue sunglasses added](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/3e22009fb6e61944f28b0389f775fc47e2c48724/examples/sunglasses-result.png) |

Inpaint HQ provides SD 1.5-class masked editing. For exact preservation outside the
edited region, composite the result through the original binary mask. Its full-size
inpainting denoiser and shared components are documented in the inpainting model card.

## Styles

Optional LoRA adapters change the model's visual style. Below is the same greenhouse
prompt with the base model, Monet, Pointillism, and Watercolor Anime.

| Clover | Monet | Pointillism | Watercolor Anime |
|:---:|:---:|:---:|:---:|
| ![Base Clover greenhouse example](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/normal.png) | ![Monet style greenhouse with painterly brushwork](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/monet.png) | ![Pointillism style greenhouse made from colored dots](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/pointillism.png) | ![Watercolor Anime style greenhouse illustration](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/watercolor_anime.png) |
| Base model | [Get Monet](https://huggingface.co/neonforestmist/clover-image-tiny-monet-lora) | [Get Pointillism](https://huggingface.co/neonforestmist/clover-image-tiny-pointillism-lora) | [Get Watercolor Anime](https://huggingface.co/neonforestmist/clover-image-tiny-watercolor-anime-lora) |

## Run Clover locally

Use **Python 3.11 or 3.12**. On macOS or Linux:

```bash
git clone https://github.com/neonforestmist/Clover-Image-Tiny.git
cd Clover-Image-Tiny
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py --device auto
```

Open **http://127.0.0.1:7860** and enter a prompt. The local web app supports regular
generation and optional styles. For masked editing, use the hosted demo or native app
linked above, or the [Inpaint HQ Python example](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint#run-an-edit-with-python).

The first generation downloads about **1.67 GB** of model files. Later runs reuse the
Hugging Face cache. Allow extra room for the Python environment and caches. Use
`--local-files-only` after setup to work offline.

<details>
<summary>Windows setup</summary>

```powershell
git clone https://github.com/neonforestmist/Clover-Image-Tiny.git
cd Clover-Image-Tiny
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py --device auto
```

</details>

<details>
<summary>Prefer the command line?</summary>

```bash
python generate.py \
  --prompt "a tiny glass greenhouse glowing in a moonlit garden" \
  --negative-prompt "blurry, distorted, low detail" \
  --device auto --steps 50 --guidance-scale 7.5 \
  --scheduler pndm --seed 1337 --output clover.png
```

The runner saves a PNG and a JSON record of settings, seed, and safety results.
Existing planned outputs are never overwritten.

</details>

[**Full setup, controls, and offline instructions →**](docs/USAGE.md)

## Model facts

| Regular Clover model | What it means |
|---|---|
| **323.4M denoiser parameters** | BK-SDM-Tiny architecture; denoiser count only |
| **About 1.67 GB of model files** | Includes the text encoder, VAE, and packaged safety checker; allow extra space for dependencies and caches |
| **512 × 512 native output** | Native output resolution |
| **Diffusers + separate Core ML exports** | Python integration and a path to on-device Apple apps |

## Evaluation

### Compact model, practical generation speed

Clover combines a **323.4M-parameter denoiser** with **1.024-second mean generation**
in the published NVIDIA A10G test. It retains the compact architecture while adding
Clover's distillation pass, style adapters, and separate Core ML deployment options.

| Measured on NVIDIA A10G | Clover Image Tiny |
|---|---:|
| Mean generation time ↓ | **1.024 s/image** |
| Peak CUDA memory ↓ | **2,233 MB** |
| Denoiser parameters ↓ | **323.4M** |

**Test settings:** 16 prompts, 512 × 512, 30 DDIM steps, guidance 7.5, after warm-up.
Lower values mean less time, memory, or denoiser storage—not automatically better images.
These are GPU results, not older-device or iPhone timings.

Clover runs in the same approximate one-second range as BK-SDM-Tiny-2M and Segmind
Tiny-SD in this test. Other references lead individual latency, memory, and CLIP
metrics; the comparison does not establish an overall quality or speed lead.

<details>
<summary>Full four-model comparison: latency, memory, and prompt alignment</summary>

| Model | U-Net parameters ↓ | Loaded pipeline parameters ↓ | Mean latency ↓ | Peak CUDA memory ↓ | Mean CLIP cosine ↑ |
|---|---:|---:|---:|---:|---:|
| Clover Image Tiny | **323.4M** | 834.1M | 1.024 s | 2,233 MB | 0.3195 |
| [BK-SDM-Tiny-2M](https://huggingface.co/nota-ai/bk-sdm-tiny-2m) | **323.4M** | 834.1M | 1.027 s | 2,230 MB | 0.3246 |
| [Segmind Tiny-SD](https://huggingface.co/segmind/tiny-sd) | **323.4M** | **530.1M** | 1.028 s | **1,649 MB** | **0.3345** |
| [BK-SDM-v2-Tiny](https://huggingface.co/nota-ai/bk-sdm-v2-tiny) | 326.8M | 750.9M | **0.957 s** | 2,067 MB | 0.3303 |

**↓ Lower is better for size, latency, and memory; ↑ higher is better for CLIP prompt alignment. Bold marks the best result in each column, including ties.** Parameter counts describe footprint, not image quality.

CLIP cosine measures prompt alignment, not overall visual quality. The latency gaps
between Clover, BK-SDM-Tiny-2M, and Segmind Tiny-SD are below 0.4% and should be read
as near parity, not an established speed advantage.

</details>

[Benchmark protocol, all outputs, and raw results](https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/benchmarks/text-to-image/results/clover-small-model-comparison-20260825/REPORT.md).

## Usage notes

**Can I use Clover offline?** Yes. Download the model and dependencies first, then use
`--local-files-only` with the local runner. No hosted generation service is required.

**Does it work on a Mac?** The Python path supports Apple silicon through PyTorch MPS.
NVIDIA systems use CUDA; CPU inference is also supported, but slower.

**Is normal Clover the same as Inpaint HQ?** They are separate checkpoints. Normal Clover
creates images from text. Inpaint HQ takes an image, a mask, and a prompt, and uses a larger denoiser.

**What are its limits?** Hands, faces, readable text, precise counts, and complex relationships
can be unreliable. Examples are selected outputs; results vary with prompts and settings.
The packaged safety checker in the Python runner and hosted demo is imperfect.

## About this repository

This repository contains the local Gradio app, Diffusers command-line runner, pinned
dependencies, and documentation. Model weights download from Hugging Face.

Source code: [Apache-2.0](LICENSE). Model and style weights: **CreativeML Open RAIL-M**;
see the [model's license ledger](https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/MODEL_DATA_LICENSES.md).
The code license does not replace the terms for downloaded weights.

## Full example gallery

<p align="center"><img src="assets/examples.png" alt="Nine original Clover Image Tiny prompt examples" width="1000"></p>

## Related projects

The [ecosystem directory](docs/ECOSYSTEM.md) lists the apps, model downloads,
Core ML bundles, style adapters, and training datasets in one place.

## Detailed documentation

<details>
<summary>Complete installation instructions and generation controls</summary>

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

</details>

<details>
<summary>Repository contents and safety information</summary>

### Repository contents

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

### Safety and limitations

The packaged Stable Diffusion safety checker remains enabled in both runnable
examples. It can miss harmful material or over-filter benign content, so
applications still need controls appropriate to their audience.

Hands, anatomy, exact counts and relationships, and readable text can be
difficult. Results vary by prompt, seed, scheduler, device, and precision.
Do not use outputs for consequential decisions or identity claims.

</details>

## Citation

If you use Clover Image Tiny in your work, please cite the model release:

```bibtex
@software{lozadaperez2026cloverimagetiny,
  author = {Lukas Lozada Perez},
  title = {Clover Image Tiny: Compact Local Text-to-Image Diffusion},
  year = {2026},
  url = {https://huggingface.co/neonforestmist/Clover-Image-Tiny}
}
```

Created by **Lukas Lozada Perez**.
