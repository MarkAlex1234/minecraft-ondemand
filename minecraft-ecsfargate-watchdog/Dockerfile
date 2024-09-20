# version 1.2.0
# docker pull doctorray/minecraft-ecsfargate-watchdog-new
# EDITED 20th SEPT 2024 - ADDS DISCORD WEBHOOK

FROM amazon/aws-cli

RUN yum install -y net-tools jq nmap-ncat && \
    yum clean all

COPY ./watchdog.sh .

ENTRYPOINT ["./watchdog.sh"]
