<!-- Standardize VantaCrypt UI and project documentation. -->
# VantaCrypt — Terminal Security Suite

VantaCrypt is an educational Python application for password checks, password generation, local credential management, and text-encryption experiments. Its terminal interface uses Rich panels and tables alongside InquirerPy keyboard menus.

> Use sample credentials while experimenting. Account passwords and vault records are currently stored without encryption at rest. Some interface labels describe stronger security than the implementation provides; see the limitations below.

## Getting started

Use Python 3.8 or newer and a terminal with Unicode and color support. Windows Terminal is a good fit for the current Windows-oriented project. A wide terminal helps the large banner, menu descriptions, and credential table fit.

Run these commands from the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe Main_UI.py
```

With dependencies already installed in your selected Python environment:

```powershell
python Main_UI.py
```

**`Main_UI.py` is the launcher.** It imports `Main` and calls `Main.main_menu()`. Running `python Main.py` currently only loads definitions and does not start the menus.

On macOS/Linux, the equivalent virtual-environment interpreter is `.venv/bin/python`. Run from the project root on every platform: data paths are relative to the working directory.

Registration creates `Data/UserData/user_data.csv` and its parent directory when needed. Vault operations create `Data/PWManagerData` when needed. No initial account is required.

## Navigation and interface

- Use Up/Down arrows to move and Enter to choose an option.
- Register an account, then log in with its username and password.
- The status strip shows guest/active status, username, UID, action count, and a vault-entry count where supplied.
- The main menu opens password checks, generation, encryption/decryption, the vault, session history, and the analytics placeholder.
- Back/Cancel options return from submenus. Logout returns to authentication; Exit closes the application.
- The current implementation clears and redraws screens and displays “Press Enter” pauses after many operations.
- Prompt wrappers catch Ctrl+C and end-of-input: menus return a Back value, text/secret/path prompts return an empty string, and confirmation prompts return false. This is not a universal application-wide exception handler.

`UI.py` owns the banner, theme, menus, prompts, status messages, reports, and tables. Purple identifies the banner, cyan is used for tool panels, gold for the vault table, and blue for history. Login and manual vault-password inputs are hidden; generated passwords and unlocked vault passwords are displayed openly.

## What is implemented

| Tool | Current behavior |
| --- | --- |
| Registration and login | CSV-backed accounts, password confirmation, assigned eight-digit UID, hidden password prompts |
| Password strength checker | Five checks: length of at least 8, uppercase, lowercase, digits, and selected symbols; a report and suggestions |
| Password generator | Length 8–128, default 16; configurable lowercase, uppercase, digits, and symbols; numeric input validation |
| Vault | Add, view, edit, and remove website/service credentials; duplicate website detection is case-insensitive |
| Vault authorization | Viewing nonempty vaults, editing, and removal require the current account password; removal asks for confirmation |
| Minimum cipher | Per-character shifts from -20 to 20; ciphertext and a separate pickle key/UID file |
| Maximum cipher | Per-character XOR using values from `secrets.randbelow(256)`; hex ciphertext and a pickle payload containing keys, UID, and a SHA-256 digest |
| Session history | Numbered, in-memory messages recorded during the current process; no persistent audit-log file |
| Intermediate cipher | Placeholder message only; Vigenère is not implemented |
| Graphs/analytics | Placeholder message only; no charts are generated |

The password generator samples from the combined selected character pool using `random.choice`. It does **not** guarantee that each selected category appears, and it does **not** use cryptographically secure randomness. The strength checker measures character rules, not entropy, breach exposure, or actual cracking time.

## Cipher files

Encryption accepts text and writes two files:

- A `.txt` ciphertext file.
- A `.dat` pickle payload with the per-character keys and owner UID. Maximum mode also stores a SHA-256 digest of the original UTF-8 text.

The expected extension is appended if it is absent. Supply existing parent directories for output paths. Existing output files trigger a warning and are then overwritten; there is no overwrite confirmation.

Decryption needs both files and checks the saved UID against the signed-in UID. Maximum mode compares a freshly calculated digest with the saved one. On a mismatch, the current code still displays the recovered text inside a failure panel.

## Project layout

```text
Project_Encrypt/
├── Main_UI.py              # Launcher: calls Main.main_menu()
├── Main.py                 # Authentication, dashboard, cipher and vault routing
├── UI.py                   # Shared presentation and input helpers
├── requirements.txt        # Direct third-party runtime dependencies
├── README.md
├── .gitignore
├── Functions/
│   ├── User_Auth.py        # CSV accounts and login
│   ├── PW_Strength.py      # Five-rule password assessment
│   ├── PW_Generator.py     # Configurable random.choice generator
│   ├── PW_Manager.py       # Pickle vault loading/saving and credential operations
│   ├── Encryptions.py      # Shift/XOR demonstrations; intermediate placeholder
│   ├── Decryption.py      # Reverse transformations and digest check
│   ├── Action_Hist.py      # In-memory session messages
│   └── Graph.py            # Analytics placeholder
└── Data/
    ├── UserData/user_data.csv
    └── PWManagerData/password_vault_<UID>.dat
```

CSV records contain `Username`, `Password`, and `UniqueID`. Each vault file contains consecutive pickled dictionaries with `Website`, `Username`, `Password`, `Notes`, and `UID`. Logout does not clear the process-wide history list; closing the process does.

## Dependencies

| Package | Used for |
| --- | --- |
| `InquirerPy>=0.3.4` | Arrow-key menus, text/secret/path input, and confirmations |
| `rich>=13.0.0` | Colors, panels, tables, layout, and progress-bar rendering |

Pip resolves their transitive dependencies. `csv`, `hashlib`, `os`, `pickle`, `random`, `secrets`, `string`, and `sys` are Python standard-library modules and do not belong in requirements.txt.

`pwinput`, `pyfiglet`, and `matplotlib` are not imported by the current source. Hidden input comes from InquirerPy, the banner is embedded text, and graphs remain a placeholder. The requirements specify minimum versions, not an exact reproducible lockfile.

## Current limitations

- **Unencrypted storage:** account passwords are plaintext CSV values; vault records are unencrypted pickle data, despite UI messages mentioning encrypted storage.
- **Trusted files only:** loading pickle data can execute code. Only use locally trusted vault and key files.
- **Educational cryptography:** the custom ciphers and editable UID fields are not robust access control or authenticated encryption. The SHA-256 value is an unkeyed digest, not a digital signature. AES is not implemented, despite appearing in the status-strip label.
- **Character limits:** maximum mode processes Unicode code points into a bytearray and fails for characters above U+00FF. Minimum mode can produce invalid Unicode values near character boundaries and does not reliably support every text input.
- **Partial error handling:** some file and input errors are caught, but not every operation is protected. Corrupt vault reads may return records loaded before the failure; this is not full corruption recovery.
- **Logout implementation:** logout calls `main_menu()` recursively. Repeated logout/login cycles accumulate call frames.
- **Terminal output:** long descriptions and fixed-width table columns may wrap; Unicode art and emoji require a compatible font/encoding. There is no explicit ASCII fallback for all displays.

Avoid committing real credentials, vault files, or cipher keys. The ignore rules cover local data and environments, but **ignore rules do not remove files already tracked by Git**.

## Development checks

Check syntax without launching the interactive app:

```powershell
python -m compileall -q Main_UI.py Main.py UI.py Functions
```

Check that the two direct dependencies can be imported:

```powershell
python -c "import rich, InquirerPy; print('Runtime dependencies available')"
```

There is currently no automated test suite in the project. For manual checks, use dummy accounts and sample text: registration/login, each password tool, vault add/view/edit/remove, cipher round trips, and logout. These checks do not establish cryptographic security.

## Contributors

- Sasank
- Raphael
