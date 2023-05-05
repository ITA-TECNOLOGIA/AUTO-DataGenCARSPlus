FROM continuumio/miniconda3
#https://pythonspeed.com/articles/activate-conda-dockerfile/#working

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install gcc -y

# Create the environment:
COPY src/main/python/environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "CARS", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
#RUN echo "Make sure flask is installed:"
#RUN python -c "import flask"

# The code to run when container is started:
COPY ./src/main/python/datagencars/ ./datagencars/
COPY ./resources/ ./resources/
COPY ./src/main/python/streamlit_app/ ./streamlit_app/
COPY ./src/main/python/streamlit_app/config.toml  ./.streamlit/

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "CARS", "streamlit","run","./streamlit_app/app.py"]