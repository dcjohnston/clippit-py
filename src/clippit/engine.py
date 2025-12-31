"""Clippit CLI wrapper engine with platform detection."""

import os
import platform
import subprocess
import tempfile
from pathlib import Path


class ClippitEngine:
    """Wrapper for the Clippit WmlComparer CLI.

    Automatically detects the current platform and uses the appropriate
    pre-built binary. Binaries are self-contained and do not require
    .NET to be installed.
    """

    def __init__(self, cli_path: str | None = None):
        """Initialize the Clippit engine.

        Args:
            cli_path: Optional explicit path to the clippit-compare binary.
                     If not provided, uses CLIPPIT_CLI_PATH env var or
                     auto-detects based on platform.
        """
        self.cli_path = cli_path or os.environ.get("CLIPPIT_CLI_PATH") or self._get_default_path()

    def _get_default_path(self) -> str:
        """Determine the correct binary path for the current platform."""
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            rid = "darwin-arm64" if machine == "arm64" else "darwin-x64"
        elif system == "linux":
            # Check for musl (Alpine Linux)
            is_musl = self._is_musl_libc()
            arch = "arm64" if machine in ("aarch64", "arm64") else "x64"
            rid = f"linux-musl-{arch}" if is_musl else f"linux-{arch}"
        elif system == "windows":
            rid = "win-x64"
        else:
            raise RuntimeError(f"Unsupported platform: {system} {machine}")

        bin_dir = Path(__file__).parent / "bin" / rid
        exe_name = "clippit-compare.exe" if system == "windows" else "clippit-compare"
        binary_path = bin_dir / exe_name

        if not binary_path.exists():
            raise RuntimeError(
                f"Clippit binary not found for platform {rid}. "
                f"Expected at: {binary_path}"
            )

        return str(binary_path)

    def _is_musl_libc(self) -> bool:
        """Check if the system uses musl libc (e.g., Alpine Linux)."""
        # Check for Alpine-specific file
        if os.path.exists("/etc/alpine-release"):
            return True
        # Check ldd output for musl
        try:
            result = subprocess.run(
                ["ldd", "--version"],
                capture_output=True,
                text=True,
            )
            return "musl" in result.stderr.lower() or "musl" in result.stdout.lower()
        except (FileNotFoundError, subprocess.SubprocessError):
            return False

    def run_redline(
        self,
        author: str,
        original: bytes,
        modified: bytes,
    ) -> tuple[bytes, str | None, str | None]:
        """Compare two DOCX documents and generate a redlined version.

        Args:
            author: Author name for tracked changes attribution.
            original: Bytes of the original DOCX document.
            modified: Bytes of the modified DOCX document.

        Returns:
            Tuple of (output_bytes, stdout, stderr) where output_bytes is
            the redlined DOCX with tracked changes.

        Raises:
            RuntimeError: If the comparison fails or no output is produced.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            original_path = Path(tmpdir) / "original.docx"
            modified_path = Path(tmpdir) / "modified.docx"
            output_path = Path(tmpdir) / "output.docx"

            original_path.write_bytes(original)
            modified_path.write_bytes(modified)

            result = subprocess.run(
                [
                    self.cli_path,
                    author,
                    str(original_path),
                    str(modified_path),
                    str(output_path),
                ],
                capture_output=True,
                text=True,
            )

            stdout = result.stdout if result.stdout else None
            stderr = result.stderr if result.stderr else None

            if result.returncode != 0:
                raise RuntimeError(
                    f"Clippit CLI failed with exit code {result.returncode}: {stderr}"
                )

            if not output_path.exists():
                raise RuntimeError(
                    f"Clippit CLI did not produce output file: {stderr}"
                )

            return output_path.read_bytes(), stdout, stderr
