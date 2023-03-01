FROM seleniarm/standalone-chromium:110.0

USER root

# install proxy
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/install_proxy.sh install_proxy.sh
RUN chmod +x install_proxy.sh && ./install_proxy.sh

RUN mkdir /opt/bin/proxy
RUN chown -R 1200:1201 /opt/bin/proxy
WORKDIR /opt/bin/proxy

# add localhost proxy files
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/Caddyfile.template Caddyfile.template
ADD https://raw.githubusercontent.com/UST-QuAntiL/docker-localhost-proxy/v0.3/start_proxy.sh start_proxy.sh
RUN chown 1200:1201 start_proxy.sh
RUN chown 1200:1201 Caddyfile.template
RUN chmod +x start_proxy.sh

USER 1200:1201

CMD ./start_proxy.sh && ../entry_point.sh
