#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Convert a .pptx file into per-slide PNG/JPG images.
# Two backends:
#   - libreoffice : headless soffice -> PDF, then pdftoppm -> images (default, cross-platform)
#   - com         : Windows PowerPoint COM (high fidelity, Windows + PowerPoint required)
# NOTE: All PowerShell invocations go through bash -c "powershell.exe ..." by design.

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_pages(expr: Optional[str]) -> Optional[List[int]]:
    # Accepts "1-5", "1,3,5", "1-3,7,10-12". Returns sorted unique 1-based list.
    if not expr:
        return None
    pages = set()
    for chunk in expr.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"^(\d+)\s*-\s*(\d+)$", chunk)
        if m:
            lo, hi = int(m.group(1)), int(m.group(2))
            if lo > hi:
                lo, hi = hi, lo
            for p in range(lo, hi + 1):
                pages.add(p)
        elif chunk.isdigit():
            pages.add(int(chunk))
        else:
            raise ValueError("Invalid --pages token: {!r}".format(chunk))
    if not pages:
        return None
    result = sorted(p for p in pages if p >= 1)
    if not result:
        raise ValueError("--pages produced no valid page numbers")
    return result


def _pages_bounds(pages: Optional[List[int]]) -> Tuple[Optional[int], Optional[int]]:
    if not pages:
        return None, None
    return min(pages), max(pages)


def _image_size(path: Path) -> Tuple[Optional[int], Optional[int]]:
    # Minimal PNG/JPEG dimension reader (no PIL dependency).
    try:
        with open(path, "rb") as f:
            head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            # IHDR starts at byte 8; width at 16, height at 20 (big-endian uint32)
            w = int.from_bytes(head[16:20], "big")
            h = int.from_bytes(head[20:24], "big")
            return w, h
        if head[:3] == b"\xff\xd8\xff":
            return _jpeg_size(path)
    except Exception:
        return None, None
    return None, None


def _jpeg_size(path: Path) -> Tuple[Optional[int], Optional[int]]:
    try:
        with open(path, "rb") as f:
            data = f.read(2)
            if data != b"\xff\xd8":
                return None, None
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                while b == b"\xff":
                    b = f.read(1)
                if not b:
                    return None, None
                marker = b[0]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    f.read(3)  # length(2) + precision(1)
                    h = int.from_bytes(f.read(2), "big")
                    w = int.from_bytes(f.read(2), "big")
                    return w, h
                seg_len = int.from_bytes(f.read(2), "big")
                if seg_len < 2:
                    return None, None
                f.seek(seg_len - 2, os.SEEK_CUR)
    except Exception:
        return None, None


def _run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


# ---------------------------------------------------------------------------
# Backend: LibreOffice + pdftoppm
# ---------------------------------------------------------------------------

SOFFICE_CANDIDATES_WIN = [
    r"C:/Program Files/LibreOffice/program/soffice.exe",
    r"C:/Program Files (x86)/LibreOffice/program/soffice.exe",
]
SOFFICE_CANDIDATE_MAC = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
SOFFICE_INSTALL_HINT = (
    "LibreOffice not found. Please install it, e.g.:\n"
    "  Windows : winget install TheDocumentFoundation.LibreOffice\n"
    "  macOS   : brew install --cask libreoffice\n"
    "  Linux   : apt-get install libreoffice (or distro equivalent)"
)
PDFTOPPM_INSTALL_HINT = (
    "pdftoppm not found. Please install poppler-utils, e.g.:\n"
    "  Windows : winget install oschwartz10612.Poppler  (or download poppler for Windows)\n"
    "  macOS   : brew install poppler\n"
    "  Linux   : apt-get install poppler-utils"
)


def _find_soffice() -> Optional[str]:
    system = platform.system()
    if system == "Windows":
        for cand in SOFFICE_CANDIDATES_WIN:
            if Path(cand).exists():
                return cand
        found = shutil.which("soffice") or shutil.which("soffice.exe")
        if found:
            return found
    elif system == "Darwin":
        if Path(SOFFICE_CANDIDATE_MAC).exists():
            return SOFFICE_CANDIDATE_MAC
        found = shutil.which("soffice")
        if found:
            return found
    else:
        for name in ("soffice", "libreoffice"):
            found = shutil.which(name)
            if found:
                return found
    return None


def _find_pdftoppm() -> Optional[str]:
    return shutil.which("pdftoppm") or shutil.which("pdftoppm.exe")


def convert_libreoffice(
    input_path: Path,
    output_dir: Path,
    fmt: str,
    dpi: int,
    pages: Optional[List[int]],
    jpeg_quality: int,
    keep_tmp: bool = False,
) -> List[Path]:
    soffice = _find_soffice()
    if not soffice:
        raise RuntimeError(SOFFICE_INSTALL_HINT)
    pdftoppm = _find_pdftoppm()
    if not pdftoppm:
        raise RuntimeError(PDFTOPPM_INSTALL_HINT)

    tmp_root = Path(tempfile.mkdtemp(prefix="pptx2img_"))
    try:
        # Step A: soffice -> pdf
        proc_a = _run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(tmp_root), str(input_path)],
            cwd=tmp_root,
        )
        if proc_a.returncode != 0:
            raise RuntimeError(
                "soffice convert-to pdf failed (rc={}): {}".format(
                    proc_a.returncode, proc_a.stderr.decode("utf-8", "replace").strip()
                )
            )
        pdf_path = tmp_root / (input_path.stem + ".pdf")
        if not pdf_path.exists():
            # fallback: pick the first pdf produced
            pdfs = list(tmp_root.glob("*.pdf"))
            if not pdfs:
                raise RuntimeError("soffice did not produce a PDF in {}".format(tmp_root))
            pdf_path = pdfs[0]

        # Step B: pdftoppm -> images
        output_dir.mkdir(parents=True, exist_ok=True)
        prefix = output_dir / "slide"
        cmd_b: List[str] = [pdftoppm, "-r", str(dpi)]
        if fmt == "png":
            cmd_b.append("-png")
        else:
            cmd_b.extend(["-jpeg", "-jpegopt", "quality={}".format(jpeg_quality)])
        lo, hi = _pages_bounds(pages)
        if lo is not None:
            cmd_b.extend(["-f", str(lo), "-l", str(hi)])
        cmd_b.extend([str(pdf_path), str(prefix)])

        proc_b = _run(cmd_b)
        if proc_b.returncode != 0:
            raise RuntimeError(
                "pdftoppm failed (rc={}): {}".format(
                    proc_b.returncode, proc_b.stderr.decode("utf-8", "replace").strip()
                )
            )

        ext = "png" if fmt == "png" else "jpg"
        produced = sorted(output_dir.glob("slide-*.{}".format(ext)))
        # pdftoppm may emit .jpeg instead of .jpg on some builds; normalize.
        if fmt == "jpg" and not produced:
            for p in sorted(output_dir.glob("slide-*.jpeg")):
                new = p.with_suffix(".jpg")
                p.replace(new)
            produced = sorted(output_dir.glob("slide-*.jpg"))

        if pages:
            keep = set(pages)
            filtered = []
            for p in produced:
                m = re.search(r"slide-(\d+)\.", p.name)
                if m and int(m.group(1)) in keep:
                    filtered.append(p)
            produced = filtered
        return produced
    finally:
        if not keep_tmp:
            shutil.rmtree(tmp_root, ignore_errors=True)


# ---------------------------------------------------------------------------
# Backend: PowerPoint COM (Windows)
# ---------------------------------------------------------------------------

def _bash_powershell(ps_script: str) -> subprocess.CompletedProcess:
    # Must go through bash -c "powershell.exe ..." per project rule.
    ps_encoded = ps_script.replace('"', '\\"')
    bash_cmd = 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "{}"'.format(ps_encoded)
    return subprocess.run(
        ["bash", "-c", bash_cmd],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def convert_com(
    input_path: Path,
    output_dir: Path,
    fmt: str,
    pages: Optional[List[int]],
) -> List[Path]:
    if platform.system() != "Windows":
        raise RuntimeError("COM backend only works on Windows with Microsoft PowerPoint installed.")
    output_dir.mkdir(parents=True, exist_ok=True)
    save_code = 18 if fmt == "png" else 17  # ppSaveAsPNG=18, ppSaveAsJPG=17

    ps = (
        "$ErrorActionPreference = 'Stop'; "
        "try {{ $ppt = New-Object -ComObject PowerPoint.Application }} "
        "catch {{ Write-Error 'PowerPoint is not installed or COM is unavailable.'; exit 2 }}; "
        "$pres = $ppt.Presentations.Open('{inp}', $true, $false, $false); "
        "$pres.SaveAs('{out}', {code}); "
        "$pres.Close(); $ppt.Quit();"
    ).format(
        inp=str(input_path).replace("'", "''"),
        out=str(output_dir).replace("'", "''"),
        code=save_code,
    )

    proc = _bash_powershell(ps)
    if proc.returncode != 0:
        raise RuntimeError(
            "PowerPoint COM export failed (rc={}): {}".format(
                proc.returncode, proc.stderr.decode("utf-8", "replace").strip()
            )
        )

    ext = "png" if fmt == "png" else "jpg"
    # PowerPoint typically saves the folder or a set of Slide1.PNG / Slide1.JPG files.
    # Handle both direct files and a nested folder named after the pptx stem.
    candidates: List[Path] = []
    nested = output_dir / input_path.stem
    if nested.is_dir():
        candidates = sorted(nested.glob("*.{}".format(ext.upper()))) + sorted(
            nested.glob("*.{}".format(ext))
        )
        # Flatten into output_dir with slide-N naming.
        flattened: List[Path] = []
        for src in candidates:
            m = re.search(r"(\d+)", src.stem)
            if not m:
                continue
            page_num = int(m.group(1))
            dst = output_dir / "slide-{}.{}".format(page_num, ext)
            if src.resolve() != dst.resolve():
                shutil.move(str(src), str(dst))
            flattened.append(dst)
        shutil.rmtree(nested, ignore_errors=True)
        produced = sorted(flattened, key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    else:
        # PowerPoint produced files directly in output_dir
        raw = sorted(output_dir.glob("*.{}".format(ext.upper()))) + sorted(
            output_dir.glob("*.{}".format(ext))
        )
        produced = []
        for src in raw:
            m = re.search(r"(\d+)", src.stem)
            if not m:
                continue
            page_num = int(m.group(1))
            dst = output_dir / "slide-{}.{}".format(page_num, ext)
            if src.resolve() != dst.resolve():
                shutil.move(str(src), str(dst))
            produced.append(dst)
        produced = sorted(produced, key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))

    if pages:
        keep = set(pages)
        filtered = []
        for p in produced:
            m = re.search(r"slide-(\d+)\.", p.name)
            if m and int(m.group(1)) in keep:
                filtered.append(p)
            elif m:
                # Remove out-of-range images to honor --pages
                try:
                    p.unlink()
                except OSError:
                    pass
        produced = filtered
    return produced


# ---------------------------------------------------------------------------
# Auto dispatch
# ---------------------------------------------------------------------------

def convert_auto(
    input_path: Path,
    output_dir: Path,
    fmt: str,
    dpi: int,
    pages: Optional[List[int]],
    jpeg_quality: int,
) -> Tuple[str, List[Path]]:
    errors = []
    try:
        files = convert_libreoffice(input_path, output_dir, fmt, dpi, pages, jpeg_quality)
        return "libreoffice", files
    except Exception as e:
        errors.append("libreoffice: {}".format(e))
    if platform.system() == "Windows":
        try:
            files = convert_com(input_path, output_dir, fmt, pages)
            return "com", files
        except Exception as e:
            errors.append("com: {}".format(e))
    raise RuntimeError("auto backend failed. Details:\n  - " + "\n  - ".join(errors))


# ---------------------------------------------------------------------------
# Manifest
# ---------------------------------------------------------------------------

def write_manifest(
    manifest_path: Path,
    input_path: Path,
    method: str,
    fmt: str,
    dpi: int,
    files: List[Path],
) -> None:
    slides = []
    for p in files:
        m = re.search(r"slide-(\d+)\.", p.name)
        page_num = int(m.group(1)) if m else -1
        w, h = _image_size(p)
        slides.append(
            {
                "page": page_num,
                "file": p.name,
                "width_px": w,
                "height_px": h,
            }
        )
    slides.sort(key=lambda s: s["page"])
    payload = {
        "generated_at": _utc_now_iso(),
        "input": input_path.name,
        "method": method,
        "format": fmt,
        "dpi": dpi,
        "slides": slides,
    }
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pptx_to_images.py",
        description="Convert a .pptx presentation into per-slide PNG/JPG images.",
    )
    p.add_argument("--input", required=True, help="Path to the source .pptx file.")
    p.add_argument("--output-dir", required=True, help="Directory for rendered images (created if missing).")
    p.add_argument("--format", choices=["png", "jpg"], default="png", help="Output image format (default: png).")
    p.add_argument("--dpi", type=int, default=150, help="Render DPI for libreoffice backend (default: 150).")
    p.add_argument(
        "--method",
        choices=["libreoffice", "com", "auto"],
        default="auto",
        help="Conversion backend (default: auto -> libreoffice then com fallback on Windows).",
    )
    p.add_argument("--pages", help='Optional page selection, e.g. "1-5" or "1,3,5".')
    p.add_argument("--jpeg-quality", type=int, default=85, help="JPEG quality 1-100 (only for --format jpg).")
    p.add_argument("--manifest", action="store_true", help="Emit manifest.json alongside the images.")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not input_path.exists():
        parser.error("Input file does not exist: {}".format(input_path))
    if input_path.suffix.lower() != ".pptx":
        parser.error("Input must be a .pptx file: {}".format(input_path))
    if not (1 <= args.jpeg_quality <= 100):
        parser.error("--jpeg-quality must be between 1 and 100")
    if args.dpi <= 0:
        parser.error("--dpi must be positive")

    try:
        pages = _parse_pages(args.pages)
    except ValueError as e:
        parser.error(str(e))
        return 2  # unreachable

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.method == "libreoffice":
            files = convert_libreoffice(
                input_path, output_dir, args.format, args.dpi, pages, args.jpeg_quality
            )
            used = "libreoffice"
        elif args.method == "com":
            files = convert_com(input_path, output_dir, args.format, pages)
            used = "com"
        else:
            used, files = convert_auto(
                input_path, output_dir, args.format, args.dpi, pages, args.jpeg_quality
            )
    except Exception as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 1

    if not files:
        print("WARNING: no images were produced.", file=sys.stderr)

    if args.manifest:
        manifest_path = output_dir / "manifest.json"
        write_manifest(manifest_path, input_path, used, args.format, args.dpi, files)
        print("manifest: {}".format(manifest_path))

    print("method: {}".format(used))
    print("images: {} file(s) in {}".format(len(files), output_dir))
    for f in files:
        print("  - {}".format(f.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
