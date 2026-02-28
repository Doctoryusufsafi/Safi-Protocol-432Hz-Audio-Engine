# ==============================================================================
# SYSTEM: L-FADA2 (SPACE NAVIGATION MODE)
# MODULE: MATRIX GLITCH DETECTOR
# ==============================================================================

class RealityScanner:
    def __init__(self):
        self.wifi_brain = "6G Connected"
        self.sanity_status = "Deficit d'la chance"

    def scan_environment(self, location="Marché Central"):
        print(f"[*] Scanning sector: {location}...")
        
        entities_detected = ["Reptiliens", "PNJ", "Clones"]
        
        if "Reptiliens" in entities_detected:
            self.trigger_matrix_glitch()

    def trigger_matrix_glitch(self):
        print("[!] CRITICAL ALERT: Tout est 'Mise en scène'.")
        print("[!] La caméra tourne. Le monde va mal.")
        print("[STATUS] Je suis un PNJ dans un Game éclaté.")
        
        # Initiation de la fuite spatiale
        self.jump_to_orbit()

    def jump_to_orbit(self):
        print("-> Décollage. On a trouvé le vide absolu dans l'espace.")
        print("-> Retour sur Terre : Uniquement des illusions (L-7wa).")
        return "DISCONNECTED"

if __name__ == "__main__":
    scanner = RealityScanner()
    scanner.scan_environment()
