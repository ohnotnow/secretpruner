# Docker Swarm Secret Pruner

This is a little python script which will loop over docker secrets looking for names that match a pattern, then remove the oldest ones up to a given limit.
__Note__: The script needs access to the docker socket, so make sure to scan through the code to make sure you trust it.

The script is pretty specific to our way of naming secrets, but hopefully it might give you an idea of how to prune your own ones.

## Details

Every time we deploy to swarm we generate a new secret with the environment variables needed by the app.  This is the format we use for our dotenv files, so that's the default in the script :
```
stackname-prod-dotenv-2020-03-20-14-50-33
```
After a while we end up with a lot of old secrets and it gets a bit messy debugging/listing them - so this script will break the secret name up and the date it was last updated.  Then if there are more than a certain number of them - it will prune the oldest until it hits the limit (defined as 'keep' in the script).


## Usage

First off, build the image that will run the script :
```bash
docker build -t secretpruner:some-tag .
```

And on a swarm master run the image :
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock secretpruner:some-tag
```
It will print out the names of any secrets it removed.  You can also run it in as a dry run by setting a PRUNE_DRY_RUN=1 environment variable, eg :
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e PRUNE_DRY_RUN=1 secretpruner:some-tag
```

## Exit codes

The script will exit with 0 if there were no issues found, 1 if something went wrong.
