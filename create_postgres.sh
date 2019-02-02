docker run --name test_postgres --mount source=postgres_volume,target=/var/lib/postgresql/data -e POSTGRES_PASSWORD=pw -e POSTGRES_DB=paragraph_generator -d postgres:11.1 
