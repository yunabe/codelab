# MyDemoCli Project

This is a demo .NET Core C# project that includes a library, two CLI programs that use the library, and unit tests.

## Directory Structure

```
MyDemoCli/
├── src/
│   ├── MyLibrary/
│   │   ├── MyLibrary.csproj
│   │   └── ... (library source files)
│   ├── CliApp1/
│   │   ├── CliApp1.csproj
│   │   └── ... (CLI app 1 source files)
│   └── CliApp2/
│       ├── CliApp2.csproj
│       └── ... (CLI app 2 source files)
├── tests/
│   ├── MyLibrary.Tests/
│   │   ├── MyLibrary.Tests.csproj
│   │   └── ... (unit test files)
├── docs/
│   ├── ChatHistory.md
└── README.md
```

## Projects

- **MyLibrary**: A class library containing shared code.
- **CliApp1**: A CLI application that uses `MyLibrary`.
- **CliApp2**: Another CLI application that uses `MyLibrary`.
- **MyLibrary.Tests**: Unit tests for `MyLibrary`.

## Building and Running

To build and run the projects, navigate to the respective directories and use the `dotnet` CLI commands.

### Build

```sh
dotnet build
```

### Run CLI Applications

```sh
dotnet run --project src/CliApp1
dotnet run --project src/CliApp2
```

### Run Tests

```sh
dotnet test
```

## Documentation

- **ChatHistory.md**: A markdown file to record chat history with GitHub Copilot.
