#!/usr/bin/env bash
cd ./government_up_yet/
docker build -t registry.gitlab.com/cachednerds/government_up_yet:backend .
docker push registry.gitlab.com/cachednerds/government_up_yet:backend
cd ../frontend/
docker build -f Dockerfile.prod -t registry.gitlab.com/cachednerds/government_up_yet:frontend .
docker push registry.gitlab.com/cachednerds/government_up_yet:frontend
