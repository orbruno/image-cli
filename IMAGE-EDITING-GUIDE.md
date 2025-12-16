# Image Editing Guide - Imagen CLI

Complete guide for editing images using reference images with the `genimg` command.

## Overview

Imagen CLI supports three modes of working with reference images:
1. **Reference Mode** - Use images for style transfer and content guidance
2. **Inpaint Mode** - Edit or replace specific elements within an image
3. **Outpaint Mode** - Extend images beyond their original boundaries

## Reference Mode (Default)

Use existing images as style or content references for generating new images.

### When to Use
- Applying artistic styles to images
- Creating variations of existing photos
- Enhancing or improving existing images
- Maintaining consistent style across multiple images

### Syntax
```bash
genimg "description of changes" -r reference-image.jpg
genimg "description of changes" -r ref1.jpg -r ref2.jpg  # Multiple references
```

### Examples

**Style Transfer:**
```bash
# Apply watercolor style
genimg "in watercolor painting style" -r artwork-reference.jpg -r photo.jpg

# Make photo look vintage
genimg "vintage 1970s photography style" -r old-photo.jpg
```

**Enhancement:**
```bash
# Improve lighting and colors
genimg "professional lighting with vibrant colors" -r dark-photo.jpg

# Increase detail and sharpness
genimg "enhance details and clarity" -r blurry-image.jpg --model generate
```

**Variations:**
```bash
# Create different time of day
genimg "same scene at golden hour" -r daytime-photo.jpg

# Different season
genimg "same location in autumn" -r summer-photo.jpg
```

## Inpaint Mode

Edit or replace specific elements within an image while keeping the rest intact.

### When to Use
- Changing backgrounds
- Replacing objects
- Modifying specific elements (sky, clothing, etc.)
- Removing unwanted elements
- Adding new objects to scenes

### Syntax
```bash
genimg "what to change" -r base-image.jpg --edit-mode inpaint
```

### Examples

**Background Changes:**
```bash
# Replace background
genimg "replace background with mountains and forest" -r portrait.jpg --edit-mode inpaint

# Change scene context
genimg "place subject in modern office setting" -r person-photo.jpg --edit-mode inpaint
```

**Object Modifications:**
```bash
# Change clothing colors
genimg "change shirt color to blue" -r photo.jpg --edit-mode inpaint

# Modify weather elements
genimg "change overcast sky to sunset" -r landscape.jpg --edit-mode inpaint

# Replace objects
genimg "replace coffee cup with tea cup" -r table-scene.jpg --edit-mode inpaint
```

**Product Photography:**
```bash
# Change product presentation
genimg "place cheese on rustic wooden board" -r cheese-photo.jpg --edit-mode inpaint

# Modify product context
genimg "surround coffee with coffee beans" -r coffee-bag.jpg --edit-mode inpaint
```

## Outpaint Mode

Extend images beyond their original boundaries, creating more canvas space.

### When to Use
- Converting portrait to landscape format
- Adding context around subjects
- Creating wider aspect ratios for banners
- Extending backgrounds
- Uncropping images

### Syntax
```bash
genimg "how to extend the image" -r image.jpg --edit-mode outpaint --aspect-ratio [ratio]
```

### Examples

**Format Conversion:**
```bash
# Convert square to wide banner
genimg "extend landscape to sides" -r square-photo.jpg --edit-mode outpaint --aspect-ratio 16:9

# Create vertical format
genimg "extend upward and downward" -r photo.jpg --edit-mode outpaint --aspect-ratio 9:16
```

**Adding Context:**
```bash
# Expand scene
genimg "continue the forest landscape to the sides" -r cropped-landscape.jpg --edit-mode outpaint --aspect-ratio 16:9

# Add more room background
genimg "extend the kitchen to show more countertop" -r tight-crop.jpg --edit-mode outpaint
```

**Social Media Formatting:**
```bash
# Create banner from portrait
genimg "expand to create banner with consistent background" -r portrait.jpg --edit-mode outpaint --aspect-ratio 16:9

# Story format
genimg "extend vertically for Instagram story" -r photo.jpg --edit-mode outpaint --aspect-ratio 9:16
```

## Best Practices

### Prompt Writing

**Be Specific:**
```bash
# Good
genimg "replace the gray sky with dramatic sunset clouds in orange and purple" -r photo.jpg --edit-mode inpaint

# Too vague
genimg "make it better" -r photo.jpg
```

**Describe Desired Result:**
```bash
# Good
genimg "extend the beach scene showing more ocean and sand" -r beach.jpg --edit-mode outpaint

# Less effective
genimg "make bigger" -r beach.jpg --edit-mode outpaint
```

### Multiple References

When using multiple references, the first is typically treated as the primary content, subsequent ones as style guides:

```bash
# Content + Style
genimg "combine these in impressionist style" -r photo.jpg -r monet-painting.jpg

# Multiple style references
genimg "blend these artistic styles" -r base.jpg -r style1.jpg -r style2.jpg
```

### Model Selection

**Use `--model generate` for:**
- Final/published images
- High-detail edits
- Professional photography
- Important marketing materials

**Use `--model fast` (default) for:**
- Testing edits
- Quick iterations
- Rough drafts
- Multiple variations

### Quality Tips

1. **Higher quality inputs = better outputs** - Use high-resolution source images
2. **Match aspect ratios** - When extending, choose appropriate target ratio
3. **Iterate** - Generate multiple versions, refine prompts based on results
4. **Combine modes** - Use reference mode first, then inpaint for details
5. **Save originals** - Always keep original files before editing

## Turri-Specific Workflows

### Product Photo Enhancement
```bash
cd ~/Documents/Emprendedurismo/Turri.cr/Productos/[Product]/Fotos

# Enhance lighting
genimg "professional product photography lighting" -r raw-photo.jpg --model generate

# Change background
genimg "place on rustic Costa Rican table setting" -r product.jpg --edit-mode inpaint

# Create banner version
genimg "extend to show more artisan setting" -r photo.jpg --edit-mode outpaint --aspect-ratio 16:9
```

### Producer Content
```bash
cd ~/Documents/Emprendedurismo/Turri.cr/Relaciones/Productores/[Name]/Fotos

# Enhance portrait
genimg "improve lighting and color in documentary style" -r portrait.jpg --model generate

# Style consistency
genimg "match this photographic style" -r reference-photo.jpg -r new-photo.jpg

# Create social media versions
genimg "extend for Instagram story format" -r photo.jpg --edit-mode outpaint --aspect-ratio 9:16
```

### Marketing Materials
```bash
cd ~/Documents/Emprendedurismo/Turri.cr/Mercadeo/Campañas/[Campaign]

# Create variations
genimg "warmer tones with sunset atmosphere" -r base-design.jpg

# Extend for different formats
genimg "extend design for wide banner" -r square-graphic.jpg --edit-mode outpaint --aspect-ratio 16:9

# Localize scenes
genimg "add Costa Rican countryside elements" -r generic-photo.jpg --edit-mode inpaint
```

## Troubleshooting

### Results Don't Match Expectations

**Try:**
- More specific prompts
- Using `--model generate` for higher quality
- Multiple reference images for better guidance
- Breaking complex edits into multiple steps

### Image Quality Issues

**Solutions:**
- Start with higher resolution source images
- Use `--model generate` instead of `fast`
- Avoid over-editing - sometimes less is more
- Save at each step to avoid quality degradation

### Unexpected Changes

**Tips:**
- Be explicit about what should NOT change
- Use inpaint mode for targeted edits instead of reference mode
- Include more context in prompt about what to preserve

---

**For more examples, see:**
- `README.md` - General usage
- `QUICK-START.md` - Quick reference
- `INSTALL.md` - Setup instructions

**Created**: 2025-11-26
**Author**: Orlando Bruno
