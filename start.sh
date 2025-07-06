if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
