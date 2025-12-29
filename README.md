# clippit-py

Python wrapper for [Clippit](https://github.com/dcjohnston/Clippit) document comparison CLI with pre-built self-contained binaries.

## Installation

```bash
pip install git+https://github.com/dcjohnston/clippit-py.git
```

Or add to your `pyproject.toml`:

```toml
dependencies = [
    "clippit-py @ git+https://github.com/dcjohnston/clippit-py.git@v0.1.0",
]
```

## Usage

```python
from clippit import ClippitEngine

engine = ClippitEngine()

# Compare two DOCX documents
with open("original.docx", "rb") as f:
    original = f.read()
with open("modified.docx", "rb") as f:
    modified = f.read()

# Generate redlined document with tracked changes
result_bytes, stdout, stderr = engine.run_redline(
    author="Reviewer",
    original=original,
    modified=modified
)

with open("redlined.docx", "wb") as f:
    f.write(result_bytes)
```

## Supported Platforms

Pre-built binaries are included for:

- **macOS**: arm64 (Apple Silicon), x64 (Intel)
- **Linux**: x64, arm64 (glibc and musl/Alpine variants)
- **Windows**: x64

The binaries are self-contained and do not require .NET to be installed.

## Building from Source

If you need to build binaries locally (requires .NET 10 SDK):

```bash
# Build for current platform
./scripts/build_all.sh

# Or build for specific platform
dotnet publish cli/ClippitCli.csproj -c Release -r osx-arm64 --self-contained true -p:PublishSingleFile=true -o src/clippit/bin/darwin-arm64
```

## License

MIT License - see [LICENSE](LICENSE) for details.

Clippit is a maintained fork of [Open-XML-PowerTools](https://github.com/OfficeDev/Open-Xml-PowerTools).
