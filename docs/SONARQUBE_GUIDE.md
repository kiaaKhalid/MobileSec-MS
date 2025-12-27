# Guide SonarQube pour MobileSec-MS 🔍

Ce guide explique comment accéder à SonarQube et configurer l'analyse.

## 1. Accès au Dashboard
Une fois `docker-compose up -d` lancé, SonarQube est accessible ici :
👉 **http://localhost:9000**

- **Login par défaut** : `admin`
- **Mot de passe par défaut** : `admin` (Il vous demandera de le changer)

---

## 2. Générer le Token (Obligatoire pour Jenkins)
Pour que Jenkins puisse envoyer des analyses, il faut un Token.

1.  Connectez-vous à SonarQube (`admin` / votre nouveau mot de passe).
2.  Allez dans **My Account** (Cliquez sur votre avatar en haut à droite) > **Security**.
3.  Dans "Generate Token" :
    - **Name** : `jenkins`
    - **Type** : `Global Analysis Token`
    - **Expiration** : `No expiration`
    - Cliquez sur **Generate**.
4.  🛑 **copiez ce token immédiatement**, vous ne pourrez plus le voir !

---

## 3. Configurer Jenkins
Jenkins a besoin de ce token pour s'authentifier.

1.  Allez dans votre Job Jenkins > **Configurer**.
2.  Dans la configuration du Pipeline, vous devez injecter ce token. Le plus simple pour un test rapide est de modifier le script `Jenkinsfile` dans l'interface Jenkins.
3.  Remplacez `${SONAR_TOKEN}` par votre vrai token (ex: `sqa_...`).

> **Bonne pratique (Production)** :
> Idéalement, ajoutez ce token dans les "Credentials" de Jenkins (ID: `sonar-token`) et utilisez `withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')])`.

---

## 4. Lancer l'analyse
Relancez simplement votre Job Jenkins ("Build with Parameters").
Une nouvelle étape **"Code Quality"** apparaitra et enverra les résultats à SonarQube.

✅ **Résultat** : Rafraichissez http://localhost:9000 pour voir les bugs, "code smells" et la duplication de code !
