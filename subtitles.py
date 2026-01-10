import subprocess
import glob
import os
import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


def _parse_vtt(path: str) -> str:
    """Return plain text content of a VTT file (strip timestamps/numbers)."""
    lines = []
    ts_re = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3} -->")
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if s.isdigit():
                continue
            if ts_re.match(s):
                continue
            # skip WEBVTT header
            if s.upper().startswith("WEBVTT"):
                continue
            lines.append(s)
    return "\n".join(lines)


def download_subtitles(
    video_id: str,
    langs: List[str] = None,
    output_dir: str = "tmp",
    use_audio_transcribe: bool = False,
) -> Optional[str]:
    """
    Download subtitles for YouTube video using yt-dlp.
    Returns transcript text or None.
    - langs: list like ['ru','en'] in priority order
    - use_audio_transcribe: if True and no captions found, download audio and call `whisper` CLI
    """
    if langs is None:
        langs = ["en"]

    os.makedirs(output_dir, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"
    sub_langs = ",".join(langs)

    # 1) try to download subtitles (human or auto)
    cmd = [
        "yt-dlp",
        "--write-sub",
        "--write-auto-sub",
        "--sub-lang",
        sub_langs,
        "--skip-download",
        "-o",
        os.path.join(output_dir, f"{video_id}.%(ext)s"),
        url,
    ]
    try:
        logger.debug("Running: %s", " ".join(cmd))
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        logger.debug("yt-dlp subtitle download failed: %s", e)

    # 2) look for files in priority order
    # possible filenames: video_id.lang.vtt, video_id.vtt, video_id.lang.srt, video_id.srt
    for lang in langs:
        # vtt variants
        candidates = [
            os.path.join(output_dir, f"{video_id}.{lang}.vtt"),
            os.path.join(output_dir, f"{video_id}.vtt"),
            os.path.join(output_dir, f"{video_id}.{lang}.srt"),
            os.path.join(output_dir, f"{video_id}.srt"),
        ]
        for path in candidates:
            if os.path.exists(path):
                logger.info("Found subtitle file: %s", path)
                if path.lower().endswith(".vtt"):
                    return _parse_vtt(path)
                else:
                    # simple SRT to text strip (remove indices and timestamps)
                    text_lines = []
                    ts_re = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} -->")
                    with open(path, "r", encoding="utf-8") as fh:
                        for line in fh:
                            s = line.strip()
                            if not s:
                                continue
                            if s.isdigit():
                                continue
                            if ts_re.match(s):
                                continue
                            text_lines.append(s)
                    return "\n".join(text_lines)

    # 3) optional fallback: download audio and transcribe with whisper CLI
    if use_audio_transcribe:
        wav_path = os.path.join(output_dir, f"{video_id}.wav")
        cmd_audio = [
            "yt-dlp",
            "-x",
            "--audio-format",
            "wav",
            "-o",
            os.path.join(output_dir, f"{video_id}.%(ext)s"),
            url,
        ]
        try:
            logger.debug("Downloading audio: %s", " ".join(cmd_audio))
            subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            logger.warning("Audio download failed: %s", e)
            return None

        if not os.path.exists(wav_path):
            logger.warning("Audio file not found: %s", wav_path)
            return None

        # call whisper CLI (must be installed)
        txt_out = os.path.join(output_dir, f"{video_id}.txt")
        whisper_cmd = [
            "whisper",
            wav_path,
            "--model",
            "small",
            "--language",
            langs[0] if langs else "en",
            "--output_format",
            "txt",
            "--output_dir",
            output_dir,
        ]
        try:
            logger.debug("Running whisper: %s", " ".join(whisper_cmd))
            subprocess.run(whisper_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(txt_out):
                with open(txt_out, "r", encoding="utf-8") as fh:
                    return fh.read()
        except subprocess.CalledProcessError as e:
            logger.warning("Whisper transcription failed: %s", e)

    return None
