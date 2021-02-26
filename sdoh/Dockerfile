# docker build -t sdoh-predictor -f $PWD/sdoh/Dockerfile $PWD/sdoh
# docker run --name=sdoh-predictor_1 -p 42450:8080 sdoh-predictor

FROM python:3.7 as build

WORKDIR /usr/src/app

# Copy code
COPY main.py process.py dl_nltk_punkt.py constants.py requirements.txt /usr/src/app/
COPY proto          /usr/src/app/proto
COPY annotate       /usr/src/app/annotate
COPY corpus         /usr/src/app/corpus
COPY pytorch_models /usr/src/app/pytorch_models
COPY models         /usr/src/app/models
COPY utils          /usr/src/app/utils
COPY docker         /usr/src/app/docker

# Copy model
COPY model          /usr/src/app/model

# pip install
RUN python3 -m pip install --no-cache-dir -r requirements.txt  && \
    python3 dl_nltk_punkt.py

CMD [ "python", "./main.py" ]