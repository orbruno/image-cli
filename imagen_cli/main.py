#!/usr/bin/env python3
"""
Imagen CLI - Generate images using Google's Imagen models via Gemini API
"""

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

import click
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

from . import __version__


@dataclass(frozen=True)
class ModelSpec:
    name: str
    description: str
    use_case: str
    max_refs: int
    max_resolution: str


MODELS: dict[str, ModelSpec] = {
    "flash": ModelSpec(
        name="gemini-2.5-flash-image",
        description="Fast Gemini Image generation (Nano Banana)",
        use_case="Quick iterations, testing, rapid prototyping",
        max_refs=0,
        max_resolution="2K",
    ),
    "pro": ModelSpec(
        name="gemini-3-pro-image-preview",
        description="Professional Gemini Image with editing (Nano Banana Pro)",
        use_case="Finals, editing, reference images, professional work",
        max_refs=14,
        max_resolution="4K",
    ),
}

# All valid model identifiers (short aliases + full model names)
VALID_MODEL_CHOICES = list(MODELS.keys()) + [m.name for m in MODELS.values()]


class ApiKeyNotFoundError(RuntimeError):
    """Raised when no Google AI API key is found in environment."""


@dataclass(frozen=True)
class GenerationResult:
    prompt: str
    model_name: str
    aspect_ratio: str
    size: str
    reference_images: tuple[str, ...]


def get_api_key() -> str:
    """Get Google AI API key from environment.

    Raises:
        ApiKeyNotFoundError: If no API key is found in environment variables.
    """
    api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ApiKeyNotFoundError(
            "GOOGLE_AI_API_KEY not found in environment variables.\n"
            "\nPlease set your API key:\n"
            '  export GOOGLE_AI_API_KEY="your-api-key-here"\n'
            "\nOr create a .env file in your project directory.\n"
            "Get your key from: https://makersuite.google.com/app/apikey"
        )
    return api_key


def detect_project_context() -> Path:
    """Detect if we're in a known project and suggest appropriate save location."""
    cwd = Path.cwd()

    if "Turri.cr" in str(cwd):
        if "Mercadeo" in str(cwd):
            return cwd / "generated-images"
        elif "Productos" in str(cwd) or "Productores" in str(cwd):
            return cwd / "Fotos"
        else:
            return cwd / "generated-images"

    return cwd


def generate_filename(prompt: str, extension: str = "png", has_reference: bool = False) -> str:
    """Generate a filename based on prompt and timestamp."""
    words = prompt.lower().split()[:4]
    cleaned_words = [
        "".join(c for c in word if c.isalnum()) for word in words
    ]
    prompt_slug = "-".join(cleaned_words)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    prefix = "imagen-edit" if has_reference else "imagen"

    return f"{prefix}_{prompt_slug}_{timestamp}.{extension}"


def ask_save_location(suggested_path: Path) -> Path:
    """Interactive prompt for save location."""
    click.echo(f"\nSuggested location: {suggested_path}")
    response = click.prompt(
        "Save here? (y/n) or enter custom path",
        type=str,
        default="y",
    )

    if response.lower() in ["y", "yes"]:
        return suggested_path
    elif response.lower() in ["n", "no"]:
        custom_path = click.prompt("Enter save path", type=click.Path())
        return Path(custom_path)
    else:
        return Path(response)


def resolve_model_name(model: str) -> str:
    """Resolve a model alias to its full model name."""
    spec = MODELS.get(model)
    if spec:
        return spec.name
    return model


def load_reference_images(
    reference_paths: tuple[str, ...],
    model_key: str,
) -> tuple[list[Image.Image], tuple[str, ...]]:
    """Load and validate reference images for the given model.

    Returns:
        Tuple of (loaded PIL images, filtered reference paths actually used)
    """
    if not reference_paths:
        return [], ()

    click.echo(f"Reference images: {len(reference_paths)}")

    spec = MODELS.get(model_key)
    max_refs = spec.max_refs if spec else 0

    if max_refs == 0:
        click.echo(f"Warning: Model '{model_key}' doesn't support reference images. Use --model pro instead.")
        click.echo("Generating without references...")
        return [], ()

    if len(reference_paths) > max_refs:
        click.echo(f"Warning: Model '{model_key}' supports max {max_refs} references, you provided {len(reference_paths)}.")
        click.echo(f"Using first {max_refs} images...")
        reference_paths = reference_paths[:max_refs]

    loaded: list[Image.Image] = []
    for ref_path in reference_paths:
        try:
            ref_img = Image.open(ref_path)
            loaded.append(ref_img)
            click.echo(f"  Loaded: {ref_path}")
        except (OSError, Image.UnidentifiedImageError) as e:
            click.echo(f"  Warning: Could not load {ref_path}: {e}", err=True)

    return loaded, reference_paths


def call_generation_api(
    client: genai.Client,
    model_name: str,
    prompt: str,
    ref_imgs: list[Image.Image],
    aspect_ratio: str,
    size: str,
) -> Image.Image:
    """Call the Gemini Image API and return the generated PIL Image.

    Raises:
        ValueError: If no image is generated or found in the response.
    """
    click.echo("\nGenerating image...")

    contents: list = []
    if ref_imgs:
        contents.extend(ref_imgs)
    contents.append(prompt)

    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=size,
        )
    )

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config
    )

    if not response or not hasattr(response, 'candidates') or not response.candidates:
        raise ValueError("No content generated by the API")

    for part in response.parts:
        if part.inline_data is not None:
            return part.as_image()

    raise ValueError("No image found in API response")


def resolve_save_path(
    output: str | None,
    prompt: str,
    has_reference: bool,
    ask_location: bool,
) -> Path:
    """Determine where to save the generated image."""
    if output:
        return Path(output)

    suggested_dir = detect_project_context()
    filename = generate_filename(prompt, has_reference=has_reference)
    save_path = suggested_dir / filename

    if ask_location:
        save_path = ask_save_location(save_path)

    return save_path


def save_image(image: Image.Image, save_path: Path) -> None:
    """Save a PIL Image to disk, creating parent directories as needed.

    Raises:
        OSError: If the image cannot be written to disk.
    """
    save_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(str(save_path))


def generate_metadata_file(image_path: Path, result: GenerationResult) -> Path | None:
    """Generate accessibility metadata file for the image."""
    metadata_path = image_path.parent / f"{image_path.stem}-metadata.md"

    alt_text = result.prompt[:100] + "..." if len(result.prompt) > 100 else result.prompt
    caption = result.prompt.split('.')[0] if '.' in result.prompt else result.prompt[:80]
    ref_list = "\n".join([f"- `{Path(ref).name}`" for ref in result.reference_images]) if result.reference_images else "- None"

    metadata_content = f"""# Image Metadata

**File**: `{image_path.name}`
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model**: {result.model_name}
**Resolution**: {result.size}
**Aspect Ratio**: {result.aspect_ratio}

---

## Generation Prompt

```
{result.prompt}
```

---

## Accessibility Metadata

### Alt Text (Suggested)

```
{alt_text}
```

### Caption (Suggested)

```
{caption}
```

### Long Description

```
A generated image based on the prompt: "{result.prompt}". Created using Google Gemini Image ({result.model_name}) at {result.size} resolution with {result.aspect_ratio} aspect ratio.
```

---

## Reference Images

{ref_list}

---

## Usage Notes

- **Purpose**: [Add intended use - e.g., product photo, marketing banner, social media]
- **Context**: [Add context about where this will be used]
- **Edits Needed**: [Note any manual edits or adjustments needed]

---

**Metadata Version**: 1.0
**Tool**: imagen-cli v{__version__}
"""

    try:
        metadata_path.write_text(metadata_content, encoding='utf-8')
        return metadata_path
    except OSError as e:
        click.echo(f"Warning: Could not create metadata file: {e}", err=True)
        return None


def display_model_list() -> None:
    """Display available models and exit."""
    click.echo("Available Imagen Models:\n")
    for key, spec in MODELS.items():
        click.echo(f"  {key}")
        click.echo(f"    Full name: {spec.name}")
        click.echo(f"    Description: {spec.description}")
        click.echo(f"    Best for: {spec.use_case}")
        click.echo()
    click.echo("Usage: genimg \"prompt\" --model [model-name]")
    click.echo("Example: genimg \"a sunset\" --model pro")


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file path (auto-generated if not specified)",
)
@click.option(
    "-r",
    "--reference",
    "reference_images",
    type=click.Path(exists=True),
    multiple=True,
    help="Reference image(s) for style/content guidance (can specify multiple)",
)
@click.option(
    "--edit-mode",
    type=click.Choice(["reference", "inpaint", "outpaint"]),
    default="reference",
    help="How to use reference images (reference=style guide, inpaint=edit parts, outpaint=extend)",
)
@click.option(
    "--model",
    type=click.Choice(VALID_MODEL_CHOICES),
    default="pro",
    help="Gemini Image model: flash (fast) or pro (with editing support)",
)
@click.option(
    "--ask",
    is_flag=True,
    help="Always ask for save location",
)
@click.option(
    "--aspect-ratio",
    type=click.Choice(["1:1", "16:9", "9:16", "4:3", "3:4"]),
    default="1:1",
    help="Aspect ratio for generated image",
)
@click.option(
    "--size",
    type=click.Choice(["1K", "2K", "4K"]),
    default="2K",
    help="Image size: 1K, 2K (both models), or 4K (Pro model only)",
)
@click.option(
    "--person-generation",
    type=click.Choice(["dont_allow", "allow_adult", "allow_all"]),
    default="allow_adult",
    help="Control people in images: dont_allow (no people), allow_adult (adults only), allow_all (all ages)",
)
@click.option(
    "--no-people",
    is_flag=True,
    help="Shortcut for --person-generation dont_allow",
)
@click.option(
    "--list-models",
    is_flag=True,
    help="List all available Imagen models and exit",
)
@click.version_option(version=__version__, prog_name="imagen-cli")
def cli(
    prompt: str | None,
    output: str | None,
    reference_images: tuple[str, ...],
    edit_mode: str,
    model: str,
    ask: bool,
    aspect_ratio: str,
    size: str,
    person_generation: str,
    no_people: bool,
    list_models: bool,
) -> None:
    """
    Generate and edit images using Google's Gemini Image models (Nano Banana).

    Examples:

        genimg "a sunset over mountains"

        genimg "a cat wearing sunglasses" -o ~/Desktop/cool-cat.png

        genimg "abstract art" --model pro --size 4K

        genimg "futuristic city" --ask

        genimg "pristine landscape" --no-people

        genimg "make it more vibrant" -r photo.jpg

        genimg "in watercolor style" -r reference1.jpg -r reference2.jpg

        genimg "combine these images" -r img1.jpg -r img2.jpg -r img3.jpg --model pro
    """
    load_dotenv()

    if list_models:
        display_model_list()
        sys.exit(0)

    if not prompt:
        click.echo("Error: Missing required argument 'PROMPT'", err=True)
        click.echo("Try 'genimg --help' for usage information", err=True)
        sys.exit(1)

    try:
        api_key = get_api_key()
    except ApiKeyNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    model_name = resolve_model_name(model)
    resolved_person_generation = "dont_allow" if no_people else person_generation

    # Validate 4K only for Pro model
    resolved_size = size
    if size == "4K" and model not in ["pro", "gemini-3-pro-image-preview"]:
        click.echo("Warning: 4K only supported for Pro model. Using 2K instead.")
        resolved_size = "2K"

    click.echo(f"Generating image with prompt: '{prompt}'")
    click.echo(f"Model: {model_name}")
    click.echo(f"Aspect ratio: {aspect_ratio}")
    click.echo(f"Size: {resolved_size}")
    click.echo(f"Person generation: {resolved_person_generation}")

    ref_imgs, used_refs = load_reference_images(reference_images, model)

    try:
        generated_image = call_generation_api(
            client, model_name, prompt, ref_imgs, aspect_ratio, resolved_size
        )
    except ValueError as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)

    save_path = resolve_save_path(output, prompt, bool(ref_imgs), ask)

    try:
        click.echo(f"\nSaving image to: {save_path}")
        save_image(generated_image, save_path)
    except OSError as e:
        click.echo(f"\nError saving image: {e}", err=True)
        sys.exit(1)

    click.echo("✓ Image saved successfully!")
    click.echo(f"  Location: {save_path.absolute()}")

    result = GenerationResult(
        prompt=prompt,
        model_name=model_name,
        aspect_ratio=aspect_ratio,
        size=resolved_size,
        reference_images=used_refs,
    )
    metadata_path = generate_metadata_file(save_path, result)

    if metadata_path:
        click.echo("✓ Metadata file created!")
        click.echo(f"  Location: {metadata_path.absolute()}")


if __name__ == "__main__":
    cli()
