# Clover Image Tiny ecosystem

The code, model weights, Core ML release, iPhone app, training tools, named
styles, and datasets live in focused repositories. This page is the complete
directory.

## Core projects

| Resource | Location |
|---|---|
| Runnable Python examples | [GitHub · Clover-Image-Tiny](https://github.com/neonforestmist/Clover-Image-Tiny) |
| Diffusers checkpoint and model card | [Hugging Face · Clover-Image-Tiny](https://huggingface.co/neonforestmist/Clover-Image-Tiny) |
| Live ZeroGPU demo | [Hugging Face Space · Clover-Image-Tiny-Demo](https://huggingface.co/spaces/neonforestmist/Clover-Image-Tiny-Demo) |
| Native iPhone app | [GitHub · Clover-Image-Tiny-iOS](https://github.com/neonforestmist/Clover-Image-Tiny-iOS) |
| LoRA trainer and Core ML GUI | [GitHub · clover-image-tiny-lora-trainer](https://github.com/neonforestmist/clover-image-tiny-lora-trainer) |
| Shared Core ML pipeline | [Hugging Face · Clover-Image-Tiny-CoreML](https://huggingface.co/neonforestmist/Clover-Image-Tiny-CoreML) |

## Named styles

| Style | Diffusers LoRA | iPhone runtime style |
|---|---|---|
| Monet | [Standard LoRA](https://huggingface.co/neonforestmist/clover-image-tiny-monet-lora) | [Named Core ML style](https://huggingface.co/neonforestmist/clover-image-tiny-monet-lora-coreml) |
| Pointillism | [Standard LoRA](https://huggingface.co/neonforestmist/clover-image-tiny-pointillism-lora) | [Named Core ML style](https://huggingface.co/neonforestmist/clover-image-tiny-pointillism-lora-coreml) |
| Watercolor Anime | [Standard LoRA](https://huggingface.co/neonforestmist/clover-image-tiny-watercolor-anime-lora) | [Named Core ML style](https://huggingface.co/neonforestmist/clover-image-tiny-watercolor-anime-lora-coreml) |

The iPhone runtime files contain only compatible LoRA state tensors. The app
requires the shared Clover Core ML model as a prerequisite.

## Training datasets

| Dataset | Style |
|---|---|
| [`GPT_Monet_Style_Images`](https://huggingface.co/datasets/neonforestmist/GPT_Monet_Style_Images) | Monet |
| [`GPT_Pointillism_Style_Images`](https://huggingface.co/datasets/neonforestmist/GPT_Pointillism_Style_Images) | Pointillism |
| [`GPT_Watercolor_Anime_Style_Images`](https://huggingface.co/datasets/neonforestmist/GPT_Watercolor_Anime_Style_Images) | Watercolor Anime |

## License map

- GitHub application and tooling code: Apache-2.0.
- Clover Image Tiny and derived LoRA/Core ML weights: CreativeML Open RAIL-M.
- Linked generated style datasets: Apache-2.0.

Always read the license in the repository that hosts the artifact being used.
