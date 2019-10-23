FROM gladiatr72/just-tini:latest as tini

FROM revolutionsystems/python:3.6.9-wee-optimized-lto

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE TRUE
ENV TINI_VERSION v0.16.1

RUN mkdir -p /code/; apt-get update && apt -y upgrade; \
    apt-get -y install netcat-openbsd curl git \
    && apt-get remove -y $( dpkg -l | cut -d" " -f3 | egrep '^(x11|tk|libice|gtk|imagemag|mysql|curl)' ) \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/* /usr/share/man /usr/local/share/man /tmp/*\
    && mkdir -p $HOME/.ipython/profile_default

COPY --from=tini /tini /tini

ADD ./requirements.txt /code/

RUN    apt-get update &&\
    apt-get install -y gcc \
    && pip install --upgrade pip ipython ipdb\
    && pip install -r /code/requirements.txt \
    && apt-get -y remove gcc; apt-get -y autoremove \
    && rm -rf $HOME/.cache /var/lib/apt/lists/* /usr/share/man /usr/local/share/man \
    && find /usr -type f -name "*.pyc" -exec rm -f {} +

ADD . /code/

WORKDIR /code

ENV PYTHONPATH /code:$PYTHONPATH

EXPOSE 8080

ENTRYPOINT ["/tini", "--"]

CMD /code/manage.py run_modelservice --loglevel=debug

LABEL Description="Image for simpl-blackjack-model" Vendor="Wharton" Version="2.2.69"
