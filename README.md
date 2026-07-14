# MaxL

MaxL is an interactive shell/interpreter built by me in Python that runs in a simulated filesystem (iMem.json). It was made as a passion project

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/maxl.git
cd maxl

# Install in editable mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

After installation, run MaxL by typing:

```bash

maxl
```

## Usage

Once MaxL is running, you'll see the branded prompt:

```
>maxl: {version 0.0.1}
```

Available commands:

- `help` - list of commands
- `ls [id]` - list contents of simulated filesystem
- `get [id]` - display file contents
- `edit [id]` - edit a file line-by-line
- `new [type] [name] [id]` - create new file/folder
- `calc [eq]` - simple calculator
- `exit` - leave MaxL

All file operations are virtual and affect only `iMem.json` - your real files are never touched.

## Project Structure

```
maxl/
├── main.py              # Entry point
├── modules/
│   └── std.py           # Core shell implementation
├── json/
│   ├── colors.json      # Color/theme definitions
│   ├── iMem.json        # Simulated filesystem
│   └── commandDecl.json # Command declarations
├其他/
│   └── resursi.md       # Link to ASCII art generator
├── log.txt              # Simple log file
├── setup.py             # Installation script
└── README.md            # This file
```

## Safety Note

⚠️ MaxL runs in a **simulated filesystem**. All edits, creations, and deletions only affect the `iMem.json` file in the `json/` directory. Your actual operating system files remain completely unchanged and safe.

## License

MIT License - see `LICENSE` file for details.

## Contributing

Feel free to open issues or submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

i hate writing so heres what AI said to put. :)
