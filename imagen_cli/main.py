#!/usr/bin/env python3
"""
Imagen CLI - Generate images using Google's Imagen models via Gemini API
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import click
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

from . import __version__

# Load environment variables
load_dotenv()

# Available Gemini Image models (Nano Banana)
IMAGEN_MODELS = {
    "flash": "gemini-2.5-flash-image",
    "pro": "gemini-3-pro-image-preview",
}

# Model descriptions
MODEL_INFO = {
    "flash": {
        "name": "gemini-2.5-flash-image",
        "description": "Fast Gemini Image generation (Nano Banana)",
        "use_case": "Quick iterations, testing, rapid prototyping",
        "max_refs": 0,
        "max_resolution": "2K"
    },
    "pro": {
        "name": "gemini-3-pro-image-preview",
        "description": "Professional Gemini Image with editing (Nano Banana Pro)",
        "use_case": "Finals, editing, reference images, professional work",
        "max_refs": 14,
        "max_resolution": "4K"
    }
}

# Aspect ratio mapping
ASPECT_RATIOS = {
    "1:1": "1:1",
    "16:9": "16:9",
    "9:16": "9:16",
    "4:3": "4:3",
    "3:4": "3:4"
}


def get_api_key() -> str:
    """Get Google AI API key from environment."""
    api_key = os.getenv("GOOGLE_AI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        click.echo(
            "Error: GOOGLE_AI_API_KEY not found in environment variables.",
            err=True,
        )
        click.echo(
            "\nPlease set your API key:",
            err=True,
        )
        click.echo(
            '  export GOOGLE_AI_API_KEY="your-api-key-here"',
            err=True,
        )
        click.echo(
            "\nOr create a .env file in ~/Documents/Dev-Tools/imagen-cli/",
            err=True,
        )
        click.echo(
            "Get your key from: https://makersuite.google.com/app/apikey",
            err=True,
        )
        sys.exit(1)
    return api_key


def detect_project_context() -> Path:
    """Detect if we're in a known project and suggest appropriate save location."""
    cwd = Path.cwd()

    # Check if in Turri project
    if "Turri.cr" in str(cwd):
        # Suggest different locations based on subdirectory
        if "Mercadeo" in str(cwd):
            return cwd / "generated-images"
        elif "Productos" in str(cwd):
            return cwd / "Fotos"
        elif "Productores" in str(cwd):
            return cwd / "Fotos"
        else:
            return cwd / "generated-images"

    # Default to current directory
    return cwd


def generate_filename(prompt: str, extension: str = "png", has_reference: bool = False) -> str:
    """Generate a filename based on prompt and timestamp."""
    # Take first few words of prompt, clean them up
    words = prompt.lower().split()[:4]
    cleaned_words = [
        "".join(c for c in word if c.isalnum()) for word in words
    ]
    prompt_slug = "-".join(cleaned_words)

    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Indicate if reference image was used
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


def generate_metadata_file(
    image_path: Path,
    prompt: str,
    model_name: str,
    aspect_ratio: str,
    size: str,
    reference_images: tuple[str, ...]
) -> Path | None:
    """Generate accessibility metadata file for the image."""
    metadata_path = image_path.parent / f"{image_path.stem}-metadata.md"

    # Generate alt text suggestion (shortened prompt)
    alt_text = prompt[:100] + "..." if len(prompt) > 100 else prompt

    # Generate caption (first sentence or shortened prompt)
    caption = prompt.split('.')[0] if '.' in prompt else prompt[:80]

    # Build reference images list
    ref_list = "\n".join([f"- `{Path(ref).name}`" for ref in reference_images]) if reference_images else "- None"

    metadata_content = f"""# Image Metadata

**File**: `{image_path.name}`
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model**: {model_name}
**Resolution**: {size}
**Aspect Ratio**: {aspect_ratio}

---

## Generation Prompt

```
{prompt}
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
A generated image based on the prompt: "{prompt}". Created using Google Gemini Image ({model_name}) at {size} resolution with {aspect_ratio} aspect ratio.
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
**Tool**: imagen-cli v0.6.0
"""

    try:
        metadata_path.write_text(metadata_content, encoding='utf-8')
        return metadata_path
    except Exception as e:
        click.echo(f"Warning: Could not create metadata file: {e}", err=True)
        return None


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
    type=click.Choice(list(IMAGEN_MODELS.keys()) + list(IMAGEN_MODELS.values())),
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
@click.option(
    "--version",
    is_flag=True,
    help="Show version and exit",
)
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
    version: bool
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
    # Handle --version flag
    if version:
        click.echo(f"imagen-cli version {__version__}")
        click.echo("Google Gemini Image (Nano Banana) generation and editing tool")
        sys.exit(0)

    # Handle --list-models flag
    if list_models:
        click.echo("Available Imagen Models:\n")
        for key, info in MODEL_INFO.items():
            click.echo(f"  {key}")
            click.echo(f"    Full name: {info['name']}")
            click.echo(f"    Description: {info['description']}")
            click.echo(f"    Best for: {info['use_case']}")
            click.echo()
        click.echo("Usage: genimg \"prompt\" --model [model-name]")
        click.echo("Example: genimg \"a sunset\" --model pro")
        sys.exit(0)

    # Require prompt if not using --version or --list-models
    if not prompt:
        click.echo("Error: Missing required argument 'PROMPT'", err=True)
        click.echo("Try 'genimg --help' for usage information", err=True)
        sys.exit(1)

    # Get API key
    api_key = get_api_key()

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Resolve model name
    model_name = IMAGEN_MODELS.get(model, model)

    # Handle --no-people flag
    if no_people:
        person_generation = "dont_allow"

    click.echo(f"Generating image with prompt: '{prompt}'")
    click.echo(f"Model: {model_name}")
    click.echo(f"Aspect ratio: {aspect_ratio}")
    click.echo(f"Size: {size}")
    click.echo(f"Person generation: {person_generation}")

    # Load reference images if provided
    ref_imgs = []
    if reference_images:
        click.echo(f"Reference images: {len(reference_images)}")

        # Check model supports references
        model_info = MODEL_INFO.get(model, {})
        max_refs = model_info.get("max_refs", 0)

        if max_refs == 0:
            click.echo(f"Warning: Model '{model}' doesn't support reference images. Use --model pro instead.")
            click.echo("Generating without references...")
        elif len(reference_images) > max_refs:
            click.echo(f"Warning: Model '{model}' supports max {max_refs} references, you provided {len(reference_images)}.")
            click.echo(f"Using first {max_refs} images...")
            reference_images = reference_images[:max_refs]

        for ref_path in reference_images:
            try:
                ref_img = Image.open(ref_path)
                ref_imgs.append(ref_img)
                click.echo(f"  Loaded: {ref_path}")
            except Exception as e:
                click.echo(f"  Warning: Could not load {ref_path}: {e}", err=True)

    try:
        # Generate image using Gemini Image
        click.echo("\nGenerating image...")

        # Validate 4K only for Pro model
        if size == "4K" and model not in ["pro", "gemini-3-pro-image-preview"]:
            click.echo(f"Warning: 4K only supported for Pro model. Using 2K instead.")
            size = "2K"

        # Build content array (text + optional reference images)
        contents = []

        # Add reference images first if provided
        if ref_imgs:
            contents.extend(ref_imgs)

        # Add the prompt
        contents.append(prompt)

        # Build generation config for Gemini Image
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=size,
            )
        )

        # Generate using Gemini Image API
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config
        )

        # Extract the generated image from response
        if not response or not hasattr(response, 'candidates') or not response.candidates:
            click.echo("Error: No content generated.", err=True)
            sys.exit(1)

        # Find the image part in the response
        generated_image = None
        for part in response.parts:
            if part.inline_data is not None:
                # Convert inline image data to PIL Image
                generated_image = part.as_image()
                break

        if not generated_image:
            click.echo("Error: No image found in response.", err=True)
            sys.exit(1)

        # Determine save location
        if output:
            save_path = Path(output)
        else:
            # Detect project context
            suggested_dir = detect_project_context()
            filename = generate_filename(prompt, has_reference=bool(ref_imgs))
            save_path = suggested_dir / filename

            if ask:
                save_path = ask_save_location(save_path)

        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the image
        click.echo(f"\nSaving image to: {save_path}")

        # The image is already a PIL Image object
        generated_image.save(str(save_path))

        click.echo(f"✓ Image saved successfully!")
        click.echo(f"  Location: {save_path.absolute()}")

        # Generate metadata file for accessibility
        metadata_path = generate_metadata_file(
            save_path,
            prompt,
            model_name,
            aspect_ratio,
            size,
            reference_images
        )

        if metadata_path:
            click.echo(f"✓ Metadata file created!")
            click.echo(f"  Location: {metadata_path.absolute()}")

    except Exception as e:
        click.echo(f"\nError generating image: {str(e)}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
