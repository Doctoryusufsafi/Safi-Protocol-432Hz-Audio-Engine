"""
OMERTA CLINICAL RESEARCH - SAFI PROTOCOL
Script Python pour la conversion 440Hz -> 432Hz (Pitch-shift indépendant du tempo)
Dépendances requises : pip install librosa soundfile numpy
"""

import librosa
import soundfile as sf
import numpy as np

def execute_safi_protocol(input_path, output_path, current_hz=440.0, target_hz=432.0):
    print(f"[*] Initialisation du Protocole Safi : {current_hz}Hz -> {target_hz}Hz")
    
    # 1. Chargement de la matrice audio (Payload)
    print("[*] Extraction des données audio...")
    y, sr = librosa.load(input_path, sr=None) # sr=None conserve le Sample Rate d'origine
    
    # 2. Calcul algorithmique du décalage
    # n_steps = 12 * log2(432/440) = -0.3176 demi-tons
    n_steps = 12 * np.log2(target_hz / current_hz)
    
    # 3. Application du traitement (Shift sans altérer le BPM)
    print("[*] Application de l'équation de transfert (Hemi-Sync bypass)...")
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
    
    # 4. Exportation de l'injection clinique
    print(f"[*] Exportation du fichier verrouillé vers : {output_path}")
    sf.write(output_path, y_shifted, sr)
    print("[STATUS] Opération terminée. Le fichier est calibré.")

# --- EXÉCUTION DU TERMINAL ---
if __name__ == "__main__":
    # Remplace ces noms par tes vrais fichiers WAV
    fichier_entree = "Casa_Velvet_Raw_440.wav"
    fichier_sortie = "Casa_Velvet_Incision_432.wav"
    
    execute_safi_protocol(fichier_entree, fichier_sortie)
