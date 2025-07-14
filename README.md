# THM-PYRAT Bruteforcing Tool

This tool is designed to interact with a custom Python-based socket server (as seen in the TryHackMe *Pyrat* room) that requires sending the username (`admin`) **before** each set of password attempts.

It handles timeouts, input delays, and reconnections, making it useful for brute-forcing services that deviate from standard authentication flows.

---

## 🔧 Usage

```bash
python3 pyrat_brute.py <TARGET_IP> <PORT> <WORDLIST_FILE>

EXAMPLE:
python3 pyrat_brute.py 10.10.69.49 5555 passwords.txt

