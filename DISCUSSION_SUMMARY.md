# MaxL Project Discussion Summary

## Project Overview
MaxL is a custom interactive shell/interpreter being developed in Python. It uses:
- `prompt_toolkit` for interactive input
- `rich` library for colored terminal output
- JSON-based files (`colors.json`, `iMem.json`) for configuration and simulated filesystem
- Custom command set (`ls`, `get`, `edit`, `new`, `calc`, `help`, `exit`, etc.)

Current project structure:
```
maxl/
├── main.py              # Entry point: loads modules.std and calls std.load()
├── modules/
│   └── std.py           # Core shell implementation: prompt loop, commands, JSON loading
├── json/
│   ├── colors.json      # Color/theme definitions
│   ├── iMem.json        # In-memory filesystem simulation
│   └── settings.json    # Additional settings
├── other/
│   └── resursi.md       # Link to ASCII art generator used for branding
└── log.txt              # Simple log file
```

## Naming Discussion: ">maxl:"
**Problem:** The name `>maxl:` contains shell metacharacters:
- `>` is output redirection in all major shells (bash, zsh, PowerShell, CMD)
- `:` is a shell builtin (no-op command) in Unix shells
- Typing `>maxl: arg` would redirect stdout to a file named `maxl:` and run `:` with `arg` as argument

**Recommendation:** 
- Keep the executable/command name **shell-safe** (e.g., `maxl`, `maxl-sh`, `maximl`)
- Preserve the "**>maxl:**" branding **inside the shell's UI** (title, prompts, output) where it belongs

**Current Implementation:** 
Your code already displays `[italic gray66]>maxl: {version 0.0.1}` in the `title()` function (line 84 of `std.py`) and uses distinctive prompts like `[output].>>> ` and `[bounders]<:>`. This is the correct place for the branding.

**Action:** 
- When distributing/packaging, name the executable `maxl` (or similar)
- Users run `python main.py` (or eventually `maxl` if packaged)
- They immediately see your ">maxl:" branded interface
- Best of both worlds: usable command + distinctive identity

## Command System Improvements
Current `std.py` uses a long `if/elif` chain in the `interpreter()` function (lines 94-116) to dispatch commands. This becomes unwieldy as features grow.

### Recommended Approach: JSON-Based Command Declarations
Move command metadata (names, help text, usage, categories) to a JSON file, keeping implementations as functions in `std.py`.

#### Example `commands.json`:
```json
{
  "help": {
    "function": "help_command",
    "help_text": "list of commands",
    "usage": "help",
    "category": "core"
  },
  "exit": {
    "function": "exit_command",
    "help_text": "end >MAXL:",
    "usage": "exit",
    "category": "core"
  },
  "ls": {
    "function": "ls_command",
    "help_text": "lists imem of id (none to root)",
    "usage": "ls [id]",
    "category": "navigation"
  },
  "get": {
    "function": "get_command",
    "help_text": "print value of imem at id",
    "usage": "get [id]",
    "category": "inspection"
  },
  "edit": {
    "function": "edit_command",
    "help_text": "edits imem at id",
    "usage": "edit [id]",
    "category": "editing"
  },
  "new": {
    "function": "new_command",
    "help_text": "new val at id",
    "usage": "new [type] [name] [id]",
    "category": "creation"
  },
  "calc": {
    "function": "calc_command",
    "help_text": "simple calculator",
    "usage": "calc [eq]",
    "category": "utilities"
  },
  "open": {
    "function": "open_command",
    "help_text": "from root/newest to nextId",
    "usage": "open [nextId]",
    "category": "navigation"
  },
  "currentdir": {
    "function": "currentdir_command",
    "help_text": "info on the current dir opened",
    "usage": "currentdir",
    "category": "info"
  }
}
```

#### Implementation Changes in `std.py`:
1. Load `commands.json` at module startup
2. Build a `COMMANDS` dictionary mapping names to `{function, help_text, usage, category}`
3. Rewrite `interpreter()` to dispatch via this dictionary
4. Update `help_command()` to generate help dynamically from the JSON

**Benefits:**
- Add/remove/change commands by editing JSON only (no Python code changes for basic modifications)
- Clear separation: declarations (JSON) vs. implementation (Python functions)
- Easy to categorize commands for organized help output
- Metadata extensibility (add `requires_args`, `aliases`, `examples`, etc.)

#### Alternative: Hybrid Decorator + JSON
- Use `@register_command` decorator in `std.py` for automatic function discovery
- Store help text, usage, category in JSON
- JSON maps command names to metadata; decorators handle registration
- Gives both auto-discovery and configurable metadata

## Future Project: maxl+ (Real Filesystem)
While the current MaxL uses a simulated filesystem (`iMem.json`), a separate `maxl+` project could operate on the actual filesystem.

### Motivation
- **Learning/Safety:** Current `maxl` is safe for experimentation (changes only affect `iMem.json`)
- **Power/Flexibility:** `maxl+` would enable real file operations, application launching, etc.

### Proposed Features for `maxl+`:
1. **Real File Editing**
   - Edit actual text files with line-by-line interface
   - Safety: backup files before editing (`.bak`), confirmation prompts for destructive ops
2. **Opening Files/Applications**
   - Use `os.startfile(filepath)` on Windows to open with associated application
   - Option to specify app: `open --app notepad file.txt`
3. **Real Directory Navigation**
   - `ls` shows actual directory contents
   - `cd` changes real working directory (with `pathlib.Path` for cross-platform)
4. **Safety Features**
   - `--real` flag to toggle between simulated and real modes
   - Confirmation prompts for `rm`, `mv`, etc.
   - Restrict operations to safe directories unless overridden

### Implementation Considerations:
- Use `pathlib.Path` for robust cross-path handling
- Wrap risky operations in try/except with informative error messages
- Consider a command whitelist/blacklist for sensitive operations
- Could share command infrastructure with main MaxL (e.g., same JSON declaration system)

### Relationship to Main Project:
- **Option A:** Separate repository (`maxl-plus`) for complete isolation
- **Option B:** Build as a mode/flag within same codebase (`python main.py --real`)
- **Option C:** Start with simulated, add "escape hatches" (`edit --real file.txt`)

**Recommendation:** Begin as a separate project to maintain the simplicity and safety of the learning-focused MaxL, then explore integration later if desired.

## Next Steps
1. **Implement JSON Command Declarations**
   - Create `commands.json` in project root
   - Modify `std.py` to load JSON and dispatch via dictionary
   - Update `help_command()` to generate dynamic help
   - Test adding a new command via JSON only

2. **Consider Module-Based Structure (Long-Term)**
   - If project grows significantly, refactor commands into separate files in `modules/`
   - Each file: class inheriting from `Command(base)` with `name`, `help_text`, `execute(args, context)`
   - `main.py` auto-discovers and loads all commands via `pkgutil.iter_modules`

3. **Plan maxl+ Development**
   - Define core feature set (file editing, opening, basic navigation)
   - Implement safety-first approach (backups, confirmations)
   - Consider sharing command infrastructure with main MaxL

4. **Documentation & Branding**
   - Keep `>maxl:` branding in UI (title, prompts)
   - Ensure executable name is shell-safe (`maxl`)
   - Update `resursi.md` or add README with project goals and usage

## Appendix: Observations from Current Code

### main.py (Lines 1-4)
```python
from modules import std

if __name__ == "__main__":
    std.load() 
```
- Simple entry point; delegates initialization to `std.load()`

### modules/std.py highlights:
- **Global state:** `glDir` (project root), `colors`, `iMem` loaded from JSON
- **Loading process:** `load()` clears screen, loads JSONs, shows title with progress bar, sets `running=True`, calls `ask(running)`
- **Title/Prompt:** Custom ASCII art with `[italic gray66]>maxl: {version 0.0.1]` and prompts like `[output].>>> `
- **Command loop:** `ask()` -> `interpreter()` -> command dispatch via `if/elif`
- **Key functions:** 
  - `getFolderById(id)`, `getItemById(id)` for navigating `iMem` tree
  - `ls()`, `get()`, `edit()`, `new()`, `calc()`, `help()`, etc.
  - Uses `itertools.cycle` for spinner animation during load
- **Sandboxed:** All file operations are on `iMem.json` (in-memory JSON only)

### json/ folder:
- `colors.json`: Defines color/theme values used in `rich` printing
- `iMem.json`: Simulated filesystem structure (folders, files with `name`, `id`, `type`, `children`/`content`)
- `settings.json`: Additional configuration (content not examined)

### other/resursi.md
- Contains link to [patorjk.com/taag/](https://patorjk.com/software/taag/#p=display&f=Slant+Relief&t=%3EMAXL%3A&x=sleek&v=4&h=4&w=80&we=false) used to generate the ">MAXL:" ASCII art seen in the title

---

*Summary created to capture key decisions, recommendations, and action items from our discussion about the MaxL project.*