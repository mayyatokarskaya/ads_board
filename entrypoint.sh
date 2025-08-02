set -e
echo "Waiting for PostgreSQL..."
while ! nc -z $HOST $PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"