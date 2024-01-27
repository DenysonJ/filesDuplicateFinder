# filesDuplicateFinder

[![Codecov](https://codecov.io/gh/DenysonJ/filesDuplicateFinder/graph/badge.svg?token=2771FCYD4R)](https://codecov.io/gh/DenysonJ/filesDuplicateFinder)
![GitHub repo size](https://img.shields.io/github/repo-size/DenysonJ/filesDuplicateFinder)
![GitHub language count](https://img.shields.io/github/languages/count/DenysonJ/filesDuplicateFinder)
![GitHub forks](https://img.shields.io/github/forks/DenysonJ/filesDuplicateFinder)

<img src="imagem.png" alt="Exemplo imagem">

The objective of this project is to develop a program called "filesDuplicateFinder" that allows finding and managing duplicate files in a directory, in order to save space. The project is under development and has a list of tasks to be completed.

Se você não fala inglês, abra este [readme em pt-br](README.md).

:construction: Under construction :construction:

## 📝 Content Table

- [Adjustments and improvements](#adjustments-and-improvements)
- [Prerequisites](#prerequisites)
- [Installing filesDuplicateFinder](#installing-filesduplicatefinder)
- [Using filesDuplicateFinder](#using-filesduplicatefinder)
- [Contributing to filesDuplicateFinder](#contributing-to-filesduplicatefinder)
- [Be one of the contributors](#be-one-of-the-contributors)
- [License](#license)


### Adjustments and improvements

The project is still under development and the next updates will focus on the following tasks:

- [X] Create tests for the main functions
- [ ] Create flexibility for soft comparison on videos
- [ ] Create log system
- [ ] Improve performance
- [ ] Improve use test case coverage
- [ ] Create a GUI
- [ ] Create a installer
- [ ] Compatibility with Windows (not tested yet)
- [ ] Compatibility with macOS (not tested yet)
- [ ] Compatibility with Linux
- [ ] Create text similarity function

## 💻 Prerequisites

Before starting, make sure you have met the following requirements:

- You have installed the latest version of `anaconda` or `miniconda` 

## 🚀 Installing filesDuplicateFinder

To install filesDuplicateFinder, install the necessary dependencies:

```bash
conda env update --file env.yml
```

## ☕ Using filesDuplicateFinder

To use filesDuplicateFinder, follow these steps:

After installing the dependencies, activate the environment:

```bash
conda activate pythonUtils
```

Or:

```bash
source activate pythonUtils
```

Then run the program:

```bash
python3 duplicateFinder.py -d <caminho_do_diretorio>
```

With this command, the program will search for duplicate files in the directory informed and delete all duplicated files, keeping only one copy of each file.
The recursive search is disabled by default, to enable it, use the `-r` or `--recursive` flag. The comparison of the files is hard by default, meaning that the program will compare the files byte by byte, to use the soft comparison, use the `-t` or `--type` flag with the option 'soft'. For more information use the `-h` or `--help` flag.

An example of using the program, specifying the soft comparison, the similarity limit of 0.8, the recursive search, searching only for files with the `.mp4` extension and moving the duplicate files to the `duplicates` folder:

```bash
python3 duplicateFinder.py -d <caminho_do_diretorio> -s 0.8 -t soft -r -i mp4 -a move -o duplicates
```

## 📫 Contributing to filesDuplicateFinder

To contribute to filesDuplicateFinder, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and confirm them: `git commit -m '<commit_message>'`
4. Send to the original branch: `git push origin <project_name> / <local>`
5. Create the pull request.

You can also consult the [github documentation](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) for more information.

## 😄 Be one of the contributors

Want to buy me a coffe?

## 📝 License

This project is under license GNU GPLv3. See the [LICENSE](LICENSE.md) for more details.

[⬆ Back to the top](#filesDuplicateFinder)<br>