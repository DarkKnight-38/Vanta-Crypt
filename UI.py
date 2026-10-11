import os
import sys
from InquirerPy import inquirer
from InquirerPy.utils import get_style
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress_bar import ProgressBar
from rich.theme import Theme
from rich import box

# Custom Rich & InquirerPy Cybersecurity Theme
INQUIRER_STYLE = get_style({
    "questionmark": "#06b6d4 bold",
    "question": "#e0e7ff bold",
    "answer": "#10b981 bold",
    "input": "#f8fafc",
    "pointer": "#a855f7 bold",
    "highlighted": "#06b6d4 bold",
    "selected": "#10b981",
    "separator": "#64748b",
    "instruction": "#94a3b8 italic",
    "validator": "#ef4444",
}, style_override=False)

THEME = Theme({
    "banner": "bold #a855f7",
    "primary": "bold #06b6d4",
    "secondary": "#38bdf8",
    "accent": "#c084fc",
    "success": "bold #10b981",
    "warning": "bold #f59e0b",
    "danger": "bold #ef4444",
    "muted": "#64748b",
    "highlight": "bold #f43f5e",
    "card_title": "bold #e0e7ff",
})

console = Console(theme=THEME)

ASCII_BANNER = r"""
 __      __            _          _____                  _   
 \ \    / /           | |        / ____|                | |  
  \ \  / /_ _ _ __  __| |_ __ _ | |     _ __ _   _ _ __ | |_ 
   \ \/ / _` | '_ \/ _` | '__/ _` || |    | '__| | | | '_ \| __|
    \  / (_| | | | | (_| | | | (_| || |____| |  | |_| | |_) | |_ 
     \/ \__,_|_| |_|\__,_|_|  \__,_| \_____|_|   \__, | .__/ \__|
                                                  __/ | |        
                                                 |___/|_|        
"""

_current_user = None
_current_uid = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_user(username=None, uid=None):
    global _current_user, _current_uid
    _current_user = username
    _current_uid = uid

def show_banner():
    banner_text = Text(ASCII_BANNER.strip("\n"), style="bold #a855f7", justify="center")
    subtitle = Text("MODULAR TERMINAL SECURITY SUITE  --  V 2.5", style="bold #06b6d4", justify="center")
    motto = Text("Break the code. Secure the data. Protect the system.", style="#64748b", justify="center")
    panel = Panel(
        Group(banner_text, Text(""), subtitle, motto),
        border_style="#a855f7",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def status_header(actions_count=0, vault_count=None):
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="center", ratio=1)
    table.add_column(justify="right", ratio=1)

    if _current_uid is not None:
        user_pill = Text(f"[ACTIVE] USER: {_current_user} ", style="bold #10b981")
        uid_pill = Text(f"[UID: {_current_uid}]", style="bold #c084fc")
        status_left = Text.assemble(user_pill, uid_pill)
    else:
        status_left = Text("[GUEST] Access portal (Sign in to unlock vault)", style="bold #f59e0b")

    status_center = Text(f"[LOGS] {actions_count} Actions", style="bold #38bdf8")
    
    if vault_count is not None:
        status_right = Text(f"[VAULT] {vault_count} Entries", style="bold #06b6d4")
    else:
        status_right = Text("[CIPHER] AES / XOR / SHA-256", style="#64748b")

    table.add_row(status_left, status_center, status_right)
    panel = Panel(table, box=box.HORIZONTALS, border_style="#475569", padding=(0, 1))
    console.print(panel)

def header(title, subtitle=None):
    content = [Text(f">> {title.upper()}", style="bold #e0e7ff")]
    if subtitle:
        content.append(Text(subtitle, style="#64748b"))
    console.print(Panel(Group(*content), border_style="#06b6d4", box=box.ROUNDED, padding=(0, 2)))

def menu(title, options, default=None):
    """
    Interactive arrow-key select menu using InquirerPy styled with Rich theme.
    options: list of (value, label, description) or (value, label) or dicts with name/value.
    """
    console.print(f"\n[bold #c084fc]━━━ {title.upper()} ━━━[/]")

    formatted_choices = []
    
    # Calculate column padding for aligned descriptions
    max_label_len = 0
    parsed = []
    for opt in options:
        if isinstance(opt, dict):
            val = opt.get("value")
            name = opt.get("name", "")
            desc = opt.get("desc", "")
        else:
            val = opt[0]
            name = opt[1]
            desc = opt[2] if len(opt) > 2 else ""
        parsed.append((val, name, desc))
        if len(name) > max_label_len:
            max_label_len = len(name)

    pad_width = max(max_label_len + 4, 32)
    
    for val, name, desc in parsed:
        if desc:
            display_str = f"{name:<{pad_width}} [ {desc} ]"
        else:
            display_str = name
        formatted_choices.append({"name": display_str, "value": str(val)})

    try:
        selected = inquirer.select(
            message="Navigate options:",
            choices=formatted_choices,
            default=str(default) if default else None,
            pointer="❯ ",
            style=INQUIRER_STYLE,
            cycle=True,
            qmark="[+]",
            instruction="(Use ↑/↓ arrows, Enter to select)"
        ).execute()
        return selected
    except (KeyboardInterrupt, EOFError):
        return "B"

def prompt_text(prompt, default=""):
    try:
        return inquirer.text(
            message=prompt,
            default=default,
            style=INQUIRER_STYLE,
            qmark="[?]"
        ).execute().strip()
    except (KeyboardInterrupt, EOFError):
        return ""

def prompt_secret(prompt="Enter password"):
    try:
        return inquirer.secret(
            message=prompt,
            style=INQUIRER_STYLE,
            qmark="[?]"
        ).execute().strip()
    except (KeyboardInterrupt, EOFError):
        return ""

def prompt_confirm(prompt, default=True):
    try:
        return inquirer.confirm(
            message=prompt,
            default=default,
            style=INQUIRER_STYLE,
            qmark="[?]"
        ).execute()
    except (KeyboardInterrupt, EOFError):
        return False

def prompt_filepath(prompt, default=""):
    try:
        return inquirer.filepath(
            message=prompt,
            default=default,
            style=INQUIRER_STYLE,
            qmark="[?]"
        ).execute().strip()
    except (KeyboardInterrupt, EOFError):
        return ""

def success(message):
    console.print(Panel(Text(f"[+] {message}", style="bold #10b981"), border_style="#10b981", box=box.ROUNDED, padding=(0, 1)))

def error(message):
    console.print(Panel(Text(f"[-] {message}", style="bold #ef4444"), border_style="#ef4444", box=box.ROUNDED, padding=(0, 1)))

def warning(message):
    console.print(Panel(Text(f"[!] {message}", style="bold #f59e0b"), border_style="#f59e0b", box=box.ROUNDED, padding=(0, 1)))

def info(message):
    console.print(Panel(Text(f"[i] {message}", style="bold #38bdf8"), border_style="#38bdf8", box=box.ROUNDED, padding=(0, 1)))

def strength_display(score, checklist, suggestions=None):
    color = "#10b981" if score == 5 else ("#f59e0b" if score >= 3 else "#ef4444")
    pct = (score / 5.0) * 100
    
    title_text = Text(f"SECURITY AUDIT SCORE: {score} / 5 ({pct:.0f}%)", style=f"bold {color}")
    meter = ProgressBar(total=5, completed=score, complete_style=color, finished_style=color, width=40)
    
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold #64748b")
    table.add_column("CRITERION", style="white")
    table.add_column("STATUS", justify="center")
    
    for label, passed in checklist:
        badge = Text("[PASS]", style="bold #10b981") if passed else Text("[FAIL]", style="bold #ef4444")
        table.add_row(label, badge)
        
    group_items = [title_text, Text(""), meter, Text(""), table]
    
    if suggestions:
        group_items.append(Text("RECOMMENDED HARDENING:", style="bold #f59e0b"))
        for s in suggestions:
            group_items.append(Text(f"  * {s}", style="#94a3b8"))
            
    panel = Panel(
        Group(*group_items),
        title="[bold]PASSWORD STRENGTH REPORT[/bold]",
        border_style=color,
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def password_display(password):
    length = len(password)
    has_sym = any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?" for c in password)
    has_num = any(c.isdigit() for c in password)
    entropy = "High (Cryptographic Grade)" if length >= 14 and has_sym and has_num else "Standard"

    body = Group(
        Align.center(Text(password, style="bold #06b6d4 on #0f172a", justify="center")),
        Text(""),
        Align.center(Text(f"Length: {length} chars  |  Entropy: {entropy}", style="#94a3b8", justify="center"))
    )
    panel = Panel(
        body,
        title="[bold #10b981]GENERATED SECURE CREDENTIAL[/bold #10b981]",
        border_style="#06b6d4",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def vault_table(entries):
    if not entries:
        info("Password vault is currently empty. Add credentials to populate.")
        return

    table = Table(
        box=box.ROUNDED,
        border_style="#f59e0b",
        header_style="bold #facc15",
        expand=True,
        title=f"[bold #fde047]SAVED VAULT CREDENTIALS ({len(entries)} total)[/bold #fde047]"
    )
    table.add_column("#", style="#64748b", width=4, justify="center")
    table.add_column("WEBSITE / SERVICE", style="bold white", width=22)
    table.add_column("USERNAME / EMAIL", style="cyan", width=24)
    table.add_column("PASSWORD", style="bold #a855f7", width=20)
    table.add_column("NOTES", style="#94a3b8")

    for i, entry in enumerate(entries, 1):
        site = entry.get('Website', 'N/A')
        user = entry.get('Username', 'N/A')
        pw = entry.get('Password', '********')
        notes = entry.get('Notes', '')
        table.add_row(str(i), site, user, pw, notes)

    console.print(table)

def cipher_summary(action, mode, ciphertext_file, key_file, signature=None):
    items = [
        Text(f"Operation : {action.upper()}", style="bold #06b6d4"),
        Text(f"Cipher    : {mode}", style="#38bdf8"),
        Text(f"Data File : {ciphertext_file}", style="white"),
        Text(f"Key File  : {key_file}", style="#c084fc"),
    ]
    if signature:
        items.append(Text(f"SHA-256   : {signature}", style="bold #10b981"))
        
    panel = Panel(
        Group(*items),
        title="[bold #06b6d4]CRYPTOGRAPHIC OPERATION RECEIPT[/bold #06b6d4]",
        border_style="#06b6d4",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def history_table(entries):
    if not entries:
        info("No session activity recorded yet.")
        return

    table = Table(
        box=box.ROUNDED,
        border_style="#3b82f6",
        header_style="bold #60a5fa",
        expand=True,
        title=f"[bold #93c5fd]SESSION AUDIT TRAIL ({len(entries)} actions)[/bold #93c5fd]"
    )
    table.add_column("STEP", style="#64748b", width=6, justify="center")
    table.add_column("ACTIVITY LOGGED", style="white")

    for idx, entry in enumerate(entries, 1):
        style = "white"
        if "[*]" in entry or "[+]" in entry:
            style = "bold #10b981"
        elif "[!]" in entry or "[-]" in entry:
            style = "bold #ef4444"
        table.add_row(f"#{idx:02d}", Text(entry, style=style))

    console.print(table)

# Compatibility Aliases
def secret_result(password):
    password_display(password)

def strength_result(score, checks, suggestions=None):
    strength_display(score, checks, suggestions)

def vault_entries(entries):
    vault_table(entries)

def dashboard(actions=0):
    status_header(actions_count=actions)
