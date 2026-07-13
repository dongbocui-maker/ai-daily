# LibreCode

A free, open-source AI-powered code editor built from the ground up with .NET 10 and Avalonia UI. Runs natively on Windows, Linux, and macOS -- no Electron, no web views, just fast native rendering.

LibreCode pairs a full-featured code editor with a local AI assistant powered by [Ollama](https://ollama.com), a built-in terminal, a model marketplace, and a serious reverse engineering toolkit for both .NET assemblies and WebAssembly binaries -- including live browser debugging over Chrome DevTools Protocol.

---

## Why LibreCode?

Most AI-powered editors are either closed-source, browser-based, or tied to cloud APIs. LibreCode is different:

- **100% local AI** -- your code never leaves your machine. Runs against any Ollama model you have installed.
- **Truly cross-platform** -- native Avalonia UI, not a web wrapper. Starts fast, stays fast.
- **Built for hackers** -- ships with .NET, WASM, and ELF (.so) reversing toolkits (decompiler, IL/WAT/x86-64 disassembly, hex editor, PE/ELF inspectors, step-through debuggers, live CDP debugging, Harmony patch generation, OLLVM deobfuscation, cross-module stealth/anti-debug analysis) alongside a modern code editor.
- **No telemetry, no accounts, no subscriptions.**

---

## Features

### Code Editor

- Syntax highlighting for 25+ languages via TextMate grammars (Dark+ theme)
- Keyword autocomplete popup as you type (Python, C#, JS/TS, Go, Rust, Java, C/C++, HTML, CSS, SQL, Shell, and more)
- Smart auto-indentation -- copies previous line indent and adds a level after `{`, `:`, `(`, `[`
- Multi-tab editing with dirty-file indicators
- Line numbers, monospace font rendering, and a welcome screen when no files are open
- Ctrl+S to save

### File Explorer

- Open any project folder and browse the full directory tree
- Create new files and folders, rename, delete
- Right-click context menu with "Run in Terminal" option
- File watcher automatically refreshes the tree when files change on disk

### AI Assistant

Four interaction modes, all powered by your local Ollama instance:

- **Ask** -- get answers to coding questions with context from your codebase
- **Agent** -- autonomous coding agent that can read files, write files, search your project, and run shell commands in a loop until the task is done
- **Plan** -- have the AI plan out an implementation approach before writing code
- **Debug** -- paste errors and get debugging help

The AI automatically pulls in relevant code context using codebase embeddings (RAG). It indexes your project files, chunks them, generates embeddings via Ollama, and uses cosine similarity search to inject the most relevant snippets into every conversation.

Custom rules let you set persistent instructions that the AI always follows (e.g., "always use TypeScript", "prefer functional style").

### Built-in Terminal

- Integrated terminal panel (toggle with Ctrl+`)
- Auto-detects PowerShell (pwsh or powershell.exe) on Windows with PSReadLine tab completion
- Opens in your project directory by default
- Resizable with a drag splitter

### Model Marketplace

- Browse the full Ollama model library without leaving the editor
- Search models by name
- See model descriptions, parameter counts, variant tags, and estimated VRAM requirements
- GPU detection shows your available VRAM so you know what will fit

### Reverse Engineering Toolkit

The Reverse tab is split into three formats -- **.NET**, **WASM**, and **ELF** -- each with their own file picker and sub-tabs. You flip between them with a single click.

#### .NET Reversing

Powered by the same decompilation engine as ILSpy/dnSpy:

- **C# Decompiler** -- load any .dll or .exe and browse the full decompiled source. Navigate by namespace and class, click to decompile individual types.
- **IL Disassembler** -- raw IL bytecode for the entire module or per-type.
- **PE Inspector** -- PE headers, sections, CLR metadata, assembly references, the works.
- **String Search** -- scan the user strings heap for hardcoded strings, URLs, keys, credentials. Real-time filtering.
- **Hex Viewer** -- page through raw bytes with offset, hex, and ASCII columns. Jump to any offset.
- **IL Debugger** -- step through .NET IL instructions one at a time. Pick a method, set breakpoints, and watch the evaluation stack and local variables change as you step. It simulates the CLR execution engine so you can understand exactly what a method does at the bytecode level without actually running it.
- **Harmony Patch Generator** -- pick any method from the type/method tree and instantly get a ready-to-compile [HarmonyLib](https://github.com/pardeike/Harmony) patch class. Emits `[HarmonyPatch]` with the correct `typeof`/argument-type matching, and prefix/postfix/transpiler/finalizer stubs wired up with the right injected parameters (`__instance`, `__result`, by-ref args) for that exact signature — toggle which patch methods you want and copy it straight into your patch assembly.
- **AI Analysis** -- send decompiled code to the AI for vulnerability analysis, obfuscation detection, anti-debugging pattern recognition, and control flow review.

#### WASM Reversing

A zero-dependency WebAssembly binary analysis toolkit built from scratch:

- **WAT Disassembly** -- full disassembly of every function in WebAssembly Text format. Browse functions in a tree, click to see the instruction listing.
- **Module Info** -- high-level overview of the binary: version, function/import/export/global/table/memory/data segment counts, section layout.
- **Imports & Exports** -- split-pane view of everything the module imports and exports, with kind and type info.
- **String Search** -- extract strings from WASM data segments with offset and segment index.
- **Hex Viewer** -- same hex/ASCII pager as the .NET side, but for .wasm files.
- **WASM Debugger** -- step-through interpreter for WASM bytecode. Select a function, set breakpoints on instruction indices, and single-step through execution. Watch the operand stack grow and shrink, inspect local variables, and see output in real time. Covers ~200 opcodes.
- **CDP Live Debugger** -- connect to a real browser instance over Chrome DevTools Protocol and debug WASM running in the wild. Discover targets, attach to a tab, pause/resume/step over/step into/step out, set breakpoints on WASM scripts by line and column, evaluate expressions in the paused frame context, inspect scope variables and the call stack, read WASM linear memory, and watch console output -- all from inside LibreCode. Just launch Chrome or Edge with `--remote-debugging-port=9222` and hit Discover.
- **AI Analysis** -- send disassembled WASM functions to the AI for the same deep analysis you get on the .NET side.

#### ELF / .so Reversing

Native shared object analysis for Linux and Android libraries:

- **Disassembly** -- browse function symbols (filterable), click to disassemble. x86 and x86-64 code is fully disassembled via Iced; other architectures (ARM, AArch64, RISC-V, ...) show an annotated hex dump of the function bytes. Stripped binaries fall back to whole-section disassembly.
- **Module Info** -- ELF header (class, endianness, OS/ABI, machine, type, entry point), dynamic linking info (SONAME, interpreter, RunPath, needed libraries), symbol statistics, full section and program header tables.
- **Symbols** -- split-pane view of the dynamic symbol interface: imports (undefined symbols) on top, exports (defined global/weak symbols) with address, size, type, and section below.
- **String Search** -- extract printable strings from all sections with offset and section name. Works even on binaries with stripped section tables.
- **Hex Viewer** -- same hex/ASCII pager as the other formats, but for .so/.elf files.
- **OLLVM Deobfuscation** -- scan an x86/x86-64 function for [Obfuscator-LLVM](https://github.com/obfuscator-llvm/obfuscator) artifacts. Builds a basic-block control-flow graph and detects the three classic passes: **control-flow flattening** (locates the dispatcher block and the state variable cycling through its constants), **bogus control flow / opaque predicates** (recurring global reads and `x*(x±1)` evenness tests whose branches have a dead edge), and **instruction substitution** (subtraction-as-add-of-negation, xor/add expansion templates). Produces a findings report plus an annotated disassembly that marks each artifact inline. Static, pattern-based: it flags and explains the obfuscation so you can read past it, rather than rewriting the binary.
- **AI Analysis** -- sends the module summary (header, imports/exports, needed libraries, notable .rodata strings) plus the current disassembly to the AI for purpose identification, vulnerability analysis, and anti-analysis pattern detection.

#### Stealth / Anti-Debug (every format)

A **Stealth** tab on all three formats -- .NET, WASM, and ELF -- scans the loaded module for the anti-debugging and anti-analysis techniques a debugger has to evade to stay invisible, ranks them by severity, and generates the evasion for each:

- **.NET** -- scans decoded IL for debugger-detection APIs (`Debugger.IsAttached`, `IsDebuggerPresent`, `CheckRemoteDebuggerPresent`, `NtQueryInformationProcess`), debugger process-name scans, timing checks, profiler env-var probes, and embedded tool-name/`/proc` strings. The Evasion tab generates a ready-to-apply Harmony patch that forces the managed `Debugger.*` checks to report "not attached", and lists the native checks that need an unmanaged detour.
- **ELF** -- flags `ptrace(PTRACE_TRACEME)`, `prctl`/`personality` anti-attach, SIGTRAP handlers, `/proc/self/status` `TracerPid` reads, `LD_PRELOAD` checks, embedded analysis-tool names (Frida, gdbserver, Magisk...), and -- on x86/x86-64 -- inline `rdtsc` timing and raw ptrace syscalls in `.text`. Produces a per-technique evasion playbook (preload shims, forged procfs, branch patches).
- **WASM** -- flags host-side timing imports and DevTools/debugger strings, with guidance for spoofing them in the JS host.

Because LibreCode's IL and WASM "debuggers" are interpreters, they never attach a real debugger or set `Debugger.IsAttached` -- so they're invisible to in-process checks by construction. The Stealth tab shows what an *external* debugger would have to defeat, and hands you the bypass.

### Session Persistence

LibreCode remembers your state between launches:

- Open tabs and active file
- Project folder
- Right panel selection
- Chat history

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+S | Save current file |
| Ctrl+` | Toggle terminal |
| Ctrl+Shift+P | Command palette |
| Tab / Enter | Accept autocomplete suggestion |
| Escape | Dismiss autocomplete |

---

## Getting Started

### Prerequisites

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- [Ollama](https://ollama.com) installed and running locally (for AI features)

### Build & Run

```bash
git clone https://github.com/re4/LibreCode.git
cd LibreCode/LibreCode
dotnet run
```

### Install a Model

The AI features need at least one Ollama model. Open a terminal and run:

```bash
ollama pull llama3.2
```

Or browse models from the **Models** tab inside LibreCode.

### Configuration

Edit `appsettings.json` to customize:

```json
{
  "Ollama": {
    "BaseUrl": "http://127.0.0.1:11434",
    "DefaultModel": "llama3.2",
    "EmbeddingModel": "nomic-embed-text",
    "Temperature": 0.7,
    "MaxTokens": 4096,
    "AutocompleteEnabled": true,
    "AutocompleteDebounceMs": 300
  }
}
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | Avalonia UI 11.3 (cross-platform native) |
| Code Editor | AvaloniaEdit + TextMate grammars |
| Terminal | Iciclecreek.Avalonia.Terminal (XTerm.NET + Porta.Pty) |
| AI Backend | Ollama (local LLM inference) |
| .NET Decompiler | ICSharpCode.Decompiler (ILSpy engine) |
| PE Analysis | System.Reflection.Metadata |
| Harmony Patches | HarmonyLib-targeted source generation from the decompiler type system |
| WASM Analysis | Custom zero-dependency binary parser + interpreter |
| ELF Analysis | Custom zero-dependency ELF parser + Iced (x86/x86-64 disassembly) |
| OLLVM Deobfuscation | Iced-based CFG builder + heuristic flattening/opaque-predicate/substitution detectors |
| Stealth / Anti-Debug | Per-format scanners (IL / imports+strings / Iced .text) + Harmony bypass generation |
| CDP Debugging | Chrome DevTools Protocol over WebSocket (System.Net.WebSockets) |
| Architecture | MVVM with CommunityToolkit.Mvvm |
| DI | Microsoft.Extensions.DependencyInjection |
| Target | .NET 10, Windows / Linux / macOS |

---

## Project Structure

```
LibreCode/
  Features/
    AI/              # AI message models and mode definitions
    Agent/           # Autonomous coding agent + tool implementations
      Tools/         # File read/write, search, shell execution
    Autocomplete/    # Editor keyword completion + data models
    Chat/            # Chat service with RAG context injection
    Context/         # Codebase indexer + embedding store
    InlineEdit/      # Inline code editing via AI
    Marketplace/     # Ollama model browser, GPU detection
    Reversing/       # .NET + WASM + ELF analysis services, IL/WASM debuggers, CDP client
                     # Harmony patch generator, OLLVM deobfuscator, stealth anti-debug scanners
  Services/
    FileSystem/      # Project-scoped file I/O with watcher
    Ollama/          # Ollama HTTP client + request/response models
    SessionPersistenceService.cs
    RulesService.cs
  ViewModels/
    MainViewModel.cs # Central application state
  Views/
    EditorView       # Code editor with tabs
    FileExplorerView # Project tree browser
    AiPanelView      # AI chat interface
    MarketplaceView  # Model browser
    SettingsView     # Rules and config
    TerminalView     # Integrated terminal
    ReversingView    # Reverse engineering panel (.NET / WASM / ELF format switcher)
    Reversing/       # .NET sub-views (Decompile, IL, PE, Strings, Hex, IL Debug, Harmony, Stealth, AI)
                     # WASM sub-views (Disassembly, Info, Imports/Exports, Strings, Hex, Debug, CDP, Stealth, AI)
                     # ELF sub-views (Disassembly, Info, Symbols, Strings, Hex, Deobf, Stealth, AI)
                     # StealthSubView is shared across all three (Module property selects the scanner)
```

---

## Contributing

Contributions are welcome -- open an issue first to discuss what you'd like to change before submitting a PR.

By submitting a pull request, you agree to the [Contributor License Agreement](CLA.md). In short:

- You assign all rights in your contribution to the project owner.
- You confirm the work is original and doesn't infringe on third-party rights.
- The project owner is not obligated to accept any contribution.

Please read the full [CLA.md](CLA.md) before contributing.

---

## License

LibreCode is released under a **Custom License (Contribution-Only, No Resale, No Fork Distribution)**. See [LICENSE.md](LICENSE.md) for the full text.

The key points:

- **You can use it** -- for personal or commercial business purposes.
- **You cannot redistribute it** -- no copying, selling, sublicensing, or making it available to third parties.
- **You cannot fork and distribute** -- forks are only permitted for the purpose of contributing back to the original repo via pull requests.
- **You cannot offer it as a service** -- no SaaS, hosted, or competing offerings built on this software.
- **All contributions become the property of the original author.**

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


# Showcase

<img width="1393" height="919" alt="Screenshot 2026-04-09 231703" src="https://github.com/user-attachments/assets/6c82c77b-e051-42dc-bb78-a1771c1dc490" />
<img width="1386" height="917" alt="Screenshot 2026-04-09 231648" src="https://github.com/user-attachments/assets/99ff2358-1b9f-4f43-b2e7-f17ffd237085" />
<img width="1392" height="919" alt="Screenshot 2026-04-09 231657" src="https://github.com/user-attachments/assets/8b99dfc6-d844-4b1a-b5e5-88cd73e60c69" />
<img width="1394" height="922" alt="Screenshot 2026-04-09 231638" src="https://github.com/user-attachments/assets/ebd970fe-4a2f-44c6-b509-056c49bff000" />

