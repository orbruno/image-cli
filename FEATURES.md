# Imagen CLI - Complete Feature Reference

## Quick Command Reference

### Info & Help Commands
```bash
genimg --list-models  # List all available Imagen models
genimg --version      # Show version information
genimg --help         # Show complete help with all options
```

### Text-to-Image Generation
```bash
genimg "your prompt here"
genimg "prompt" --model generate
genimg "prompt" --aspect-ratio 16:9
genimg "prompt" -o ~/Desktop/output.png
genimg "prompt" --ask
```

### Image Editing with References
```bash
# Single reference (style transfer, enhancement)
genimg "make it more vibrant" -r photo.jpg

# Multiple references (combine styles/content)
genimg "in watercolor style" -r style-ref.jpg -r photo.jpg

# Inpainting (edit specific parts)
genimg "change sky to sunset" -r base.jpg --edit-mode inpaint

# Outpainting (extend boundaries)
genimg "extend landscape to sides" -r photo.jpg --edit-mode outpaint --aspect-ratio 16:9
```

---

## All Features

### 1. Text-to-Image Generation
Generate images from text descriptions using Imagen 3.

**Models:**
- `fast` (default) - imagen-3.0-fast-generate-001
- `generate` - imagen-3.0-generate-001 (higher quality)

**Aspect Ratios:**
- `1:1` (square, default)
- `16:9` (wide/landscape)
- `9:16` (tall/portrait)
- `4:3` (standard photo)
- `3:4` (portrait photo)

### 2. Reference Image Mode
Use existing images as style or content references.

**Use Cases:**
- Style transfer (apply artistic styles)
- Image enhancement (improve quality, lighting, colors)
- Creating variations (same subject, different styles)
- Consistency (match style across multiple images)

**How to Use:**
```bash
genimg "your edit description" -r reference-image.jpg
genimg "blend these styles" -r image1.jpg -r image2.jpg -r image3.jpg
```

**Example Prompts:**
- "in watercolor painting style"
- "with professional photography lighting"
- "make colors more vibrant and saturated"
- "in the style of vintage 1970s photography"
- "improve clarity and sharpness"

### 3. Inpaint Mode
Edit or replace specific elements while preserving the rest of the image.

**Use Cases:**
- Background replacement
- Object modification
- Element removal/addition
- Color changes
- Scene context changes

**How to Use:**
```bash
genimg "what to change" -r base-image.jpg --edit-mode inpaint
```

**Example Prompts:**
- "replace background with mountains"
- "change shirt color to blue"
- "replace cloudy sky with sunset"
- "place product on wooden table"
- "remove background, make it white"

### 4. Outpaint Mode
Extend images beyond their original boundaries.

**Use Cases:**
- Format conversion (square → wide banner)
- Adding context around subjects
- Creating different aspect ratios
- Extending backgrounds
- Uncropping tight shots

**How to Use:**
```bash
genimg "how to extend" -r image.jpg --edit-mode outpaint --aspect-ratio [ratio]
```

**Example Prompts:**
- "extend landscape to sides"
- "continue the forest background"
- "expand to show more of the room"
- "extend vertically for full-height banner"

### 5. Smart Save Locations
Automatically detects project context and suggests appropriate save locations.

**Turri.cr Project Detection:**
- In `Mercadeo/` → saves to `generated-images/`
- In `Productos/` → saves to `Fotos/`
- In `Productores/` → saves to `Fotos/`
- Other locations → current directory

**Override Options:**
- `-o PATH` - Specify exact save location
- `--ask` - Always prompt for location interactively

### 6. Automatic Filename Generation
Generates descriptive filenames based on prompt and timestamp.

**Format:**
- Text-to-image: `imagen_prompt-words_YYYYMMDD-HHMMSS.png`
- With reference: `imagen-edit_prompt-words_YYYYMMDD-HHMMSS.png`

**Example:**
```
imagen_sunset-over-mountains_20251126-143022.png
imagen-edit_make-more-vibrant_20251126-143045.png
```

---

## Complete Options Reference

| Option | Values | Description |
|--------|--------|-------------|
| `PROMPT` | Text | Required. Description of image to generate or edit |
| `-o, --output` | File path | Save location (auto-generated if not specified) |
| `-r, --reference` | File path | Reference image (can use multiple times) |
| `--edit-mode` | `reference`, `inpaint`, `outpaint` | How to use reference images |
| `--model` | `fast`, `generate` | Model quality (fast=default, generate=higher quality) |
| `--aspect-ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | Output image dimensions |
| `--ask` | Flag | Always prompt for save location |
| `--help` | Flag | Show help message |

---

## Common Workflows

### Product Photography Enhancement
```bash
# Basic generation
genimg "artisan coffee beans on rustic table" --model generate

# Enhance existing photo
genimg "professional product lighting" -r raw-photo.jpg --model generate

# Change background
genimg "place on Costa Rican wooden surface" -r product.jpg --edit-mode inpaint

# Create banner version
genimg "extend showing more artisan setting" -r photo.jpg --edit-mode outpaint --aspect-ratio 16:9
```

### Marketing Material Creation
```bash
# Generate from scratch
genimg "Turrialba countryside with coffee farmers" --aspect-ratio 16:9

# Create variations
genimg "warmer tones with sunset lighting" -r base-design.jpg

# Extend for different formats
genimg "extend to wide banner format" -r square.jpg --edit-mode outpaint --aspect-ratio 16:9
```

### Photo Enhancement Pipeline
```bash
# Step 1: Enhance lighting and colors
genimg "improve lighting and saturation" -r original.jpg --model generate -o enhanced.jpg

# Step 2: Change specific elements
genimg "change sky to dramatic sunset" -r enhanced.jpg --edit-mode inpaint -o final.jpg

# Step 3: Create social media versions
genimg "extend for Instagram story" -r final.jpg --edit-mode outpaint --aspect-ratio 9:16
```

---

## Tips for Best Results

### Prompt Writing
1. **Be specific** - Detail what you want
2. **Describe results** - Not just actions
3. **Include context** - Style, mood, lighting
4. **Name elements** - Specific objects, colors, positions

**Good Prompts:**
- "professional product photography with soft studio lighting on white background"
- "extend the beach landscape showing more turquoise ocean and white sand"
- "in the style of 1950s vintage travel posters with warm nostalgic tones"

**Vague Prompts (avoid):**
- "make it better"
- "fix this"
- "improve"

### Quality Optimization
1. **Use high-res inputs** - Better source = better output
2. **Choose right model** - `generate` for finals, `fast` for testing
3. **Iterate** - Try multiple variations
4. **Combine techniques** - Reference mode + inpaint for complex edits
5. **Match aspect ratios** - Appropriate for use case

### Workflow Efficiency
1. **Test with `fast` model** - Iterate quickly
2. **Final with `generate` model** - Best quality for publishing
3. **Save incrementally** - Keep versions at each step
4. **Use multiple references** - Combine style + content
5. **Be specific about preservation** - State what NOT to change

---

## Integration with Turri.cr

The CLI is designed to work seamlessly within the Turri.cr project structure:

**Automatic Path Detection:**
- Detects when you're in Turri folders
- Suggests appropriate save locations
- Names files descriptively

**Common Use Cases:**

**Products** (`~/Documents/Emprendedurismo/Turri.cr/Productos/[Product]/`):
```bash
cd Fotos/
genimg "product description" --model generate
genimg "enhance lighting" -r existing.jpg
```

**Producers** (`~/Documents/Emprendedurismo/Turri.cr/Relaciones/Productores/[Name]/`):
```bash
cd Fotos/
genimg "documentary-style portrait in workshop" --model generate
genimg "improve lighting and color" -r portrait.jpg
```

**Marketing** (`~/Documents/Emprendedurismo/Turri.cr/Mercadeo/`):
```bash
cd Campañas/2025-Q1/
genimg "Costa Rican countryside farmers" --aspect-ratio 16:9
genimg "extend for banner" -r photo.jpg --edit-mode outpaint --aspect-ratio 16:9
```

---

## Version
**Current Version:** 0.2.0 (2025-11-26)

**See:** `CHANGELOG.md` for version history

---

**Related Documentation:**
- `README.md` - Complete documentation
- `QUICK-START.md` - Quick reference guide
- `IMAGE-EDITING-GUIDE.md` - Detailed image editing guide
- `INSTALL.md` - Installation instructions
- `CHANGELOG.md` - Version history
