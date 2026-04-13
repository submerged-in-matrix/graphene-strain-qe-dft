# Bash Scripting — Quick Reference for Python Users

## The Shebang and Settings

`#!/bin/bash` is like Python's `if __name__ == "__main__"` — tells the system which interpreter to use. `set -e` means "exit immediately if any command fails" — like wrapping everything in a try/except that always raises.

---

## Variables

No spaces around `=`. `A0=2.460000` works, `A0 = 2.460000` breaks. Reference with `$A0` or `${A0}`. No types — everything is a string. This is the #1 bash gotcha.

---

## Arrays

`STRAINS=(6 8 10 12 14 16 18)` — parentheses, space-separated (no commas). Access with `${STRAINS[@]}` for all elements.

---

## Loops

```bash
for STRAIN in "${STRAINS[@]}"; do
    ...
done
```

The `do`/`done` pair is bash's equivalent of Python's colon + indentation.

---

## Math

Bash can't do floating point. `bc -l` is the calculator: `echo "1 + 6 / 100" | bc -l` gives `1.06000...`. The `|` (pipe) sends output of one command as input to the next — like chaining functions. `xargs printf "%.6f"` formats the result.

---

## String Formatting

`printf "0p%02d" 6` → `0p06`. Same syntax as Python's `%` formatting.

---

## Here-Documents (the big one)

```bash
cat > filename.in << EOF
content here
variables like ${A1X} get expanded
EOF
```

This is how the script writes input files. Everything between `<< EOF` and `EOF` gets written to the file, with variables substituted. It's like Python's `f"""..."""` written directly to a file.

---

## Conditionals

```bash
if grep -q "convergence" file.out; then
    echo "success"
else
    continue  # skip to next loop iteration
fi
```

`grep -q` searches silently (returns true/false). `if/then/else/fi` — note `fi` is `if` backwards.

---

## Command Substitution

`EF=$(grep "Fermi energy" file.out | tail -1 | awk '{print $5}')` — the `$(...)` captures command output into a variable. Like Python's `subprocess.check_output()`.

---

## Key Commands — Bash vs Python

| Bash | Python equivalent | What it does |
|------|-------------------|--------------|
| `echo` | `print()` | Print to screen |
| `cat > file` | `open(file, 'w')` | Write to file |
| `grep "text" file` | `if "text" in line` | Search for pattern |
| `awk '{print $5}'` | `line.split()[4]` | Extract the 5th field |
| `tail -1` | `lines[-1]` | Last line |
| `head -1` | `lines[0]` | First line |
| `|` (pipe) | chained methods | Pass output → input |
| `mv` | `shutil.move()` | Move file |
| `mkdir -p` | `os.makedirs(exist_ok=True)` | Create directory |
| `2>&1` | `stderr=subprocess.STDOUT` | Merge error into normal output |

---

## The Pipe Chain Pattern

This is bash's superpower. Example:

```bash
grep "Fermi" file | tail -1 | awk '{print $5}'
```

Reads as: find lines containing "Fermi" → take the last one → extract the 5th word. Each `|` feeds the previous command's output to the next — composing simple tools into complex operations.
