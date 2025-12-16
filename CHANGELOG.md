# Changelog - Imagen CLI

## [0.6.0] - 2025-11-26

### ♿ New Feature: Automatic Accessibility Metadata

**Every generated image now includes accessibility metadata** to ensure web accessibility compliance.

### What's New

**Automatic Metadata Generation:**
- ✅ Creates `[image-name]-metadata.md` file alongside every generated image
- ✅ **Alt Text** - Auto-suggested alternative text for screen readers
- ✅ **Caption** - Auto-suggested caption based on prompt
- ✅ **Long Description** - Detailed accessibility description
- ✅ **Generation Details** - Full prompt, model, resolution, aspect ratio
- ✅ **Reference Images** - List of all reference images used
- ✅ **Usage Notes** - Editable fields for context and intended use

**Benefits:**
- Ready for WCAG 2.1 Level AA compliance
- Easy integration with web accessibility standards
- Structured metadata for CMS and web platforms
- Human-readable Markdown format for easy editing
- Helps with SEO and image discoverability

**Example:**

When you run:
```bash
genimg "a sunset over mountains" --model pro --size 2K
```

Creates:
- `imagen_a-sunset-over-20251126-120000.png` (image)
- `imagen_a-sunset-over-20251126-120000-metadata.md` (accessibility metadata)

**Metadata File Structure:**
```markdown
# Image Metadata

**File**: `imagen_sunset_20251126-120000.png`
**Generated**: 2025-11-26 12:00:00
**Model**: gemini-3-pro-image-preview
**Resolution**: 2K
**Aspect Ratio**: 1:1

## Generation Prompt
[Full prompt here]

## Accessibility Metadata

### Alt Text (Suggested)
[Auto-generated alt text]

### Caption (Suggested)
[Auto-generated caption]

### Long Description
[Detailed description for screen readers]

## Reference Images
- None (or list of files)

## Usage Notes
- **Purpose**: [Editable]
- **Context**: [Editable]
- **Edits Needed**: [Editable]
```

### Changed
- Output now shows both image and metadata file locations
- Metadata creation runs automatically after image save

---

## [0.5.0] - 2025-11-26

### 🚀 MAJOR MIGRATION: Imagen 4 → Gemini Image (Nano Banana)

**Complete platform migration** from Google Imagen 4 to **Gemini Image** (code-named "Nano Banana"). This unlocks powerful new editing and reference capabilities.

### ✨ New Features

**Reference Image Support (Up to 14 Images!):**
- ✅ **Real reference image support** with Pro model
- ✅ Use up to **14 reference images** for style transfer and guidance
- ✅ **Natural language image editing** - "make the sky more dramatic", "change to vintage style"
- ✅ **Image combination** - merge multiple images into one composition
- ✅ **Style transfer** - apply artistic styles from reference images
- ❌ Flash model does NOT support reference images (validation added)

**4K Resolution Support:**
- ✅ **4K generation** available with Pro model
- ✅ Resolution options: 1K, 2K, **4K**
- ✅ Automatic validation (4K only works with Pro model)

**New Model Architecture:**
- **Flash** (`gemini-2.5-flash-image`) - Fast iterations, no reference images
- **Pro** (`gemini-3-pro-image-preview`) - Professional quality, editing, 4K, up to 14 refs

### ⚠️ Breaking Changes

**Model Names Changed:**
- ❌ `fast` (was `imagen-4.0-fast-generate-001`)
- ❌ `standard` (was `imagen-4.0-generate-001`)
- ❌ `ultra` (was `imagen-4.0-ultra-generate-001`)
- ❌ `imagen3` (was `imagen-3.0-generate-002`)
- ✅ `flash` (now `gemini-2.5-flash-image`)
- ✅ `pro` (now `gemini-3-pro-image-preview`)

**Default Settings Changed:**
- Default model: `standard` → **`pro`** (better quality, editing support)
- Default size: `1K` → **`2K`** (better quality)

**API Changes:**
- Switched from Imagen API to Gemini Image API
- Uses `generate_content()` instead of `generate_images()`
- Multimodal content support (images + text)
- Image extraction from `inline_data` in response candidates

### Changed

**Reference Image Workflow:**
- Reference images now ACTUALLY work (previous version had no real implementation)
- Images passed as array before prompt: `[img1, img2, ..., prompt]`
- Automatic validation of model support
- Warning if too many references for model

**CLI Output:**
- Removed `--edit-mode` option (no longer needed with Gemini Image)
- Better error messages for model/reference compatibility
- Shows reference image count and validation warnings

**Examples:**
```bash
# Edit an existing image
genimg "make colors more vibrant" -r photo.jpg --model pro

# Style transfer with multiple references
genimg "apply this painting style to this photo" -r monet.jpg -r photo.jpg --model pro

# High-res 4K generation
genimg "detailed architectural photo" --model pro --size 4K

# Combine multiple images
genimg "combine these into artistic collage" -r img1.jpg -r img2.jpg -r img3.jpg --model pro

# Maximum references (14 images)
genimg "create composition inspired by all these" \
  -r ref1.jpg -r ref2.jpg -r ref3.jpg -r ref4.jpg \
  --model pro --size 4K
```

### Technical Details

**New Dependencies:**
- Uses `google-genai>=0.3.0` package
- Multimodal content generation with `GenerateContentConfig`
- Image config with `ImageGenerationConfig`
- Base64 decoding of inline image data

**API Integration:**
```python
# New Gemini Image API pattern
contents = [image1, image2, ..., "prompt text"]
config = types.GenerateContentConfig(
    response_modalities=["TEXT", "IMAGE"],
    image_config=types.ImageGenerationConfig(
        aspect_ratio=aspect_ratio,
        image_size=size,
    )
)
response = client.models.generate_content(model=model_name, contents=contents, config=config)
```

**Migration Notes:**
- Previous Imagen 4 implementation did NOT support reference images despite having the option
- This version implements ACTUAL reference image support via Gemini Image
- Pro model required for reference images and 4K
- Flash model is faster but more limited

---

## [0.4.0] - 2025-11-26

### Added - Advanced Image Control

**Image Size Control:**
- Added `--size` option to specify image resolution (`1K` or `2K`)
- Only works with Standard and Ultra models (not Fast or Imagen 3)
- Default: 1K for faster generation
- Displays warning if 2K requested with incompatible model

**Person Generation Control:**
- Added `--person-generation` option to control people in images
  - `dont_allow` - No people in generated images
  - `allow_adult` - Adults only (default)
  - `allow_all` - All ages allowed
- Added `--no-people` shortcut flag for `dont_allow` mode

**Display Improvements:**
- Now shows size and person generation settings when generating
- Better parameter visibility in console output

**Examples:**
```bash
# High-resolution image
genimg "landscape" --model ultra --size 2K

# No people in scene
genimg "pristine wilderness" --no-people

# Family-friendly generation
genimg "family portrait" --person-generation allow_all
```

### Changed
- Updated model list display in `--list-models`
- Enhanced help text with new parameter descriptions
- Improved examples in docstring

### Technical Details
- Uses Imagen API's `image_size` parameter
- Uses Imagen API's `person_generation` parameter
- Validates model compatibility for 2K size
- Gracefully handles `--no-people` flag override

---

## [0.2.0] - 2025-11-26

### Added - Image Editing Features

**Reference Image Support:**
- Added `-r, --reference` option to accept one or multiple reference images
- Support for using images as style/content guidance
- Automatic filename prefixing (`imagen-edit_*`) when using reference images

**Edit Modes:**
- `--edit-mode reference` (default) - Use images for style transfer and enhancement
- `--edit-mode inpaint` - Edit specific parts of images
- `--edit-mode outpaint` - Extend images beyond original boundaries

**Documentation:**
- Created comprehensive `IMAGE-EDITING-GUIDE.md`
- Updated all existing docs with image editing examples
- Added Turri-specific workflows for product photo editing
- Enhanced QUICK-START.md with editing examples

**Examples Added:**
```bash
# Basic editing
genimg "make it more vibrant" -r photo.jpg

# Multiple references
genimg "in watercolor style" -r style-ref.jpg -r photo.jpg

# Inpainting
genimg "change sky to sunset" -r base.jpg --edit-mode inpaint

# Outpainting
genimg "extend landscape" -r photo.jpg --edit-mode outpaint --aspect-ratio 16:9
```

### Changed
- Updated `generate_filename()` to indicate edited images
- Enhanced help text with editing examples
- Improved option descriptions

### Technical Details
- Uses Google Generative AI SDK's `reference_images` parameter
- Supports PIL Image loading for reference files
- Validates reference image paths before processing
- Graceful error handling for invalid reference images

---

## [0.1.0] - 2025-11-26

### Initial Release

**Core Features:**
- Text-to-image generation using Imagen 3
- Two model options (fast/generate)
- Smart context-aware save locations
- Turri.cr project integration
- Multiple aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- Interactive save location prompts
- Automatic filename generation

**Documentation:**
- README.md
- INSTALL.md
- QUICK-START.md
- Installation script

**Installation:**
- UV-based package management
- Global `genimg` command
- Environment variable configuration

---

**Version Format**: [Major.Minor.Patch]
- Major: Breaking changes
- Minor: New features (backwards compatible)
- Patch: Bug fixes
