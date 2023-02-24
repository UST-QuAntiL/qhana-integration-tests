FROM python:3.11

ADD . /app
WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install

# install proxy
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/install_proxy.sh install_proxy.sh
RUN chmod +x install_proxy.sh && ./install_proxy.sh

# add localhost proxy files
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/Caddyfile.template Caddyfile.template
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/start_proxy.sh start_proxy.sh
RUN chmod +x start_proxy.sh

CMD ./start_proxy.sh && poetry run
