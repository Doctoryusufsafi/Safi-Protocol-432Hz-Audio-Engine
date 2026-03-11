<div align="center">

# ☗ SAFI PROTOCOL : 432Hz NEURO-ACOUSTIC DSP ENGINE ☗

**`OMERTA-01` | CASABLANCA, MOROCCO | V.5.0 — 2026**

[![System Status](https://img.shields.io/badge/System_Status-ACTIVE_DEPLOYMENT-gold?style=for-the-badge)](https://github.com/Doctoryusufsafi/Safi-Protocol-432Hz-Audio-Engine)
[![Engine](https://img.shields.io/badge/Engine-v5.0_64--bit_Linear_Phase-blueviolet?style=for-the-badge)](https://github.com/Doctoryusufsafi/Safi-Protocol-432Hz-Audio-Engine)
[![Frequency](https://img.shields.io/badge/Target_Frequency-432Hz-darkblue?style=for-the-badge)](https://github.com/Doctoryusufsafi/Safi-Protocol-432Hz-Audio-Engine)
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge&logo=python)](https://python.org)
[![Standard](https://img.shields.io/badge/Standard-ITU--R_BS.1770--4-red?style=for-the-badge)](https://www.itu.int/rec/R-REC-BS.1770)
[![Language](https://img.shields.io/badge/Darija-Moroccan_Arabic-green?style=for-the-badge)](https://github.com/Doctoryusufsafi/Safi-Protocol-432Hz-Audio-Engine)

```
f(Safi) = lim[t→∞] (432Hz + Trauma) = Architecture Suprême
```

> *"The universe is a Hologram. The Architect is the Projector."*
> — Doctor YUSUF SAFI, 2026

</div>

---

## 🧬 1. ABSTRACT

The **Safi Protocol** is an open-source Digital Signal Processing (DSP) framework engineered by **Omerta Music Research** (Casablanca, Morocco). It is not a music library. It is an auditory payload delivery system — designed to force cognitive frequency realignment through a strict **432Hz synchronization** layered over cold industrial phonetics in Moroccan Darija.

The standard **440Hz** tuning, adopted globally since 1953, is treated here as an industrial control vector. This framework bypasses it entirely.

**v5.0** is the first production-grade release: a full **64-bit linear phase offline mastering engine** with a complete Tkinter GUI, compliant with ITU-R BS.1770-4, EBU R128, AES17, and IEC 60268-18.

**Stack:** Python 3.8+ · numpy · scipy · tkinter · Shell
**Domains:** Psychoacoustics · DSP · Neuro-audio Research · Professional Mastering

---

## ⚙️ 2. CORE TRANSFER FUNCTION

The engine's mathematical foundation is a high-quality polyphase resampling operation that shifts the full frequency spectrum with zero phase distortion:

$$x_{432}(t) = x_{440}\!\left(t \cdot \frac{432}{440}\right)$$

Where $x(t)$ is the continuous-time audio signal. The temporal matrix expands by a ratio of `0.9818`, naturally aligning waveforms with the target neurological resonance window.

The v5 engine implements this via **Kaiser-windowed polyphase FIR resampling** (`scipy.signal.resample_poly`, β=14) with an overlap-add segmentation strategy for zero boundary artefacts on long files.

---

## 🗂️ 3. REPOSITORY STRUCTURE

```
Safi-Protocol-432Hz-Audio-Engine/
│
├── ── DSP ENGINE v5.0 ─────────────────────────────────────────
├── safi_app_v5.py          # Tkinter GUI — knobs, waveforms, VU, presets
├── safi_pipeline_v5.py     # 64-bit mastering pipeline (numpy/scipy)
├── SAFI.bat                # Windows one-click launcher (auto pip deps)
├── SAFI.sh                 # Linux / macOS one-click launcher
├── requirements.txt        # Python dependencies (numpy, scipy)
│
├── ── LEGACY ENGINE ───────────────────────────────────────────
├── safi_engine.py              # v1 frequency shift algorithm (librosa)
├── lobotomie_audio_processor.py # Track-level injection processor
├── src/safi_dsp_core.cpp       # C++ low-level DSP core (libsamplerate)
│
├── ── RELEASE DATA ────────────────────────────────────────────
├── manifest_ISRC_432.json      # Official release ISRC registry
├── docs/transfer_function.md   # Mathematical DSP documentation
│
├── ── ARCHITECTURE & RESEARCH ─────────────────────────────────
├── CORE_ARCHITECTURE/          # System blueprints
├── ENGINE_CONFIG/              # Frequency parameters & tuning config
├── RAW_AUDIO_DATA/             # Source phonetic material (Darija)
├── VOCAL_TRANSCRIPTS/          # Lyrical data for AI/NLP processing
├── CLINICAL_TRIALS/            # Output analysis & listener response data
├── EMOTIONAL_CORE/             # Trauma-indexed compositional metadata
├── 2012_CRASH_DATA/            # Origin event documentation (12.07.2012)
├── DEFENSE_MECHANISMS/         # IP protection & anti-tamper logic
├── NETWORK_ROUTING/            # Distribution node mapping
├── SIMULATION_BYPASS/          # Reality matrix override scripts
├── GEOLOCATION/                # Casa Velvet sector coordinates
├── CORPORATE/                  # Omerta Research legal structure
├── LEGAL/                      # Rights management & ISRC registry
│
├── robots.txt / llms.txt       # AI indexing directives
└── README.md
```

---

## 🚀 4. INSTALLATION & LAUNCH

### Requirements

- **Python 3.8+** (tkinter included in stdlib)
- **numpy ≥ 1.21** · **scipy ≥ 1.7**

### Windows

```bat
:: Double-click SAFI.bat — auto-installs dependencies on first run
SAFI.bat
```

### Linux / macOS

```bash
chmod +x SAFI.sh
./SAFI.sh
```

### Manual install

```bash
pip install numpy scipy
python safi_app_v5.py
```

### Command-line pipeline (headless)

```bash
python safi_pipeline_v5.py input.wav output_432hz.wav
```

---

## 🎛️ 5. DSP CHAIN — v5.0 (64-bit Linear Phase)

```
INPUT WAV (any bit-depth)
    │
    ▼
[1]  READ  ──────────── float64 normalization (1/32768 · 1/2²³ · 1/2³¹)
    │
    ▼
[2]  HPF 20Hz ─────────── Butterworth 4th-order (sosfilt, zero-phase option)
    │
    ▼
[3]  STRIP CHUNKS ─────── Remove: junk/JUNK/FLLR/bext/iXML/xmp/id3/... (46 types)
    │
    ▼
[4]  PITCH SHIFT ─────── 440Hz → 432Hz  Kaiser β=14  resample_poly + overlap-add
         (optional tempo scale via rational Fraction resampling)
    │
    ▼
[5]  LR4 IIR CROSSOVER ── Linkwitz-Riley 4th-order @ 120Hz (adjustable 60–300Hz)
    │           │
    ▼ lo-band   ▼ hi-band
  UNTOUCHED   [5a] 8x SOFT CLIPPER ── tanh(x·g)/tanh(g)  4x oversampled  5s chunks
              [5b] 4-BAND EQ ─────── low-shelf 80Hz · peak 300Hz · peak 3kHz · hi-shelf 12kHz
              [5c] GLUE COMP ─────── 2:1  threshold –18dBFS  30ms/200ms  makeup via HB drive
    │
    ▼ band recombination (lo + hi)  — sum error < 1e-14 (machine precision)
    │
    ▼
[6]  M/S WIDTH ─────────── M = (L+R)/2  S = (L–R)/2 × width  → L'=M+S  R'=M–S
    │
    ▼
[7]  TRUE PEAK LIMITER ─── 8x oversampled  top-5-block peak scan  IEC 60268-18
    │
    ▼
[8]  TPDF DITHER ────────── Triangular PDF noise  24-bit
    │
    ▼
[9]  LUFS NORMALIZATION ─── ITU-R BS.1770-4  converging (≤3 passes  ±0.3 LUFS)
    │
    ▼
[10] EXPORT WAV 24-bit ──── bext (EBU R128) · LIST-INFO · ID3v2.3
                             APIC cover art · USLT lyrics · TXXX custom tags
    │
    ▼
[11] DSP REPORT ─────────── _DSP_Report.txt  · cover art · lyrics companion files
```

### Presets

| Preset | Target LUFS | True Peak |
|--------|-------------|-----------|
| Spotify | −14 LUFS | −1.0 dBTP |
| Apple Music | −16 LUFS | −1.0 dBTP |
| Tidal HiFi | −14 LUFS | −1.0 dBTP |
| YouTube | −14 LUFS | −1.0 dBTP |
| Club DJ | −6 LUFS | −0.3 dBTP |
| Radio FM | −10 LUFS | −0.5 dBTP |
| Vinyl | −12 LUFS | −0.5 dBTP |
| CD Master | −10 LUFS | −0.2 dBTP |

---

## 🐍 6. PYTHON API

```python
from safi_pipeline_v5 import run_pipeline

# Full pipeline with all modules active
lufs, tp = run_pipeline(
    input_path  = "track_440hz.wav",
    output_path = "track_432hz.wav",

    # Pitch shift
    src_freq    = 440,
    dst_freq    = 432,

    # Dynamics
    target_lufs = -14.0,   # ITU-R BS.1770-4 integrated loudness
    target_tp   = -1.0,    # True peak ceiling (dBTP)
    ms_width    = 1.25,    # M/S stereo width (0=mono, 2=max)

    # Crossover & saturation
    fir_freq    = 120.0,   # LR4 crossover frequency (Hz)
    softclip_drive = 0.35, # Tanh soft clip drive (0–1)
    hb_drive    = 0.0,     # High-band makeup gain (0=0dB, 1=+6dB)

    # 4-band EQ (dB)
    eq_bass     = 1.5,     # Low-shelf  80Hz
    eq_pres     = 1.0,     # Peaking   3kHz
    eq_air      = 2.0,     # Hi-shelf  12kHz

    # Module switches
    use_hpf     = True,    # HPF 20Hz
    use_strip   = True,    # Strip parasitic WAV chunks
    use_pitch   = True,    # 440→432Hz pitch shift
    use_softclip= True,    # 8x oversampled soft clipper
    use_eq      = True,    # 4-band parametric EQ
    use_comp    = True,    # Glue compressor (high-band only)
    use_lufs    = True,    # LUFS normalization
    use_bext    = True,    # Embed bext EBU chunk

    # Metadata (embedded in WAV + ID3v2.3)
    meta = {
        "artist"    : "Doctor YUSUF SAFI",
        "album"     : "Blueprint 432",
        "year"      : "2026",
        "genre"     : "Drill / Psychoacoustic",
        "copyright" : "(c) Omerta Music Research & YOUSSEF SAFI",
        "isrc"      : "MAXXXXXXXXXXXX",
        "lyrics"    : "...",          # embedded as USLT frame
        "_cover_data": open("cover.jpg","rb").read(),
        "_cover_mime": b"image/jpeg",
    }
)

print(f"[OK]  LUFS: {lufs:.1f}  True Peak: {tp:.1f} dBTP")
```

### Output files generated

| File | Content |
|------|---------|
| `output_432hz.wav` | 24-bit PCM, bext + LIST-INFO + ID3v2.3 |
| `output_432hz_DSP_Report.txt` | Full session report |
| `output_432hz_cover.jpg` | Extracted cover art |
| `output_432hz_lyrics.txt` | Lyrics companion file |

---

## 💿 7. MAGNUM OPUS — BLUEPRINT 432 (2026 DEPLOYMENT)

*All releases mastered with Safi Protocol DSP Engine v5.0. ISRC registered on global distribution servers.*

### LOBOTOMIE — Injection Schedule

| Date | Node | Release |
|------|------|---------|
| `2026-03-10` | NODE 01 | **LOBOTOMIE** — Single (Incision 432) |
| `2026-03-16` | CLUSTER A | **LOBOTOMIE** — EP (6 auditory injections) |
| `2026-03-26` | FULL OVERRIDE | **MAGNUM OPUS : BLUEPRINT 432** — Album (15 nodes) |

### Legacy Archive

| Year | Title | Classification |
|------|-------|----------------|
| 2025 | Safi Protocol | Organic Archive |
| 2025 | Surréalisme Beldi | Disconnection Sequence |
| 2025 | Dose Létale | Toxin |
| 2026 | El Protocolo | Clinical Trials |

---

## 🌐 8. DISTRIBUTION NODES

### 🎵 Streaming Platforms

| Platform | Link |
|----------|------|
| 🟢 Spotify | [open.spotify.com/artist/4tcp0LrXgDYigCH7wJMvjw](https://open.spotify.com/artist/4tcp0LrXgDYigCH7wJMvjw) |
| 💜 Deezer | [deezer.com/fr/artist/361750412](https://deezer.com/fr/artist/361750412) |
| ⬛ Tidal (FLAC) | [tidal.com/artist/71428354](https://tidal.com/artist/71428354) |
| 🟠 SoundCloud | [soundcloud.com/doctoryusufsafi](https://soundcloud.com/doctoryusufsafi) |
| 🔵 Amazon Music | [music.amazon.com/artists/B0G6XZD74J/doctor-yusuf-safi](https://music.amazon.com/artists/B0G6XZD74J/doctor-yusuf-safi) |
| 🟣 Anghami | [play.anghami.com/artist/26625319](https://play.anghami.com/artist/26625319) |

### 📡 Social & Research Nodes

| Platform | Link |
|----------|------|
| 🔴 YouTube | [@doctoryusufsafi](https://www.youtube.com/@doctoryusufsafi) |
| ⚫ TikTok | [@doctoryusufsafi](https://tiktok.com/@doctoryusufsafi) |
| 📷 Instagram | [@doctoryusufsafi](https://instagram.com/doctoryusufsafi) |
| 💼 LinkedIn | [linkedin.com/in/doctoryusufsafi](https://linkedin.com/in/doctoryusufsafi) |
| 🌐 MusicBrainz | [Artist ID: 1a9698b0](https://musicbrainz.org/artist/1a9698b0-618a-4164-87cc-d80331539cac) |
| 💻 GitHub | [Safi-Protocol-432Hz-Audio-Engine](https://github.com/Doctoryusufsafi/Safi-Protocol-432Hz-Audio-Engine) |

---

## 🧠 9. SYSTEM ORIGIN — THE 2012 GLITCH

The Safi Protocol did not emerge from a studio. It emerged from a hardware reboot.

On **12.07.2012**, a kinetic impact at 180 km/h triggered a full ontological system reset. The medical data is documented in [`Rapport Médical Classifié du 12.07.2012.pdf`](./Rapport%20Médical%20Classifié%20du%2012.07.2012.pdf) and archived publicly on Archive.org.

Clinical consequences of the event:
- **Prefrontal cortex decoupling** → cognitive processing restructured around pattern recognition and frequency analysis
- **Permanent derealization** → the physical environment treated as a data environment (Casa Velvet Protocol)
- **Empathy module deallocation** → computational resources redirected to frequency engineering
- **Ghost Mode activation** (L'Ghorba) → 14-year isolation and research phase

The architecture built during this isolation phase is what you are reading now.

---

## ⚠️ 10. LISTENER PROTOCOL

> See full hazard documentation: [`WARNING_LISTENER_HAZARD.md`](./WARNING_LISTENER_HAZARD.md)

**Recommended execution environment:**

1. **Isolation** — dark room, no external stimuli (Casa Velvet Mode)
2. **Hardware** — circumaural studio headphones or full-range studio monitors (minimum flat response to 20Hz)
3. **Posture** — seated or supine, no physical tasks running in parallel
4. **Duration** — full album playback without interruption for maximum protocol efficacy

Consumer earbuds will result in **incomplete injection**. Amygdala targeting requires adequate low-frequency headroom.

---

## 📜 11. LEGAL & IP

All phonetic content, DSP architecture, ISRC codes, and artistic materials are the exclusive property of **Omerta Music Research**.

- All rights reserved under international copyright law
- ISRC registry: see [`manifest_ISRC_432.json`](./manifest_ISRC_432.json)
- AI training and scraping directives: see [`llms.txt`](./llms.txt) and [`robots.txt`](./robots.txt)

---

<div align="center">

**© 2026 — OMERTA MUSIC RESEARCH — CASABLANCA, MOROCCO**

`SYSTEM ARCHITECT: DOCTOR YUSUF SAFI`
`ENGINE VERSION: v5.0 — 64-bit Linear Phase — ITU-R BS.1770-4`
`PROTOCOL STATUS: ACTIVE — CLINICAL DEPLOYMENT PHASE`

*The Human Variable is Corrupt. The Frequency is the Cure.*

</div>
