.PHONY: help install-dev install-staging install-prod upgrade-dev upgrade-staging upgrade-prod uninstall-dev uninstall-staging uninstall-prod template lint test clean

CHART_NAME := oeg
NAMESPACE_DEV := sunrise6g-dev
NAMESPACE_STAGING := sunrise6g-staging
NAMESPACE_PROD := sunrise6g

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint: ## Lint the Helm chart
	helm lint .

template: ## Render templates with default values
	helm template $(CHART_NAME) . --debug

template-dev: ## Render templates with dev values
	helm template $(CHART_NAME)-dev . -f values-dev.yaml --debug

template-staging: ## Render templates with staging values
	helm template $(CHART_NAME)-staging . -f values-staging.yaml --debug

template-prod: ## Render templates with prod values
	helm template $(CHART_NAME)-prod . -f values-prod.yaml --debug

install-dev: ## Install chart in dev environment
	helm install $(CHART_NAME)-dev . -f values-dev.yaml -n $(NAMESPACE_DEV) --create-namespace

install-staging: ## Install chart in staging environment
	helm install $(CHART_NAME)-staging . -f values-staging.yaml -n $(NAMESPACE_STAGING) --create-namespace

install-prod: ## Install chart in production environment
	helm install $(CHART_NAME)-prod . -f values-prod.yaml -n $(NAMESPACE_PROD) --create-namespace

upgrade-dev: ## Upgrade dev deployment
	helm upgrade $(CHART_NAME)-dev . -f values-dev.yaml -n $(NAMESPACE_DEV)

upgrade-staging: ## Upgrade staging deployment
	helm upgrade $(CHART_NAME)-staging . -f values-staging.yaml -n $(NAMESPACE_STAGING)

upgrade-prod: ## Upgrade production deployment
	helm upgrade $(CHART_NAME)-prod . -f values-prod.yaml -n $(NAMESPACE_PROD)

uninstall-dev: ## Uninstall dev deployment
	helm uninstall $(CHART_NAME)-dev -n $(NAMESPACE_DEV)

uninstall-staging: ## Uninstall staging deployment
	helm uninstall $(CHART_NAME)-staging -n $(NAMESPACE_STAGING)

uninstall-prod: ## Uninstall production deployment
	helm uninstall $(CHART_NAME)-prod -n $(NAMESPACE_PROD)

status-dev: ## Show status of dev deployment
	helm status $(CHART_NAME)-dev -n $(NAMESPACE_DEV)

status-staging: ## Show status of staging deployment
	helm status $(CHART_NAME)-staging -n $(NAMESPACE_STAGING)

status-prod: ## Show status of production deployment
	helm status $(CHART_NAME)-prod -n $(NAMESPACE_PROD)

test-dev: ## Test dev installation
	helm test $(CHART_NAME)-dev -n $(NAMESPACE_DEV)

dry-run-dev: ## Dry run dev installation
	helm install $(CHART_NAME)-dev . -f values-dev.yaml -n $(NAMESPACE_DEV) --dry-run --debug

dry-run-staging: ## Dry run staging installation
	helm install $(CHART_NAME)-staging . -f values-staging.yaml -n $(NAMESPACE_STAGING) --dry-run --debug

dry-run-prod: ## Dry run production installation
	helm install $(CHART_NAME)-prod . -f values-prod.yaml -n $(NAMESPACE_PROD) --dry-run --debug

package: ## Package the chart
	helm package .

clean: ## Clean packaged charts
	rm -f *.tgz

validate: lint template ## Run validation checks

pods-dev: ## Show pods in dev namespace
	kubectl get pods -n $(NAMESPACE_DEV)

pods-staging: ## Show pods in staging namespace
	kubectl get pods -n $(NAMESPACE_STAGING)

pods-prod: ## Show pods in production namespace
	kubectl get pods -n $(NAMESPACE_PROD)

logs-controller-dev: ## Show controller logs in dev
	kubectl logs -f deployment/oegcontroller -n $(NAMESPACE_DEV)

logs-mongo-dev: ## Show mongo logs in dev
	kubectl logs -f deployment/oegmongo -n $(NAMESPACE_DEV)

port-forward-dev: ## Port forward to dev service
	kubectl port-forward svc/oeg 8080:80 -n $(NAMESPACE_DEV)
