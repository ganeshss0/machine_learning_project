# Start Machine Learning Project

### Software and Account Requirements.

1. [GitHub Account]
2. [Azure Account]
3. [Visual Studio Code]
4. [Git CLI]

Create environment
```
conda create -p venv python==3.7 -y
```
```
conda active venv/
```
OR
```
conda activate venv
```
```
pip install -r requirements.txt
```
To add files to git
```
git add.
```
OR 
```
git add <file_name>
```

To ignore file or folder from git we can write name of file/folder in `.gitignore` file.
To check the git status
```
git status
```
To check all version maintained by git
```
git log
```
To create version/commit all changes by git
```
git commit -m "message"
```
To send version/changes to github
```
git push origin main
```

Build Docker Image
```
docker build -t <image_name>:<tagname> .
```
> Note: Image name for docker must be lowercase.

To list docker image
```
docker images
```
Run docker images
```
docker run -p 5000:5000 -e PORT:5000 <Image ID>
```