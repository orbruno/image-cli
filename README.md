# Imagen CLI - Image Generation & Editing Tool

CLI tool for generating and editing images using Google's **Gemini Image** models (code-named "Nano Banana") via the Gemini API.

## ✨ Features

- 🎨 **Generate** images from text prompts
- ✏️ **Edit** existing images with natural language
- 🔀 **Combine** multiple images into one
- 📐 Multiple resolutions: 1K, 2K, **4K** (Pro model)
- 🖼️ Up to **14 reference images** for style and content (Pro model)
- 🎯 Smart save location detection (project-aware)
- ⚡ Two models: Flash (fast) and Pro (professional with editing)
- ♿ **Automatic accessibility metadata** - alt text, captions, long descriptions

## Installation

```bash
cd ~/Documents/Dev-Tools/imagen-cli
uv tool install .
```

This installs the `genimg` command globally.

## Setup

1. Get a Google AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set it as an environment variable:

```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

Or create a `.env` file:

```
GOOGLE_AI_API_KEY=your-api-key-here
```

## Usage

### Info Commands

```bash
genimg --list-models  # Show available models
genimg --version      # Show version
genimg --help         # Show all options
```

### Basic Text-to-Image Generation

```bash
# Simple generation (uses Pro model by default)
genimg "a sunset over mountains"

# Specify model
genimg "abstract art" --model flash

# High-resolution 4K (Pro model only)
genimg "photorealistic landscape" --model pro --size 4K

# Different aspect ratios
genimg "wide banner" --aspect-ratio 16:9
genimg "phone wallpaper" --aspect-ratio 9:16

# Custom output location
genimg "logo design" -o ~/Desktop/logo.png

# Ask where to save
genimg "product photo" --ask
```

### Image Editing with Reference Images ⭐

This is the killer feature that sets Gemini Image apart!

**Edit an existing image:**
```bash
genimg "make the colors more vibrant" -r photo.jpg
genimg "change to vintage 1970s style" -r modern-photo.jpg
```

**Apply style from one image to another:**
```bash
genimg "apply this painting style to this photo" -r monet-painting.jpg -r photo.jpg
```

**Combine multiple images:**
```bash
genimg "combine these into one artistic collage" -r img1.jpg -r img2.jpg -r img3.jpg --model pro
```

**Transform specific elements:**
```bash
genimg "change the background to a mountain landscape" -r portrait.jpg --model pro
genimg "replace the sky with dramatic sunset clouds" -r landscape.jpg
```

**Use up to 14 references (Pro model):**
```bash
genimg "create a composition inspired by all these" \
  -r ref1.jpg -r ref2.jpg -r ref3.jpg -r ref4.jpg \
  --model pro --size 4K
```

### Advanced Controls

**Control people in images:**
```bash
# No people at all
genimg "pristine natural landscape" --no-people

# Adults only (default)
genimg "professional office" --person-generation allow_adult

# All ages
genimg "family gathering" --person-generation allow_all
```

**High-resolution output:**
```bash
# 4K only for Pro model
genimg "detailed architectural photo" --model pro --size 4K
```

## Available Models

| Model | ID | Resolution | Reference Images | Best For |
|-------|-----|-----------|-----------------|----------|
| **flash** | gemini-2.5-flash-image | 1K, 2K | No | Quick iterations, testing |
| **pro** | gemini-3-pro-image-preview | 1K, 2K, **4K** | **Up to 14** | Finals, editing, professional work |

**Default:** Pro model (best quality and supports editing)

## All Options

| Option | Values | Description |
|--------|--------|-------------|
| `-r, --reference` | File path | Reference image(s) - can use multiple times |
| `--model` | `flash`, `pro` | Model to use |
| `--size` | `1K`, `2K`, `4K` | Resolution (4K only for Pro) |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | Image dimensions |
| `--person-generation` | `dont_allow`, `allow_adult`, `allow_all` | Control people |
| `--no-people` | Flag | Shortcut for no people |
| `-o, --output` | Path | Custom save location |
| `--ask` | Flag | Interactively choose save location |
| `--list-models` | Flag | Show available models |
| `--version` | Flag | Show version |
| `--help` | Flag | Show help |

## Smart Save Location

The tool detects your project context:

- In `Mercadeo/` → saves to `generated-images/`
- In `Productos/` → saves to `Fotos/`
- In `Productores/` → saves to `Fotos/`
- Otherwise → current directory

## Accessibility Metadata

**Every generated image automatically includes a metadata file** for accessibility:

When you generate `imagen_sunset_20251126-120000.png`, the tool also creates `imagen_sunset_20251126-120000-metadata.md` with:

- **Alt Text** - Suggested alternative text for screen readers
- **Caption** - Suggested caption text
- **Long Description** - Detailed description for accessibility
- **Generation details** - Prompt, model, resolution, reference images used
- **Usage notes** - Editable fields for context and intended use

This ensures all generated images are ready for accessible web deployment with proper ARIA labels and semantic HTML.

## Examples

### For Turri.cr

**Product Photography:**
```bash
cd ~/Documents/Emprendedurismo/Turri.cr/Productos/Cafe-Organico
genimg "artisan coffee beans on rustic wooden table, professional product photography" \
  --model pro --size 4K --aspect-ratio 1:1 --no-people
```

**Edit Existing Product Photo:**
```bash
genimg "make lighting more professional and warm" -r existing-photo.jpg --model pro
```

**Marketing Banner:**
```bash
cd Mercadeo/Campañas/2025-Q1
genimg "Turrialba countryside with coffee farmers, golden hour" \
  --aspect-ratio 16:9 --model pro --size 2K
```

**Style Transfer:**
```bash
genimg "apply this artistic style to create promotional image" \
  -r brand-style-ref.jpg -r product-photo.jpg --model pro
```

### General Examples

**Quick Iteration:**
```bash
# Test with Flash model
genimg "concept sketch of logo" --model flash

# Refine with Pro
genimg "polished version of logo" --model pro --size 2K
```

**Image Combination:**
```bash
genimg "merge these photos into a before-and-after comparison" \
  -r before.jpg -r after.jpg --model pro --aspect-ratio 16:9
```

**Natural Language Editing:**
```bash
genimg "add snow to this landscape" -r summer-photo.jpg
genimg "make this portrait black and white with film grain" -r color-portrait.jpg
genimg "remove the background and make it pure white" -r product-photo.jpg
```

## What Changed from v0.4.0?

**Major Migration:**
- ✅ Switched from Imagen 4 to **Gemini Image (Nano Banana)**
- ✅ **Full reference image support** (up to 14 images)
- ✅ **Natural language image editing**
- ✅ **4K resolution** support (Pro model)
- ✅ **Image combination** capabilities
- ⚠️ Model names changed: `flash`, `pro` (instead of fast/standard/ultra)
- ⚠️ Default is now `pro` (was `standard`)
- ⚠️ Default size is now `2K` (was `1K`)

## Troubleshooting

### Reference images not working

Make sure you're using the **Pro model**:
```bash
genimg "edit this" -r photo.jpg --model pro
```

Flash model doesn't support reference images.

### 4K not working

4K is only available with Pro model:
```bash
genimg "high-res image" --model pro --size 4K
```

### API Key not found

```bash
# Check if set
echo $GOOGLE_AI_API_KEY

# Set it
export GOOGLE_AI_API_KEY="your-key"

# Or add to ~/.zshrc
echo 'export GOOGLE_AI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

## Pricing

**$0.03 USD per image** (same for both Flash and Pro models)

## Links

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Docs - Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Source Code](~/Documents/Dev-Tools/imagen-cli/)

---

**Author**: Orlando Bruno
**Created**: 2025-11-26
**Version**: 0.5.0
**License**: MIT
