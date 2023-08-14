# Setting up Virtual Environment using Python 3.8

## Linux system
### 1. Install Python 3.8 (if not installed)
First, make sure Python 3.8 is installed on your system. If not, you'll need to install it. Here's a brief on how to do it:

```bash
sudo apt update
sudo apt install python3.8
```
### 2. Install venv (if not installed)
The venv module is part of the standard library for Python 3.3 and newer. If you have an older version of Python 3.8, or you don't have the venv module installed, you can install it with:
```bash
sudo apt install python3.8-venv
```

### 3. Create the Virtual Environment
Navigate to the directory where you want your virtual environment. Then, run:

```bash
python3.8 -m venv llm-agent
```
This will create a new virtual environment named llm-agent using Python 3.8.


### 4. Activate the Virtual Environment
To activate the llm-agent virtual environment:

```bash
source llm-agent/bin/activate
```
Once activated, your terminal prompt will change to show the name of the activated environment.


### 5. Install Packages from requirements.txt
If you have a requirements.txt file in the current directory (or any specified path), you can install all the packages listed in it by running:

```bash
pip install -r requirements.txt
```
### 6. Deactivate the Virtual Environment (Optional)
Once you're done with your work in the virtual environment, you can deactivate it and return to your system's global Python environment by running:

```bash
deactivate
```


## Windows system
Make sure Python 3.8 is installed and added to PATH. Then use the following commands in Command Prompt:
### 1. Create the Virtual Environment
python -m venv llm-agent

### 2. Activate the Virtual Environment
.\llm-agent\Scripts\activate

### 3. Install Packages from requirements.txt
pip install -r requirements.txt

### 4. Deactivate the Virtual Environment (Optional)
deactivate


## macOS system
First, ensure Python 3.8 is installed. You might want to use Homebrew or pyenv for managing multiple Python versions.
### 1. (Optional) Install Python 3.8 using Homebrew if not installed
brew install python@3.8

### 2. (Optional) Add Python 3.8 to your PATH if using Homebrew
echo 'export PATH="/usr/local/opt/python@3.8/bin:$PATH"' >> ~/.zshrc # or ~/.bash_profile
source ~/.zshrc # or source ~/.bash_profile

### 3. Create the Virtual Environment
python3.8 -m venv llm-agent

### 4. Activate the Virtual Environment
source llm-agent/bin/activate

### 5. Install Packages from requirements.txt
pip install -r requirements.txt

### 6. Deactivate the Virtual Environment (Optional)
deactivate
