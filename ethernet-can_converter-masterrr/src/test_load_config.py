import unittest
import json

from file_handling.Load_config import LoadConfig  # Import après l'ajout de src/ au path

class TestLoadConfig(unittest.TestCase):
    def test_load_config(self):
        """Test pour charger la configuration et afficher son contenu."""
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/default_configuration.json"))
        
        config = LoadConfig.load_config(config_path)

        # Vérification de la présence des clés importantes
        self.assertIn("pc_mac", config)
        self.assertIn("raspberry_mac", config)
        self.assertIn("eth_type_can", config)

        # Afficher le contenu lu
        print("\n=== Contenu de la configuration chargée ===")
        print(json.dumps(config, indent=4, default=str))  # Utilisation de `default=str` pour afficher les bytes

if __name__ == "__main__":
    unittest.main()
