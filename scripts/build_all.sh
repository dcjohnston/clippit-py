#!/bin/bash
# Build self-contained Clippit CLI binaries for all supported platforms
# Requires .NET 10 SDK

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CLI_PROJECT="$PROJECT_ROOT/cli/ClippitCli.csproj"
BIN_DIR="$PROJECT_ROOT/src/clippit/bin"

# Runtime Identifiers (RIDs) and their output directory names
declare -A RIDS=(
    ["osx-arm64"]="darwin-arm64"
    ["osx-x64"]="darwin-x64"
    ["linux-x64"]="linux-x64"
    ["linux-arm64"]="linux-arm64"
    ["linux-musl-x64"]="linux-musl-x64"
    ["linux-musl-arm64"]="linux-musl-arm64"
    ["win-x64"]="win-x64"
)

echo "Building Clippit CLI for all platforms..."
echo "Project: $CLI_PROJECT"
echo "Output: $BIN_DIR"
echo ""

for rid in "${!RIDS[@]}"; do
    output_dir="${RIDS[$rid]}"
    echo "Building for $rid -> $output_dir"

    dotnet publish "$CLI_PROJECT" \
        -c Release \
        -r "$rid" \
        --self-contained true \
        -p:PublishSingleFile=true \
        -p:DebugType=none \
        -p:DebugSymbols=false \
        -o "$BIN_DIR/$output_dir"

    echo "  Done: $BIN_DIR/$output_dir"
done

echo ""
echo "All builds complete!"
ls -la "$BIN_DIR"/*/clippit-compare* 2>/dev/null || ls -la "$BIN_DIR"/*/*
