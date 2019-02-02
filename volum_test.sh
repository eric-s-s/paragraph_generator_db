name=test_volume
postgres_name=postgres_volume


docker volume create "${name}"

docker volume inspect "${name}"


docker volume create "${postgres_name}"

docker volume inspect "${postgres_name}"

