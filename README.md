# Python-Project-Template
A template for python project.

## 1. Get inside codespace
Create a new codespace for this project.

## 2. Create virtual environment
- In the terminal type `python -m venv .venv`  
- get inside the virtual environment `source .venv/bin/activate`

## 3. Write Code
Write the developmet code whatver is the project about.

## 4. Create three important files for any python project:
- requirements.txt
- Makefile
- tests

## 5. Add testing code
Write the testing code.

## 6. Add all the required packages into requirements file
Add some important packages:
- pytest
- pytest-cov
- black
- pylint 
- ipython

## 7. Add all the required steps in Makefile
Add the code to automate the process of installing packages to testing and linting

## 8. Run Makefile and Debug and adjust code
- To install packages and update pip: `make install`
- To test and check coverage: `make test`
- To format and lint the codes: `make refactor`
- To implement all of the above: `make all`

## 9. Push code to repository
- Check which files are staged: `git status`
- Add files to staging area: `git add *` for adding all the unstaged files or for selective files `git add <file_name>`
- Commit the files with a message: `git commit -m "<message>"`
- Push files to repository: `git push`

## 10. Add Continus Integration pipeline using Github Actions
To create an automated pipeline which would trigger with every push and pull of code.


[![CI Pipeline](https://github.com/0Mr-Panda0/Python-Project-Template/actions/workflows/main.yml/badge.svg)](https://github.com/0Mr-Panda0/Python-Project-Template/actions/workflows/main.yml)