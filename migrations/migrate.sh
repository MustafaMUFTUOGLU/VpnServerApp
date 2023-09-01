mkdir -p migrations/versions
#alembic downgrade -1
REVISION=$(alembic current | awk '{print $7}')
REV=$(echo $REVISION | sed "s/'//g")
if [ -z "$REVISION" ]
then
   echo "migrate starting"
else
  alembic revision --rev-id "$REV"
fi
alembic downgrade -1
alembic upgrade head
alembic revision --autogenerate -m "$(date +%F)"
alembic -x data=true upgrade head
#alembic upgrade head
