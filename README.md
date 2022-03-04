# DeepAgri Project
Authors: [Pierre Cera-Huelva](https://github.com/PierreCeraH), [Wenfang Zhou](https://github.com/WenfangZh), [Constantin Talandier](https://github.com/Constantier), [Gaspar Dupas](https://github.com/Gaspar97)

## Project Description
Project in the context of a Paris LeWagon Data Science project (FT #802).

The aim of the project is to predict the production of soft wheat (used for bread) in Metropolitan France. The model will be aimed at predicting production at the mid-year harvest in early July based on data available at the start of March of the same year.

- Data Source:
- Type of analysis:

Please document the project the best you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for deepagri in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/deepagri`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "deepagri"
git remote add origin git@github.com:{group}/deepagri.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
deepagri-run
```

# Install

Go to `https://github.com/{group}/deepagri` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/deepagri.git
cd deepagri
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
deepagri-run
```
