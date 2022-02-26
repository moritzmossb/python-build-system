# Pybuild

Ever get tired of `make`? Use pybuild, a (not yet fully complete) build system where you specify your project 
in a json-document called `data.json` (an example can be found in `example.json`). To get started, either clone the 
repo or simply download the main.py. Next, add an alias to your .bashrc (or .zshrc, etc): 

```bash
alias pybuild="python /path/to/main.py"
```

and restart your terminal (or source .bashrc, .zshrc, ...). Next enter your project directory and type 
`pybuild`. If no `data.json` is found, then a setup process starts where you enter basic information.

## The JSON-Object

The root object has two children: *about* and *environment*. The *about* object is currently
without use, but I have some ideas I want to implement. The *environment* 
object is where you specify all your compile-units (like targets in make). However, 
you first need to specify your compiler by adding the `command` to the `compiler` object:

```json
{
    "compiler": {
        "command": "g++"
    }
}
```

When you complete the setup, `data.json` is created, where two `compile-types` are present:
*object* and *exec*. Object compiles a target into an object which can be used for linking, 
*exec* builds the enitre project and produces an executable. Currently using *exec* results
in all currently compiled objects being used.

### Compiler Flags
Typically pybuild differentiates between two types of flag. Global and ''local''. 
Global flags are used in all compilation processes and are specified in the 
*compiler* object. Local flags are specified by the compile type.

### Compilation Units
To add a compilation-unit (i.e. a target), you add an object to the 
*compile-units* array in *environment*. A target-object is of the following form:
```json
{
    "name": "card",
    "file": "game/card.cpp",
    "type": "object",
    "dependencies": []
}
```

Files are easily specified by starting in the set source-directory. For the given example, the 
target "card" has it's source file in `<project-root>/src/card/card.cpp`. Dependencies are 
implementation files you use in your project, e.g. when you include `card.hpp` in your 
`main.cpp`. Dependencies are added via their target name.