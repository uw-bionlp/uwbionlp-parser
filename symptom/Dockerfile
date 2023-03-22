# docker build -t sdoh-predictor -f $PWD/sdoh/Dockerfile $PWD/sdoh
# docker run --name=sdoh-predictor_1 -p 42450:8080 sdoh-predictor

FROM python:3.7 as build

WORKDIR /usr/src/app

# Copy code
COPY main.py process.py requirements.txt /usr/src/app/
COPY proto /usr/src/app/proto
COPY spert /usr/src/app/spert

# Copy model
COPY model /usr/src/app/model

# user
RUN chmod 777 -R /usr/src/app

# pip install
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir --user -r requirements.txt  && \
    python3 -m spacy download en_core_web_sm

CMD [ "python", "./main.py" ]