# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

XHS Studio is a desktop automation tool for Xiaohongshu (小红书). It batch-edits and re-publishes existing notes on the XHS Creator platform (`creator.xiaohongshu.com`) to boost visibility. Each account runs in its own Chrome persistent profile via Playwright, with human behavior simulation (randomized mouse movements, typing delays, scroll patterns, rest breaks) to avoid detection.

## Commands

```bash
# Run the application
python main.py

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser (required after first install)
playwright install chromium

# Build Windows executable
build_exe.bat   # PyInstaller, outputs dist/XHS助手.exe
```

No test suite exists in this project.

## Architecture

### Async Model

The app bridges PySide6 (Qt) and Python asyncio using `qasync`. `main.py` creates a `QEventLoop` that replaces the default asyncio event loop, so all `async/await` code runs within the Qt event loop. All Playwright calls are async.

### GUI Layer (`app/`)

- **`MainWindow`** — top-level window; owns `AccountManager`, `BrowserManager`, `XHSOperator` instances. Provides toolbar (add/open-all/run-all/close-all, batch-size spinner) and a scrollable list of `AccountCard` widgets. Exposes `update_status()`, `update_progress()`, `update_fail()` callbacks that `XHSOperator` calls from async context to update the UI.
- **`AccountCard`** — per-account widget showing name, status, progress, fail count, and action buttons (open/continue/restart/stop/delete).

### Core Layer (`core/`)

- **`AccountManager`** — CRUD for accounts stored in `config/accounts.json`. Each account: `{id, name, user_data_dir}`. `delete_account()` also removes the `userdata/` directory.
- **`BrowserManager`** — wraps Playwright async API. Uses `channel='chrome'` (system Chrome) with persistent contexts under `userdata/`. `open_account()` navigates to `creator.xiaohongshu.com` and polls the URL until login is detected.
- **`XHSOperator`** — the automation engine. Key flow: `enter_note_manager()` → `get_note_list()` (scrapes note IDs from `data-impression` DOM attributes) → `continue_round()` loops through notes calling `process_note()` → each note: hover card → click edit → focus ProseMirror/Tiptap editor → append random word via `human_type()` → click publish → enforce 150-180s minimum time. Rest breaks every 3-7 notes.
- **`human.py`** — human behavior simulation. `human_click()`, `human_type()`, `human_type_with_typo()` (5% typo rate), `simulate_reading()`, `move_to_locator()`, various wait/think functions, `finish_with_target_time()` (2.5-3 min/note), `rest_after_batch()` (3-20 min), `startup_delay()` (60-120s between accounts).
- **`ProgressManager`** — persists per-account `{round, last_note_id}` to `data/progress.json`. Enables resume after interruption.

### Data Storage

- `config/accounts.json` — account definitions
- `data/progress.json` — per-account progress (round number, last processed note ID)
- `userdata/<uuid>/` — Chromium persistent profile directories (one per account)

### Task Cancellation

`XHSOperator` uses a `stop_flags` dict (keyed by account ID) to support cooperative cancellation. `stop_task()` sets a flag; the processing loop checks it between notes.

## Key Conventions

- No `__init__.py` files in `app/` or `core/` — imports work from the project root.
- All browser interactions are non-headless (`headless=False`) so the user can observe.
- Progress is saved after each note, enabling mid-batch resume.
- The word bank in `human.py:get_random_word()` contains Chinese real-estate terms — customize there to change appended content.
