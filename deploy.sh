#!/usr/bin/env bash

kubectl apply -f ./k8s/frontend.yml
kubectl apply -f ./k8s/backend.yml
kubectl apply -f ./k8s/ingress.yml