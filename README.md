# ClientHub - Projet CI/CD Industriel

Ce dépôt contient l'application web conteneurisée (API Flask, Nginx, MySQL) ainsi que le pipeline d'intégration et de déploiement continus (CI/CD) entièrement automatisé via GitHub Actions.

---

## Fonctionnement du Pipeline CI/CD

Le pipeline est défini dans le fichier `.github/workflows/ci-cd.yml` et se déclenche automatiquement à chaque `git push` sur la branche `main`. Il s'articule en 4 jobs séquentiels :

1. **Tests Unitaires (`unit-tests`)** :
   * Configure l'environnement Python.
   * Installe les dépendances depuis `requirements.txt`.
   * Exécute les tests unitaires via `pytest`.

2. **Tests End-to-End (`e2e-tests`)** :
   * Démarre l'infrastructure complète via `docker compose up --build -d`.
   * Vérifie la disponibilité de l'API (`/health`) et valide les fonctionnalités métier (`/clients`).
   * Nettoie les conteneurs à la fin.

3. **Build & Push Docker Hub (`build-and-push`)** :
   * S'exécute **uniquement** si les tests unitaires et E2E ont réussi.
   * Se connecte à Docker Hub de manière sécurisée via les secrets.
   * Construit l'image Docker de l'API et la pousse sur le registre avec le tag `latest`.

4. **Déploiement sur VM Azure (`deploy`)** :
   * Se connecte à la machine virtuelle Azure distante via SSH.
   * Récupère ou met à jour le code source et le fichier `docker-compose.yml` (`git clone`/`git pull`).
   * Télécharge la dernière image depuis Docker Hub (`docker compose pull`).
   * Redémarre l'application de manière **idempotente** (`docker compose up -d --force-recreate --remove-orphans`).
   * Vérifie que l'application répond correctement sur l'IP publique et le port assigné.

---

## Choix Techniques

* **Docker & Docker Compose** : Isolation des services (Nginx, API Flask, MySQL) pour garantir la portabilité et s'assurer que l'environnement de production est strictement identique à l'environnement local.
* **Pytest & Requests** : Utilisation de `pytest` pour unifier l'exécution des tests unitaires et E2E sous une commande unique (`pytest`), garantissant l'échec du pipeline au moindre problème.
* **Idempotence** : Utilisation des flags `--force-recreate` et `--remove-orphans` lors du déploiement pour éviter l'accumulation de conteneurs obsolètes et garantir un redémarrage propre sans casser le service existant.
* **Sécurité (GitHub Secrets)** : Aucun identifiant, mot de passe ou clé d'accès n'est stocké en clair dans le code source. Tout passe par les secrets chiffrés du dépôt GitHub (`DOCKER_USERNAME`, `DOCKER_PASSWORD`, `AZURE_VM_HOST`, `AZURE_VM_USER`, `AZURE_VM_PASSWORD`).

---

## Accès à l'application

L'application est déployée sur la machine virtuelle Azure et accessible via son IP publique sur le port configuré :
* **URL de l'API (Healthcheck)** : `http://40.66.52.118:8022/health`
