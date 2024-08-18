### **Data build Tools Project**


Ce projet de data engineering utilise Apache Spark, dbt (Data Build Tool), et Apache Airflow pour traiter et transformer des données. Le déploiement de l'ensemble du pipeline a été réalisé avec Docker, ce qui permet une gestion efficace des environnements et des dépendances.

# Technologies Utilisées: 

#Apache Spark : Utilisé pour le traitement distribué des données volumineuses, permettant des transformations rapides et efficaces sur de grands ensembles de données.
#dbt (Data Build Tool) : Employé pour transformer les données, en utilisant SQL, et pour gérer les transformations de données de manière modulaire et maintenable.
#Apache Airflow : Utilisé pour l'orchestration des tâches, permettant d'automatiser et de planifier les différentes étapes du pipeline de données.
#Docker : Permet le déploiement facile et la gestion des environnements, assurant que le pipeline fonctionne de manière cohérente sur différentes machines et environnements.
Dans ce projet j'ai travaillé la technique d'ETL(Extract, transform, load) 

## Flux de Travail:

# Extraction des Données :

Les données brutes sont extraites de plusieurs sources (par exemple, bases de données, fichiers CSV) et stockées dans un data lake.

# Transformation avec Apache Spark :

Spark est utilisé pour nettoyer et transformer les données brutes, en les préparant pour les étapes suivantes.
Les transformations incluent l'agrégation, le filtrage, et la jointure de grandes tables de données.

# Transformation avec dbt :

dbt prend les données transformées par Spark et applique des modèles SQL pour effectuer des transformations supplémentaires.
dbt gère la création de vues et de tables dans l'entrepôt de données.

# Orchestration avec Apache Airflow :

Airflow orchestre l'ensemble du pipeline de données, en automatisant les étapes d'extraction, de transformation, et de chargement (ETL).
Des DAGs (Directed Acyclic Graphs) sont utilisés pour planifier et surveiller les tâches.

#Déploiement avec Docker :

Tous les composants (Spark, dbt, Airflow) sont déployés dans des conteneurs Docker, assurant une isolation et une portabilité entre les environnements de développement, de test, et de production.
