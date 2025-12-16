# Installation Guide - Imagen CLI

## Prerequisites

- Python 3.11 or higher
- UV package manager (recommended)
- Google AI API key

## Step 1: Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Install the CLI tool

```bash
cd ~/Documents/Dev-Tools/imagen-cli
uv sync
uv pip install -e .
```

This installs the `genimg` command globally, making it available from anywhere.

## Step 3: Set up your API key

### Option A: Environment variable (recommended)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export GOOGLE_AI_API_KEY="your-api-key-here"
```

Then reload your shell:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Option B: .env file

Create a `.env` file in the project directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
GOOGLE_AI_API_KEY=your-actual-api-key-here
```

## Step 4: Get your Google AI API key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and use it in Step 3

## Step 5: Test the installation

```bash
genimg "a beautiful sunset" --ask
```

This will generate a test image and ask where you want to save it.

## Verification

To verify the installation worked:

```bash
which genimg
genimg --help
```

You should see the help message with all available options.

## Troubleshooting

### "genimg: command not found"

Make sure you ran `uv pip install -e .` in the project directory. You may need to restart your terminal.

### "GOOGLE_AI_API_KEY not found"

Make sure you've set the API key as described in Step 3. Try running:

```bash
echo $GOOGLE_AI_API_KEY
```

If it's empty, the environment variable isn't set correctly.

### Permission errors

If you get permission errors during installation, make sure you have write access to the installation directory. UV should handle this automatically for user installations.

## Uninstallation

To remove the tool:

```bash
uv pip uninstall imagen-cli
```

---

**Need help?** Check the main README.md for usage examples and options.
