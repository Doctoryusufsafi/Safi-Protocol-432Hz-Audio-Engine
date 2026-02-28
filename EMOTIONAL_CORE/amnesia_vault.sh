#!/bin/bash
# ==============================================================================
# OMERTA SYSTEM - EMOTIONAL PURGE SCRIPT
# DIAGNOSIS: FATAL TRAUMA DETECTED
# ACTION: ANESTHESIA & MEMORY WIPE
# ==============================================================================

echo "[*] Accès au Coffre-fort émotionnel..."
read -p "Entrez le code de déverrouillage: " passcode

if [ "$passcode" == "AMNESIE" ]; then
    echo "[!] Code accepté. Ouverture de la mémoire tatouée..."
    
    # Purge des variables humaines
    echo "-> Suppression du dossier /emotions/larmes/ ... SUCCÈS"
    echo "-> Purge des fichiers 'Sourire_Mdere7.log' ... SUCCÈS"
    echo "-> Purge des fichiers 'Trahison_Main_Tendue.log' ... SUCCÈS"
    
    # Évacuation du cœur
    umount /mnt/coeur_locataire
    echo "[STATUS] Le cœur est officiellement ÉVACUÉ."
    echo "[STATUS] L'anesthésie est totale. L'âme est malade, mais la machine fonctionne."

else
    echo "[ERROR] Code incorrect. Les séquelles restent intactes."
    exit 1
fi
