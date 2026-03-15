# mini-rage-app

## clone repo 
```bash
git clone https://github.com/youssefBedeer/mini-rage-app.git mini-rag-app
```

## Create conda environment
```bash
conda create -n mini-rag-app python=3.8
conda activate mini-rag-app
```
install wsl to run linux on our window system<br>
run power shell as administrator
```bash
wsl --install 
wsl --set-default-version 2
wsl --install Ubuntu
```
open Ubuntu 
```bash
sudo apt update
cd "/mnt/{put path here}/"
code .
```
download mini conda on ubuntu 
```bash
cd ~
mkdir -p ~/miniconda3

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

cd ~/miniconda3
bash miniconda.sh
bash ~/.profile
```
create conda env in ubuntu 
```bash
conda create -n mini-rag-app python=3.8
```
open new ubuntu CLI (on working dir)
```bash
conda info --envs
conda activate {the env-dir we have created}
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
pip install -r requirements.txt
```

### Setup the environment variables

```bash
cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run the FastAPI server 
```bash 
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## command to clean docker 
```bash
# stop all containers
sudo docker stop ${sudo docker ps -aq}
# remove all stopped containers 
sudo docker rm ${sudo docker ps -aq}
# remove all images 
sudo docker rmi ${sudo docker ps -q}
# remove all volumes
sudo docker volume rm ${sudo docker volume ls -q}
# clean everything remaining
sudo docker system prune -all
```