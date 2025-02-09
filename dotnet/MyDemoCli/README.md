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

## Adding a New Library and Unit Tests

To add a new library and its unit tests to the project, follow these steps:

1. Create a new library project:

```sh
dotnet new classlib -o src/NewLibrary
```

2. Add the new library project to the solution:

```sh
dotnet sln add src/NewLibrary/NewLibrary.csproj
```

3. Create a new unit test project:

```sh
dotnet new mstest -o tests/NewLibrary.Tests
```

4. Add the new unit test project to the solution:

```sh
dotnet sln add tests/NewLibrary.Tests/NewLibrary.Tests.csproj
```

5. Add a project reference to the new library in the unit test project file (`NewLibrary.Tests.csproj`):

```xml
<ItemGroup>
  <ProjectReference Include="../../src/NewLibrary/NewLibrary.csproj" />
</ItemGroup>
```

6. Write unit tests for the new library in the `tests/NewLibrary.Tests` directory.

7. Run the tests to verify they work:

```sh
dotnet test
```

## Documentation

- **ChatHistory.md**: A markdown file to record chat history with GitHub Copilot.
