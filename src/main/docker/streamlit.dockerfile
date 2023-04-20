FROM python:3.8
#https://medium.com/@DahlitzF/run-python-applications-as-non-root-user-in-docker-containers-by-example-cba46a0ff384

RUN pip3 install --upgrade pip

RUN adduser worker
WORKDIR /home/worker

RUN chown worker:worker /home/worker/ -R

ENV PATH="/home/worker/.local/bin:${PATH}"

USER worker

COPY ./src/main/python/requeriments.txt /home/worker/

RUN pip3 install --user -r /home/worker/requeriments.txt

COPY --chown=worker ./src/main/python/datagencars/ /home/worker/datagencars/
COPY --chown=worker ./src/main/python/streamlit/ /home/worker/streamlit/
#RUN mkdir -p /home/worker/.streamlit/
COPY ./src/main/python/streamlit/config.toml  /home/worker/.streamlit/

CMD ["streamlit","run","app.py"]
