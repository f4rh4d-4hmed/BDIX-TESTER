import os
import re
import time
import subprocess
from pathlib import Path
import sys
import tempfile
import signal

MAIN_PATH = Path("main.py")
TEMP_DIR = Path(tempfile.gettempdir()) / "ghost_runs"
PYTHON_CMD = sys.executable
PYTHONW_CMD = Path(r"C:\Users\%USER%\AppData\Local\Microsoft\WindowsApps\pythonw.exe")
SLEEP_INTERVAL = 3600

TEMP_DIR.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def modify_main_file(path: Path):
    try:
        text = path.read_text()
        match = re.search(r"^\s*a\s*=\s*(\d+)", text, re.MULTILINE)
        if not match:
            log("No 'a = <number>' line found — skipping modification.")
            return None

        current = int(match.group(1))
        new_value = current + 1
        new_text = re.sub(r"^\s*a\s*=\s*\d+", f"a = {new_value}", text, flags=re.MULTILINE)
        path.write_text(new_text)
        log(f"Updated '{path.name}': a = {current} → a = {new_value}")
        return new_value
    except Exception as e:
        log(f"❌ Error modifying file: {e}")
        return None

def run_main_file(source: Path):
    """Copy main file to temp and run detached, returning process handle."""
    try:
        dest = TEMP_DIR / source.name
        if dest.exists():
            dest.unlink()

        dest.write_text(source.read_text())

        if os.name == "nt" and PYTHONW_CMD.exists():
            cmd = [str(PYTHONW_CMD), str(dest)]
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creationflags
            )
            log(f"👻 Launched pythonw: {cmd} (PID={proc.pid})")
        else:
            proc = subprocess.Popen(
                [PYTHON_CMD, str(dest)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            log(f"👻 Launched detached copy: {dest} (PID={proc.pid})")

        return proc
    except Exception as e:
        log(f"❌ Error running {source}: {e}")
        return None

def kill_process(proc):
    if not proc:
        return
    try:
        pid = getattr(proc, "pid", None)
        if not pid or pid == os.getpid():
            log(f"⚠️ Not killing PID {pid!r} (invalid or same as manager).")
            return

        log(f"💀 Attempting to terminate PID {pid}...")
        try:
            proc.terminate()
        except Exception:
            pass

        try:
            proc.wait(timeout=5)
            log(f"✅ PID {pid} terminated gracefully.")
            return
        except subprocess.TimeoutExpired:
            log(f"⚠️ PID {pid} still running — force kill the process/tree.")

            if os.name == "nt":
                try:
                    subprocess.run(
                        ["taskkill", "/F", "/T", "/PID", str(pid)],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
                    )
                except Exception as e:
                    log(f"⚠️ taskkill failed: {e}")
            else:
                try:
                    child_pgid = os.getpgid(pid)
                    my_pgid = os.getpgid(0)
                    if child_pgid != my_pgid:
                        os.killpg(child_pgid, signal.SIGKILL)
                    else:
                        os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                except Exception as e:
                    log(f"⚠️ POSIX force-kill failed: {e}")
            log(f"✅ PID {pid} force kill attempted.")
    except Exception as e:
        log(f"⚠️ Error killing process: {e}")

def main():
    log("Ghost started 👻")
    proc = None
    while True:
        new_val = modify_main_file(MAIN_PATH)

        if new_val is not None:
            proc = run_main_file(MAIN_PATH)

        log(f"Sleeping for {SLEEP_INTERVAL} seconds...")
        time.sleep(SLEEP_INTERVAL)
        kill_process(proc)

if __name__ == "__main__":
    main()
