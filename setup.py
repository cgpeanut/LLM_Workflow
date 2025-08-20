import os, sys, subprocess, time, json, requests, textwrap
from pathlib import Path

def sh(cmd, check=True):
    """Run a shell command, stream output."""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in p.stdout:
        print(line, end="")
    p.wait()
    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")

if not Path("/usr/local/bin/ollama").exists() and not Path("/usr/bin/ollama").exists():
    print("🔧 Installing Ollama ...")
    sh("curl -fsSL https://ollama.com/install.sh | sh")
else:
    print("✅ Ollama already installed.")

try:
    import gradio
except Exception:
    print("🔧 Installing Gradio ...")
    sh("pip -q install gradio==4.44.0")

###

def start_ollama():
    try:
        requests.get("http://127.0.0.1:11434/api/tags", timeout=1)
        print("✅ Ollama server already running.")
        return None
    except Exception:
        pass
    print("🚀 Starting Ollama server ...")
    proc = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(60):
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:11434/api/tags", timeout=1)
            if r.ok:
                print("✅ Ollama server is up.")
                break
        except Exception:
            pass
    else:
        raise RuntimeError("Ollama did not start in time.")
    return proc

server_proc = start_ollama()

###

MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b-instruct")
print(f"🧠 Using model: {MODEL}")
try:
    tags = requests.get("http://127.0.0.1:11434/api/tags", timeout=5).json()
    have = any(m.get("name")==MODEL for m in tags.get("models", []))
except Exception:
    have = False

if not have:
    print(f"⬇️  Pulling model {MODEL} (first time only) ...")
    sh(f"ollama pull {MODEL}")

###
