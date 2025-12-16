# Quick Start Guide - Imagen CLI

## Installation (One-time setup)

```bash
cd ~/Documents/Dev-Tools/imagen-cli
./install.sh
```

**OR manually:**

```bash
cd ~/Documents/Dev-Tools/imagen-cli
uv sync
uv pip install -e .
```

## Setup API Key

Get your key from: https://makersuite.google.com/app/apikey

**Add to your shell profile** (`~/.zshrc` or `~/.bashrc`):

```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

Then reload:
```bash
source ~/.zshrc
```

## Usage

### Quick Info

```bash
genimg --list-models  # Show available Imagen models
genimg --version      # Show version
genimg --help         # Show all options
```

### Basic Commands

**Text-to-Image Generation:**
```bash
# Generate image in current directory
genimg "a sunset over mountains"

# Generate with specific output path
genimg "a cat wearing sunglasses" -o ~/Desktop/cat.png

# Ask where to save
genimg "abstract art" --ask

# High-quality 2K image
genimg "photorealistic portrait" --model ultra --size 2K

# Different aspect ratios
genimg "wide landscape" --aspect-ratio 16:9
genimg "phone wallpaper" --aspect-ratio 9:16

# Control people in images
genimg "pristine wilderness" --no-people
genimg "family portrait" --person-generation allow_all
```

**Image Editing with Reference:**
```bash
# Edit an existing image
genimg "make it more vibrant" -r photo.jpg

# Use multiple reference images for style
genimg "in watercolor style" -r style-ref.jpg -r photo.jpg

# Edit specific parts (inpainting)
genimg "change sky to sunset" -r base.jpg --edit-mode inpaint

# Extend image (outpainting)
genimg "expand background" -r small.jpg --edit-mode outpaint
```

### Smart Context-Aware Saving

When in a Turri.cr project:
- In `Mercadeo/` → saves to `generated-images/`
- In `Productos/` → saves to `Fotos/`
- In `Productores/` → saves to `Fotos/`

### Available Options

| Option | Values | Description |
|--------|--------|-------------|
| `-r, --reference` | File path | Reference image(s) for editing (can use multiple) |
| `--edit-mode` | `reference`, `inpaint`, `outpaint` | How to use reference images |
| `--model` | `fast`, `standard`, `ultra`, `imagen3` | Model quality tier |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | Image dimensions |
| `--size` | `1K` (default), `2K` | Image resolution (Standard/Ultra only) |
| `--person-generation` | `dont_allow`, `allow_adult`, `allow_all` | Control people in images |
| `--no-people` | Flag | Shortcut for no people |
| `-o, --output` | File path | Custom save location |
| `--ask` | Flag | Always prompt for location |

### Models

- **fast** (`imagen-3.0-fast-generate-001`) - Faster, good quality
- **generate** (`imagen-3.0-generate-001`) - Slower, higher quality

## Examples for Turri

### Product Photography
```bash
# Generate product photo
cd ~/Documents/Emprendedurismo/Turri.cr/Productos/Cafe-Organico
genimg "artisan coffee beans in rustic setting" --model generate

# Enhance existing product photo
cd ~/Documents/Emprendedurismo/Turri.cr/Productos/Queso-Artesanal
genimg "make lighting more professional" -r existing-photo.jpg --model generate

# Change background of product
genimg "place on rustic wooden table" -r product-photo.jpg --edit-mode inpaint
```

### Marketing Materials
```bash
# Generate marketing material
cd ~/Documents/Emprendedurismo/Turri.cr/Mercadeo/Campañas/2025-Q1
genimg "Costa Rican countryside with farmers" --aspect-ratio 16:9

# Create variations from existing design
genimg "in warmer tones with sunset lighting" -r base-design.jpg

# Extend banner image
genimg "extend landscape to sides" -r banner.jpg --edit-mode outpaint --aspect-ratio 16:9
```

### Producer Content
```bash
# Generate producer photos
cd ~/Documents/Emprendedurismo/Turri.cr/Relaciones/Productores/[Nombre]
genimg "portrait of artisan producer in workshop" --ask

# Enhance existing producer photo
genimg "improve lighting and color" -r producer-photo.jpg --model generate

# Create styled version
genimg "in documentary photography style" -r original.jpg
```

## Tips

### General Usage
1. **Be specific in prompts** - Better results with detailed descriptions
2. **Use `--ask` for important images** - Choose exact location
3. **Project context detection** - CLI detects Turri folders automatically
4. **Quality vs Speed** - Use `--model generate` for final/important images
5. **Aspect ratios** - Match your use case (social media, website, etc.)

### Working with Reference Images
6. **Reference mode** - Use for style transfer and general enhancements
7. **Inpaint mode** - Best for replacing/editing specific elements
8. **Outpaint mode** - Extend images beyond their original boundaries
9. **Multiple references** - Combine style reference + content image for best results
10. **Clear edits** - Be specific about what to change when editing (e.g., "make sky more blue" vs "improve it")

## Troubleshooting

### Command not found
```bash
cd ~/Documents/Dev-Tools/imagen-cli
uv pip install -e .
```

### API key not found
```bash
echo $GOOGLE_AI_API_KEY  # Should print your key
source ~/.zshrc          # Reload if just added
```

### Permission errors
The tool creates directories automatically if they don't exist.

---

**More info**: See README.md and INSTALL.md
