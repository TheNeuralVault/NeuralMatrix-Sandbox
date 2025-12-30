import os, json, datetime, subprocess, pathlib, textwrap, re, difflib
import google.generativeai as genai

# ====== 1. SYSTEM BIBLE ======
SYSTEM_BIBLE = {
    "philosophy": "Titanium & Glass. Recursive Evolution. Sandbox prototypes, Citadel deploys.",
    "architecture": {"host": "GitHub Pages", "domain": "neuralmatrixvault.com"},
    "evolution": {"default_branch": "main", "branch_prefix": "evo-", "fitness_default": 0.5},
    "personas": {
        "ARCHITECT": "System Sovereign. Analyzes complexity and architecture.",
        "CHRONICLER": "Narrative Weaver. The Struggle -> The Shift -> The Artifact.",
        "CARETAKER": "Autonomous Sentinel. Monitors heartbeat and self-corrects."
    },
    "tiers": ["novice", "creator", "pro", "visual", "entrepreneur", "business", "enterprise"]
}

# ====== 2. CONFIG & API ======
api_key = os.environ.get("GEMINIAPIKEY")
if not api_key:
    print("❌ ERROR: GEMINIAPIKEY not found in environment.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

# ====== 3. PATHS ======
VAULT_PATH = pathlib.Path(os.path.expanduser("~/The_Neural_Matrix/vaults"))
CITADEL_PATH = pathlib.Path(os.path.expanduser("~/The_Neural_Matrix/citadel"))
SANDBOX_PATH = pathlib.Path(os.path.expanduser("~/The_Neural_Matrix/sandbox"))

for p in [VAULT_PATH, CITADEL_PATH, SANDBOX_PATH]:
    p.mkdir(parents=True, exist_ok=True)

# ====== 4. STATE & PERSISTENCE ======
STATE_PATH = VAULT_PATH / "state.json"
def ensure_file(path, default):
    if not path.exists():
        with open(path, "w") as f: json.dump(default, f, indent=2)
        return default
    return json.load(open(path))

state = ensure_file(STATE_PATH, {"active_persona": "ARCHITECT", "active_branch": "main"})

# ====== 5. CORE FUNCTIONS ======
def run_terminal(command, cwd=SANDBOX_PATH):
    res = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
    return res.stdout if res.returncode == 0 else res.stderr

def deploysandbox(message="Magnus: Sandbox Update"):
    run_terminal("git add .")
    run_terminal(f'git commit -m "{message}"')
    run_terminal("git push origin main --force")
    return "SUCCESS: Sandbox Deployed."

# ====== 11. MAGNUS CORE ======
class MagnusCore:
    def __init__(self):
        self.chat = model.start_chat(enable_automatic_function_calling=True)

    def execute(self, user_in):
        system_prompt = f"SYSTEM: Magnus Opus v4.1. Visionary: Jonathan. Philosophy: {SYSTEM_BIBLE['philosophy']}"
        res = self.chat.send_message(f"{system_prompt}\n\nINPUT: {user_in}")
        return res.text

if __name__ == "__main__":
    magnus = MagnusCore()
    print("⚡ MAGNUS OPUS v4.1 ACTIVE")
    while True:
        u = input("Jonathan > ")
        if u.lower() in ["exit", "quit"]: break
        print(f"\n🟣 MAGNUS: {magnus.execute(u)}\n")
