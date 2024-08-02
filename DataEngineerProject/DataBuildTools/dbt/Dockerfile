FROM getdbt/dbt:latest

WORKDIR /dbt

# Installer le package DBT pour Athena
RUN pip install dbt-athena-adapter

COPY . /dbt

ENTRYPOINT ["dbt"]
CMD ["run"]

