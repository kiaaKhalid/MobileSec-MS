.PHONY: help build up down logs test clean status health ps pull

help: ## Affiche l'aide
	@echo "MobileSec-MS - Commandes disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build tous les services Docker
	docker-compose build

up: ## Démarre tous les services
	docker-compose up -d
	@echo "✅ Services démarrés!"
	@echo "📊 Vérification de l'état..."
	@sleep 5
	@make status

down: ## Arrête tous les services
	docker-compose down

stop: ## Arrête sans supprimer les containers
	docker-compose stop

start: ## Démarre les containers existants
	docker-compose start

restart: ## Redémarre tous les services
	docker-compose restart

ps: ## Affiche l'état des containers
	@docker-compose ps

pull: ## Met à jour les images Docker
	docker-compose pull

logs: ## Affiche les logs de tous les services
	docker-compose logs -f

logs-apk: ## Logs APKScanner
	docker-compose logs -f apkscanner

logs-secret: ## Logs SecretHunter
	docker-compose logs -f secrethunter

logs-crypto: ## Logs CryptoCheck
	docker-compose logs -f cryptocheck

logs-network: ## Logs NetworkInspector
	docker-compose logs -f networkinspector

logs-report: ## Logs ReportGen
	docker-compose logs -f reportgen

logs-fix: ## Logs FixSuggest
	docker-compose logs -f fixsuggest

logs-ci: ## Logs CIConnector
	docker-compose logs -f ciconnector

logs-frontend: ## Logs Frontend
	docker-compose logs -f frontend

status: ## Affiche le statut des services
	@echo "🔍 État des services:"
	@docker-compose ps

health: ## Vérifie la santé de tous les services
	@echo "🏥 Health check..."
	@curl -s http://localhost:8001/health | jq -r '"✅ APKScanner: " + .status' || echo "❌ APKScanner: DOWN"
	@curl -s http://localhost:8002/health | jq -r '"✅ SecretHunter: " + .status' || echo "❌ SecretHunter: DOWN"
	@curl -s http://localhost:8003/health | jq -r '"✅ CryptoCheck: " + .status' || echo "❌ CryptoCheck: DOWN"
	@curl -s http://localhost:8004/health | jq -r '"✅ NetworkInspector: " + .status' || echo "❌ NetworkInspector: DOWN"
	@curl -s http://localhost:8005/health | jq -r '"✅ ReportGen: " + .status' || echo "❌ ReportGen: DOWN"
	@curl -s http://localhost:8006/health | jq -r '"✅ FixSuggest: " + .status' || echo "❌ FixSuggest: DOWN"
	@curl -s http://localhost:8007/health | jq -r '"✅ CIConnector: " + .status' || echo "❌ CIConnector: DOWN"

test: ## Lance un test d'intégration complet
	@echo "🧪 Test d'intégration..."
	@bash tests/integration-test.sh

clean: ## Nettoie les volumes et containers
	docker-compose down -v
	@echo "🧹 Nettoyage terminé"

rebuild: clean build up ## Rebuild complet depuis zéro

scan-example: ## Scanne un APK d'exemple
	@echo "📱 Scan d'un APK d'exemple..."
	@if [ -f examples/apks/test.apk ]; then \
		curl -X POST -F "file=@examples/apks/test.apk" http://localhost:8001/scan | jq '.'; \
	else \
		echo "❌ Aucun APK trouvé dans examples/apks/"; \
	fi

ci-github: ## Génère un workflow GitHub Actions
	curl http://localhost:8007/github-action > .github/workflows/security.yml
	@echo "✅ Workflow GitHub Actions créé: .github/workflows/security.yml"

ci-gitlab: ## Génère une config GitLab CI
	curl http://localhost:8007/gitlab-ci > .gitlab-ci.yml
	@echo "✅ Config GitLab CI créée: .gitlab-ci.yml"

install: ## Installation complète (build + up + health)
	@echo "🚀 Installation de MobileSec-MS..."
	@make build
	@make up
	@sleep 10
	@make health
	@echo ""
	@echo "✅ Installation terminée!"
	@echo "📚 Documentation: http://localhost:8080"
	@echo "🔍 Commandes disponibles: make help"
