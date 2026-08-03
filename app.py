#!/usr/bin/env python3
"""Run Clover Image Tiny in a local Gradio interface."""

from __future__ import annotations

import argparse
import math
import threading
from dataclasses import asdict, dataclass
from typing import Any

import gradio as gr
import torch
from diffusers import (
    DDIMScheduler,
    DiffusionPipeline,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    PNDMScheduler,
)


MODEL_ID = "neonforestmist/Clover-Image-Tiny"
DEFAULT_NEGATIVE_PROMPT = "blurry, distorted, low detail"
SCHEDULERS: dict[str, type[Any]] = {
    "PNDM": PNDMScheduler,
    "DDIM": DDIMScheduler,
    "Euler": EulerDiscreteScheduler,
    "Euler Ancestral": EulerAncestralDiscreteScheduler,
    "DPM++ 2M": DPMSolverMultistepScheduler,
}
STYLES: dict[str, dict[str, str]] = {
    "Clover": {"repo": "", "name": "", "trigger": "No trigger phrase required."},
    "Monet": {
        "repo": "neonforestmist/clover-image-tiny-monet-lora",
        "name": "monet",
        "trigger": "Monet Style",
    },
    "Pointillism": {
        "repo": "neonforestmist/clover-image-tiny-pointillism-lora",
        "name": "pointillism",
        "trigger": "pointillism painting",
    },
    "Watercolor Anime": {
        "repo": "neonforestmist/clover-image-tiny-watercolor-anime-lora",
        "name": "watercolor_anime",
        "trigger": "watercolor anime",
    },
}

APP_CSS = """
.gradio-container { max-width: 1220px !important; margin: 0 auto !important; }
.hero {
  border: 1px solid var(--border-color-primary); border-radius: 20px;
  padding: 24px 26px; margin: 10px 0 18px;
  background: linear-gradient(120deg, var(--block-background-fill), rgba(34,197,94,.10));
}
.hero small { color: #16803b; font-weight: 750; letter-spacing: .1em; text-transform: uppercase; }
.hero h1 { font-size: clamp(30px, 5vw, 48px); letter-spacing: -.045em; margin: 8px 0; }
.hero p { color: var(--body-text-color-subdued); max-width: 760px; line-height: 1.55; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 18px; }
.stat { padding: 11px 13px; border: 1px solid var(--border-color-primary); border-radius: 12px; background: var(--block-background-fill); }
.stat strong, .stat span { display: block; }
.stat span { color: var(--body-text-color-subdued); font-size: 12px; margin-top: 2px; }
#output-image { min-height: 520px; }
#metadata { min-height: 150px; }
@media (max-width: 700px) { .stats { grid-template-columns: 1fr; } }
"""

PIPELINE: DiffusionPipeline | None = None
PIPELINE_DEVICE = ""
BASE_SCHEDULER_CONFIG: dict[str, Any] = {}
LOADED_STYLES: set[str] = set()
PIPELINE_LOCK = threading.Lock()


@dataclass(frozen=True)
class Request:
    prompt: str
    negative_prompt: str
    style: str
    steps: int
    guidance_scale: float
    seed: int
    width: int
    height: int
    scheduler: str


def choose_device(requested: str) -> tuple[str, torch.dtype]:
    if requested == "auto":
        if torch.cuda.is_available():
            requested = "cuda"
        elif torch.backends.mps.is_available():
            requested = "mps"
        else:
            requested = "cpu"
    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    if requested == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS was requested but is unavailable")
    dtype = torch.float16 if requested in {"cuda", "mps"} else torch.float32
    return requested, dtype


def validate_request(
    prompt: object,
    negative_prompt: object,
    style: object,
    steps: object,
    guidance_scale: object,
    seed: object,
    width: object,
    height: object,
    scheduler: object,
) -> Request:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must not be empty")
    if not isinstance(negative_prompt, str):
        raise ValueError("Negative prompt must be text")
    if style not in STYLES:
        raise ValueError("Choose a listed style")
    if scheduler not in SCHEDULERS:
        raise ValueError("Choose a listed scheduler")

    step_count = int(steps)
    parsed_seed = int(seed)
    parsed_width = int(width)
    parsed_height = int(height)
    parsed_guidance = float(guidance_scale)
    if not 4 <= step_count <= 100:
        raise ValueError("Steps must be between 4 and 100")
    if not 0 <= parsed_seed < 2**63:
        raise ValueError("Seed must be between 0 and 2^63 − 1")
    if not math.isfinite(parsed_guidance) or not 0 <= parsed_guidance <= 20:
        raise ValueError("Guidance must be between 0 and 20")
    for name, value in (("Width", parsed_width), ("Height", parsed_height)):
        if not 256 <= value <= 768 or value % 64:
            raise ValueError(f"{name} must be 256–768 and divisible by 64")

    return Request(
        prompt=prompt.strip(),
        negative_prompt=negative_prompt.strip(),
        style=str(style),
        steps=step_count,
        guidance_scale=parsed_guidance,
        seed=parsed_seed,
        width=parsed_width,
        height=parsed_height,
        scheduler=str(scheduler),
    )


def load_pipeline(model: str, device: str, local_files_only: bool) -> DiffusionPipeline:
    global PIPELINE, PIPELINE_DEVICE, BASE_SCHEDULER_CONFIG
    if PIPELINE is not None:
        return PIPELINE

    resolved_device, dtype = choose_device(device)
    pipeline = DiffusionPipeline.from_pretrained(
        model,
        torch_dtype=dtype,
        use_safetensors=True,
        local_files_only=local_files_only,
    ).to(resolved_device)
    if pipeline.safety_checker is None or pipeline.feature_extractor is None:
        raise RuntimeError("The downloaded checkpoint is missing its safety checker")
    pipeline.set_progress_bar_config(disable=True)
    PIPELINE = pipeline
    PIPELINE_DEVICE = resolved_device
    BASE_SCHEDULER_CONFIG = dict(pipeline.scheduler.config)
    return pipeline


def style_hint(style: str) -> str:
    trigger = STYLES.get(style, STYLES["Clover"])["trigger"]
    if style == "Clover":
        return "Base Clover selected. No trigger phrase is needed."
    return f"Add `{trigger}` to the prompt to invoke this style."


def apply_style(pipeline: DiffusionPipeline, style: str) -> None:
    if style == "Clover":
        pipeline.disable_lora()
        return
    spec = STYLES[style]
    if style not in LOADED_STYLES:
        pipeline.load_lora_weights(spec["repo"], adapter_name=spec["name"])
        LOADED_STYLES.add(style)
    pipeline.enable_lora()
    pipeline.set_adapters(spec["name"])


def generate(
    prompt: object,
    negative_prompt: object,
    style: object,
    steps: object,
    guidance_scale: object,
    seed: object,
    width: object,
    height: object,
    scheduler: object,
    *,
    model: str,
    device: str,
    local_files_only: bool,
) -> tuple[Any, dict[str, object]]:
    try:
        request = validate_request(
            prompt,
            negative_prompt,
            style,
            steps,
            guidance_scale,
            seed,
            width,
            height,
            scheduler,
        )
        with PIPELINE_LOCK:
            pipeline = load_pipeline(model, device, local_files_only)
            apply_style(pipeline, request.style)
            scheduler_type = SCHEDULERS[request.scheduler]
            pipeline.scheduler = scheduler_type.from_config(BASE_SCHEDULER_CONFIG)
            generator_device = "cuda" if PIPELINE_DEVICE == "cuda" else "cpu"
            generator = torch.Generator(device=generator_device).manual_seed(request.seed)
            with torch.inference_mode():
                result = pipeline(
                    prompt=request.prompt,
                    negative_prompt=request.negative_prompt,
                    num_inference_steps=request.steps,
                    guidance_scale=request.guidance_scale,
                    width=request.width,
                    height=request.height,
                    generator=generator,
                )
    except Exception as error:  # noqa: BLE001 - present local runtime errors in the GUI
        raise gr.Error(str(error)) from error

    safety = getattr(result, "nsfw_content_detected", None)
    metadata: dict[str, object] = {
        **asdict(request),
        "model": model,
        "device": PIPELINE_DEVICE,
        "nsfw_content_detected": safety[0] if isinstance(safety, list) and safety else None,
    }
    return result.images[0], metadata


def build_app(model: str, device: str, local_files_only: bool) -> gr.Blocks:
    with gr.Blocks(title="Clover Image Tiny") as demo:
        gr.HTML(
            """
            <section class="hero">
              <small>Local text-to-image</small>
              <h1>Clover Image Tiny</h1>
              <p>A compact Stable Diffusion 1.4-class model with optional named
              style LoRAs. The checkpoint downloads from Hugging Face on first use,
              then remains available from the local cache.</p>
              <div class="stats">
                <div class="stat"><strong>512 × 512</strong><span>reference resolution</span></div>
                <div class="stat"><strong>4–100</strong><span>inference steps</span></div>
                <div class="stat"><strong>Local</strong><span>CUDA, MPS, or CPU</span></div>
              </div>
            </section>
            """
        )
        with gr.Row(equal_height=False):
            with gr.Column(scale=5):
                prompt = gr.Textbox(
                    label="Prompt",
                    value="a tiny glass greenhouse glowing in a moonlit garden",
                    lines=3,
                )
                negative_prompt = gr.Textbox(
                    label="Negative prompt", value=DEFAULT_NEGATIVE_PROMPT, lines=2
                )
                style = gr.Dropdown(list(STYLES), value="Clover", label="Style")
                hint = gr.Markdown(style_hint("Clover"))
                with gr.Row():
                    steps = gr.Slider(4, 100, value=50, step=1, label="Steps")
                    guidance = gr.Slider(0, 20, value=7.5, step=0.5, label="Guidance")
                with gr.Row():
                    seed = gr.Number(value=1337, precision=0, label="Seed")
                    scheduler = gr.Dropdown(list(SCHEDULERS), value="PNDM", label="Scheduler")
                with gr.Row():
                    width = gr.Dropdown([256, 320, 384, 448, 512, 576, 640, 704, 768], value=512, label="Width")
                    height = gr.Dropdown([256, 320, 384, 448, 512, 576, 640, 704, 768], value=512, label="Height")
                run = gr.Button("Generate", variant="primary")
            with gr.Column(scale=7):
                output = gr.Image(label="Generated image", type="pil", elem_id="output-image")
                metadata = gr.JSON(label="Generation details", elem_id="metadata")

        style.change(style_hint, style, hint)
        run.click(
            lambda *values: generate(
                *values,
                model=model,
                device=device,
                local_files_only=local_files_only,
            ),
            [prompt, negative_prompt, style, steps, guidance, seed, width, height, scheduler],
            [output, metadata],
            concurrency_limit=1,
        )
    return demo


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL_ID)
    parser.add_argument("--device", choices=("auto", "cuda", "mps", "cpu"), default="auto")
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--share", action="store_true")
    args = parser.parse_args()

    build_app(args.model, args.device, args.local_files_only).queue(
        default_concurrency_limit=1
    ).launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        theme=gr.themes.Base(primary_hue="green", neutral_hue="slate"),
        css=APP_CSS,
    )


if __name__ == "__main__":
    main()
