set -e

echo "Starting MongoDB Server..."
podman run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=example --name=mongo mongo:6.0
