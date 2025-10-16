import base64
import hashlib

class DeveloperProtection:
    def __init__(self):
        self.required_developers = self._decode_developers()
    
    def _decode_developers(self):
        encoded_devs = [
            "Z2l0aHViOiB3aG9JbW0=",
            "ZGlzY29yZDogcGFseWFjMA==",
            "c3lud2VhdmU6IHYyLjA="
        ]
        
        developers = []
        for encoded in encoded_devs:
            try:
                decoded = base64.b64decode(encoded).decode('utf-8')
                developers.append(decoded)
            except:
                pass
        
        return developers
    
    def verify_developers(self):
        if not self.required_developers:
            return False
        expected_lines = [
            "github: whoImm",
            "discord: palyac0", 
            "synweave: v1.0"
        ]
        
        return all(any(expected in dev for dev in self.required_developers) 
                  for expected in expected_lines)
    
    def get_developer_info(self):
        return self.required_developers