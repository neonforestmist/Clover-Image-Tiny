# 🍀 Clover Image Tiny

### Small model. Room for big ideas.

**Turn a few words into an image. Explore a different style. Make a focused edit.**
Clover Image Tiny is a compact, open-weight AI image generator for local text-to-image
workflows on Mac, Windows, and Linux, with Core ML releases for Apple devices.
Download the model once, then create offline on your own hardware.

<p align="center">
  <a href="https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo"><img alt="Try the demo" src="assets/links/try-demo.svg" height="40"></a>
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny"><img alt="Get the model" src="assets/links/get-model.svg" height="40"></a>
  <a href="https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint"><img alt="Inpainting" src="assets/links/inpainting.svg" height="40"></a>
  <a href="https://github.com/neonforestmist/Clover-Image-Tiny"><img alt="GitHub source" src="assets/links/github-source.svg" height="40"></a>
</p>

## Create from a prompt

Describe the scene you want to explore. The regular Clover model can turn simple prompts
into landscapes, still lifes, and stylized artwork. These are existing model examples,
with the original prompts shown below.

| Moonlit greenhouse | Blue flowers | Stained-glass night |
|:---:|:---:|:---:|
| ![Clover text-to-image output: a tiny greenhouse in a moonlit garden](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_74.png) | ![Clover text-to-image output: a bouquet of blue flowers](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_79.png) | ![Clover text-to-image output: a stained-glass starry night](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/prompt-gallery/original/image_78.png) |
| “a tiny glass greenhouse glowing in a moonlit garden” | “A bouquet of blue flowers” | “A stain glass window of a starry night” |

## Change a detail with inpainting

Keep the image you started with and describe an edit to a selected area. Inpainting means
painting a mask over the part you want to regenerate—white marks the edit, black marks what
to keep. The published example below uses the prompt **“add blue sunglasses.”**

| Before | After the masked edit |
|:---:|:---:|
| ![Original cat artwork before the masked sunglasses edit](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/3e22009fb6e61944f28b0389f775fc47e2c48724/examples/sunglasses-source.png) | ![Clover inpainting example: the cat with blue sunglasses added](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint/resolve/3e22009fb6e61944f28b0389f775fc47e2c48724/examples/sunglasses-result.png) |

[**Explore Clover Inpaint HQ →**](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint) · [**Try generation and inpainting →**](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo)

Inpaint HQ pairs the full Stable Diffusion 1.5 inpainting denoiser with Clover's shared
components. It is a larger, separate model focused on editing quality. For exact preservation,
composite the result through the original binary mask.

## Why create with Clover?

- **Keep your ideas local.** Run generation on your own computer after downloading the weights.
- **Start small.** The regular model has a 323.4M-parameter denoiser and generates at a native 512 × 512 resolution.
- **Find your look.** Explore Monet, Pointillism, and Watercolor Anime with optional style adapters.
- **Make it part of your workflow.** Use a visual demo, Python, a command-line runner, or the native Core ML app.

Clover is a good fit for visual brainstorming, illustration experiments, and developers
building local creative tools. You control the prompt, seed, style, and generation settings.

## One prompt, different styles

Style adapters—also called LoRAs—let you change the visual character of your images.
Here is the same greenhouse prompt with the base model and three published Clover styles.

| Clover | Monet | Pointillism | Watercolor Anime |
|:---:|:---:|:---:|:---:|
| ![Base Clover greenhouse example](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/normal.png) | ![Monet style greenhouse with painterly brushwork](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/monet.png) | ![Pointillism style greenhouse made from colored dots](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/pointillism.png) | ![Watercolor Anime style greenhouse illustration](https://huggingface.co/neonforestmist/Clover-Image-Tiny/resolve/3f2a698bc3cbad617970a73d623e0732bb5f87f5/examples/normal-to-lora/watercolor_anime.png) |
| [Base model](https://huggingface.co/neonforestmist/Clover-Image-Tiny) | [Get Monet](https://huggingface.co/neonforestmist/clover-image-tiny-monet-lora) | [Get Pointillism](https://huggingface.co/neonforestmist/clover-image-tiny-pointillism-lora) | [Get Watercolor Anime](https://huggingface.co/neonforestmist/clover-image-tiny-watercolor-anime-lora) |

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
generation and optional styles. For masked editing, use the [hosted demo](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo),
[native app](https://github.com/neonforestmist/Clover-Image-Tiny-iOS), or [Inpaint HQ Python example](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint#run-an-edit-with-python).

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

## Choose your way to create

| Your workflow | Start here |
|---|---|
| Try it in your browser | [Hosted demo: generation and inpainting](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo) |
| Generate locally with a visual interface | [GitHub setup and Gradio app](https://github.com/neonforestmist/Clover-Image-Tiny#run-clover-locally) |
| Build with Python and Diffusers | [Model weights](https://huggingface.co/neonforestmist/Clover-Image-Tiny) · [Local runner](https://github.com/neonforestmist/Clover-Image-Tiny/blob/main/generate.py) |
| Create on iPhone or iPad | [Native Clover app](https://github.com/neonforestmist/Clover-Image-Tiny-iOS) · [Core ML resources](https://huggingface.co/neonforestmist/Clover-Image-Tiny-CoreML) |
| Train a personal style | [Visual LoRA trainer](https://github.com/neonforestmist/clover-image-tiny-lora-trainer) |

The hosted demo runs remotely. Local Python and Core ML workflows run on your hardware
after setup; model downloads require a network connection.

## Small enough to build around

| Regular Clover model | What it means |
|---|---|
| **323.4M denoiser parameters** | A compact Stable Diffusion 1.4-class image model |
| **About 1.67 GB of model files** | Includes the text encoder, VAE, and packaged safety checker; allow extra space for dependencies and caches |
| **512 × 512 native output** | A practical starting point for visual experiments |
| **Diffusers + separate Core ML exports** | Python integration and a path to on-device Apple apps |

On one NVIDIA A10G benchmark, Clover averaged **1.024 seconds per image** across
16 prompts at 512 × 512, 30 DDIM steps, and guidance 7.5. That is a specific measured
GPU result, not an iPhone timing or a speed guarantee. [See the comparison and protocol](https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/benchmarks/text-to-image/results/clover-small-model-comparison-20260825/REPORT.md).

## A few things to know

**Can I use Clover offline?** Yes. Download the model and dependencies first, then use
`--local-files-only` with the local runner. No hosted generation service is required.

**Does it work on a Mac?** The Python path supports Apple silicon through PyTorch MPS.
NVIDIA systems use CUDA; CPU inference is also supported, but slower.

**Is normal Clover the same as Inpaint HQ?** They are separate checkpoints. Normal Clover
creates images from text. Inpaint HQ takes an image, a mask, and a prompt, and uses a larger denoiser.

**What are its limits?** Hands, faces, readable text, precise counts, and complex relationships
can be unreliable. Examples are selected outputs; results vary with prompts and settings.
The packaged safety checker in the Python runner and hosted demo is imperfect.

## Explore the project

[Model weights and card](https://huggingface.co/neonforestmist/Clover-Image-Tiny) · [Inpaint HQ](https://huggingface.co/neonforestmist/Clover-Image-Tiny-Inpaint) ·
[Core ML downloads](https://huggingface.co/neonforestmist/Clover-Image-Tiny-CoreML) · [Complete ecosystem](docs/ECOSYSTEM.md) ·
[Training and benchmark details](https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/docs/MODEL_DETAILS.md)

This repository contains the local Gradio app, Diffusers command-line runner, pinned
dependencies, and documentation. Model weights download from Hugging Face.

Source code: [Apache-2.0](LICENSE). Model and style weights: **CreativeML Open RAIL-M**;
see the [model's license ledger](https://huggingface.co/neonforestmist/Clover-Image-Tiny/blob/main/MODEL_DATA_LICENSES.md).
The code license does not replace the terms for downloaded weights.

Created by **Lukas Lozada Perez**.
