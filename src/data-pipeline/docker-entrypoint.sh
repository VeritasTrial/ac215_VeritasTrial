# Docker entrypoint script

if [ "$#" -gt 0 ]; then
  pipenv run "$@"
else
  pipenv shell
fi
