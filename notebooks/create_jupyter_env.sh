#!/bin/bash
echo "This script will install a new virtual environment for Jupyter in the directory '$(pwd)'. Do you want to continue? ([Y]/n)"
read answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  echo "Exiting..."
  exit 1
fi

if [ -d "jupyter-env" ]; then
  echo "The virtual environment already exists. Do you want to delete it and create a new one? (y/[N])"
  read answer
  if [[ "$answer" =~ ^[Yy]$ ]]; then
    echo "Deleting the existing virtual environment..."
    rm -rf jupyter-env
  else
    echo "Exiting..."
    exit 1
  fi
fi

echo "Creating a new virtual environment for Jupyter..."
python3 -m venv jupyter-env
source jupyter-env/bin/activate

echo "Installing Jupyter..."
pip3 install jupyter > /dev/null

echo "Installing the IPython kernel..."
python3 -m ipykernel install --user --name=jupyter-env --display-name="Python3 (jupyter-env)" > /dev/null

echo "Refreshing the Jupyter kernel list..."
jupyter kernelspec list

deactivate
echo "Environment created! Run 'source jupyter-env/bin/activate' to activate it."