#!/usr/bin/env python3
"""Generate images with the Clover Image Tiny public release."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

import torch
from diffusers import (
    DDIMScheduler,
    DiffusionPipeline,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    PNDMScheduler,
)

DEFAULT_STEPS = 50
DEFAULT_GUIDANCE_SCALE = 7.5
DEFAULT_RESOLUTION = 512
DEFAULT_MODEL = "neonforestmist/Clover-Image-Tiny"
MIN_STEPS = 4
MAX_STEPS = 100
MIN_RESOLUTION = 256
MAX_RESOLUTION = 768
RESOLUTION_MULTIPLE = 64
MAX_IMAGES = 4
MAX_TEXT_LENGTH = 2_000
MAX_SEED = 2**63 - 1
SCHEDULERS: dict[str, type[Any]] = {
    "pndm": PNDMScheduler,
    "ddim": DDIMScheduler,
    "euler": EulerDiscreteScheduler,
    "euler-a": EulerAncestralDiscreteScheduler,
    "dpmpp-2m": DPMSolverMultistepScheduler,
}


def _runtime(requested: str) -> tuple[torch.device, torch.dtype]:
    if requested == "auto":
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
    else:
        device = torch.device(requested)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is unavailable")
    if device.type == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("MPS was requested but is unavailable")
    dtype = torch.float16 if device.type in {"cuda", "mps"} else torch.float32
    return device, dtype


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Clover Image Tiny with configurable conventional Diffusers settings. "
            "The defaults reproduce the validated 50-step reference recipe."
        )
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Hub repository ID or local directory (default: %(default)s)",
    )
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument(
        "--steps",
        type=int,
        default=DEFAULT_STEPS,
        help=f"requested inference steps ({MIN_STEPS}..{MAX_STEPS})",
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=DEFAULT_GUIDANCE_SCALE,
        help="classifier-free guidance scale (0.0..20.0)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=DEFAULT_RESOLUTION,
        help=(
            f"output width ({MIN_RESOLUTION}..{MAX_RESOLUTION}, multiple of {RESOLUTION_MULTIPLE})"
        ),
    )
    parser.add_argument(
        "--height",
        type=int,
        default=DEFAULT_RESOLUTION,
        help=(
            f"output height ({MIN_RESOLUTION}..{MAX_RESOLUTION}, multiple of {RESOLUTION_MULTIPLE})"
        ),
    )
    parser.add_argument(
        "--scheduler",
        choices=tuple(SCHEDULERS),
        default="pndm",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=1,
        help=f"number of images (1..{MAX_IMAGES}); seeds increment from --seed",
    )
    parser.add_argument("--output", type=Path, default=Path("clover-image-tiny.png"))
    parser.add_argument("--device", choices=("auto", "cuda", "mps", "cpu"), default="auto")
    parser.add_argument("--local-files-only", action="store_true")
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if not isinstance(args.prompt, str) or not args.prompt.strip():
        raise ValueError("--prompt must not be empty")
    if len(args.prompt) > MAX_TEXT_LENGTH:
        raise ValueError(f"--prompt must contain at most {MAX_TEXT_LENGTH} characters")
    if len(args.negative_prompt) > MAX_TEXT_LENGTH:
        raise ValueError(f"--negative-prompt must contain at most {MAX_TEXT_LENGTH} characters")
    if not MIN_STEPS <= args.steps <= MAX_STEPS:
        raise ValueError(f"--steps must be between {MIN_STEPS} and {MAX_STEPS}")
    if not math.isfinite(args.guidance_scale) or not 0.0 <= args.guidance_scale <= 20.0:
        raise ValueError("--guidance-scale must be finite and between 0.0 and 20.0")
    for name in ("width", "height"):
        value = int(getattr(args, name))
        if not MIN_RESOLUTION <= value <= MAX_RESOLUTION or value % RESOLUTION_MULTIPLE != 0:
            raise ValueError(
                f"--{name} must be between {MIN_RESOLUTION} and {MAX_RESOLUTION} "
                f"and divisible by {RESOLUTION_MULTIPLE}"
            )
    if not 1 <= args.num_images <= MAX_IMAGES:
        raise ValueError(f"--num-images must be between 1 and {MAX_IMAGES}")
    if not 0 <= args.seed <= MAX_SEED or args.seed + args.num_images - 1 > MAX_SEED:
        raise ValueError("--seed and all incremented image seeds must be in [0, 2**63)")
    if args.output.suffix.lower() != ".png":
        raise ValueError("--output must use a .png filename")


def _output_paths(output: Path, count: int) -> tuple[list[Path], Path]:
    images = [output]
    images.extend(
        output.with_name(f"{output.stem}-{index:02d}{output.suffix}")
        for index in range(2, count + 1)
    )
    return images, output.with_suffix(output.suffix + ".json")


def _write_new(path: Path, payload: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(payload)


def main() -> int:
    parser = _parser()
    args = parser.parse_args()
    try:
        _validate_args(args)
    except ValueError as exc:
        parser.error(str(exc))
    device, dtype = _runtime(args.device)
    output_paths, metadata_path = _output_paths(args.output, args.num_images)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for path in (*output_paths, metadata_path):
        if path.exists() or path.is_symlink():
            raise FileExistsError(f"planned output already exists: {path}")
    pipe = DiffusionPipeline.from_pretrained(
        args.model,
        torch_dtype=dtype,
        local_files_only=args.local_files_only,
    )
    scheduler_type = SCHEDULERS[args.scheduler]
    pipe.scheduler = scheduler_type.from_config(pipe.scheduler.config)
    pipe = pipe.to(device)
    generator_device = "cuda" if device.type == "cuda" else "cpu"
    seeds = [args.seed + index for index in range(args.num_images)]
    generators = [torch.Generator(device=generator_device).manual_seed(seed) for seed in seeds]
    generator: torch.Generator | list[torch.Generator]
    generator = generators[0] if len(generators) == 1 else generators
    with torch.inference_mode():
        result = pipe(
            prompt=args.prompt.strip(),
            negative_prompt=args.negative_prompt,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance_scale,
            height=args.height,
            width=args.width,
            num_images_per_prompt=args.num_images,
            generator=generator,
        )
    if not isinstance(result.images, list) or len(result.images) != args.num_images:
        raise RuntimeError("the pipeline returned an unexpected number of images")
    safety = getattr(result, "nsfw_content_detected", None)
    if not isinstance(safety, list) or len(safety) != args.num_images:
        raise RuntimeError("the pipeline returned an unexpected safety-check result")
    image_records: list[dict[str, Any]] = []
    image_payloads: list[bytes] = []
    for image, output_path, seed, nsfw in zip(
        result.images,
        output_paths,
        seeds,
        safety,
        strict=True,
    ):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        payload = buffer.getvalue()
        image_payloads.append(payload)
        image_records.append(
            {
                "filename": output_path.name,
                "seed": seed,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "nsfw_content_detected": nsfw,
            }
        )
    validated_gallery_recipe = (
        args.scheduler == "pndm"
        and args.steps == DEFAULT_STEPS
        and args.guidance_scale == DEFAULT_GUIDANCE_SCALE
        and args.negative_prompt == ""
        and args.width == DEFAULT_RESOLUTION
        and args.height == DEFAULT_RESOLUTION
        and args.num_images == 1
    )
    metadata = {
        "model": args.model,
        "prompt": args.prompt.strip(),
        "negative_prompt": args.negative_prompt,
        "seed": args.seed,
        "scheduler": type(pipe.scheduler).__name__,
        "scheduler_key": args.scheduler,
        "num_inference_steps": args.steps,
        "guidance_scale": args.guidance_scale,
        "height": args.height,
        "width": args.width,
        "num_images": args.num_images,
        "images": image_records,
        "device": device.type,
        "dtype": str(dtype).removeprefix("torch."),
        "nsfw_content_detected": safety,
        "validated_gallery_recipe": validated_gallery_recipe,
        "leaf_steps": None,
        "cross_device_pixel_identity_claimed": False,
    }
    for output_path, payload in zip(output_paths, image_payloads, strict=True):
        _write_new(output_path, payload)
    _write_new(metadata_path, (json.dumps(metadata, indent=2) + "\n").encode("utf-8"))
    print(
        json.dumps(
            {
                "output": str(output_paths[0]),
                "outputs": [str(path) for path in output_paths],
                "metadata": str(metadata_path),
                **metadata,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
