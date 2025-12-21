# Guide d'utilisation de l'AI Scanner

## Vue d'ensemble

L'AI Scanner utilise un modèle de Deep Learning basé sur des réseaux de neurones convolutifs (CNN) pour détecter les malwares Android à partir de l'analyse statique des permissions.

## Fonctionnalités

### Analyse en temps réel
- Upload de fichiers APK par glisser-déposer ou sélection
- Analyse automatique des permissions
- Détection de patterns malveillants

### Résultats détaillés
- **Score de risque** : Pourcentage de probabilité de malware (0-100%)
- **Score de confiance** : Niveau de confiance du modèle dans sa prédiction
- **Statut** : SECURE, SUSPICIOUS, ou MALWARE
- **Permissions détectées** : Liste des permissions demandées par l'APK

### Recommandations intelligentes
Le système fournit des recommandations contextuelles basées sur le niveau de risque détecté.

## Utilisation

1. **Sélectionner un fichier APK**
   - Glissez-déposez le fichier dans la zone prévue
   - Ou cliquez pour ouvrir le sélecteur de fichiers

2. **Lancer l'analyse**
   - Cliquez sur "Analyser l'APK"
   - Attendez quelques secondes pendant le traitement

3. **Consulter les résultats**
   - Vérifiez le score de risque
   - Lisez les recommandations
   - Examinez les permissions détectées

## Interprétation des résultats

### SECURE (Vert)
- Score de risque < 30%
- Aucun pattern malveillant détecté
- Installation sûre

### SUSPICIOUS (Orange)
- Score de risque 30-70%
- Patterns inhabituels détectés
- Procéder avec prudence

### MALWARE (Rouge)
- Score de risque > 70%
- Patterns malveillants confirmés
- Ne pas installer

## Moteur d'analyse

**MobileSec-DeepLearning-v3**
- Architecture CNN optimisée
- Entraîné sur 50,000+ échantillons
- Précision : 96.5%
- Taux de faux positifs : < 2%
