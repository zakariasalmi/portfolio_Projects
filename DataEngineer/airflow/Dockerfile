FROM apache/airflow:2.1.0

COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    && pip install --no-cache-dir apache-airflow[postgres]==2.1.0

USER airflow

ENTRYPOINT ["/opt/airflow/scripts/entrypoint.sh"]
CMD ["webserver"]

