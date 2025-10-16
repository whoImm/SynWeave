import math
from typing import Dict, List, Tuple, Set
from collections import Counter
import re

class AdvancedPatternDetector:
    def __init__(self):
        self.keyboard_rows = {
            'qwerty': '1234567890',
            'numpad_vertical': '14702580369',
            'numpad_horizontal': '1234567890'
        }

        self.special_numbers = {
            '777', '888', '999', '666', '333', '111', '000',
            '1004', '1313', '1010', '2000', '2020', '2023', '2024'
        }
        
        self.plate_codes = self._generate_plate_codes()
    
    def _generate_plate_codes(self) -> Set[str]:
        return set(str(i).zfill(2) for i in range(1, 82))
    
    def analyze_password(self, password: str) -> Dict[str, float]:
        if not password.isdigit() or not (3 <= len(password) <= 8):
            return {'total_score': 0, 'breakdown': {}}
        
        analysis = {}
        analysis['length_score'] = self._analyze_length(password)
        analysis['sequential_score'] = self._analyze_sequential(password)
        analysis['repetition_score'] = self._analyze_repetition(password)
        analysis['keyboard_score'] = self._analyze_keyboard_pattern(password)
        analysis['entropy_score'] = self._analyze_entropy(password)
        analysis['social_score'] = self._analyze_social(password)
        analysis['cultural_score'] = self._analyze_cultural(password)
        analysis['geographic_score'] = self._analyze_geographic(password)
        total_score = sum(analysis.values())
        analysis['total_score'] = min(total_score, 50)
        
        return analysis
    
    def _analyze_length(self, password: str) -> float:
        length = len(password)
        if length <= 4:
            return 8.0 
        elif length == 5:
            return 6.0
        elif length == 6:
            return 4.0
        elif length == 7:
            return 2.0
        else:
            return 0.0
    
    def _analyze_sequential(self, password: str) -> float:
        if len(password) < 2:
            return 0.0
        
        increasing = all(int(password[i+1]) - int(password[i]) == 1 
                        for i in range(len(password)-1))

        decreasing = all(int(password[i]) - int(password[i+1]) == 1 
                        for i in range(len(password)-1))

        partial_seq = self._find_longest_sequence(password)
        
        if increasing or decreasing:
            return 7.0
        elif partial_seq >= 4:
            return 4.0
        elif partial_seq >= 3:
            return 2.0
        else:
            return 0.0
    
    def _find_longest_sequence(self, password: str) -> int:
        max_seq = 1
        current_seq = 1
        
        for i in range(1, len(password)):
            diff = int(password[i]) - int(password[i-1])
            if abs(diff) == 1:
                current_seq += 1
                max_seq = max(max_seq, current_seq)
            else:
                current_seq = 1
        
        return max_seq
    
    def _analyze_repetition(self, password: str) -> float:
        if len(set(password)) == 1:
            return 6.0

        if self._has_pair_repetition(password):
            return 5.0

        if self._has_pattern_repetition(password):
            return 4.0

        if self._has_partial_repetition(password):
            return 3.0
        
        return 0.0
    
    def _has_pair_repetition(self, password: str) -> bool:
        if len(password) % 2 != 0:
            return False
        
        for i in range(0, len(password), 2):
            if i+1 < len(password) and password[i] != password[i+1]:
                return False
        return True
    
    def _has_pattern_repetition(self, password: str) -> bool:
        length = len(password)
        for pattern_len in range(1, length//2 + 1):
            if length % pattern_len == 0:
                pattern = password[:pattern_len]
                repeats = length // pattern_len
                if pattern * repeats == password:
                    return True
        return False
    
    def _has_partial_repetition(self, password: str) -> bool:
        counter = Counter(password)
        most_common_count = counter.most_common(1)[0][1]
        if most_common_count >= len(password) * 0.75:
            return True
        if len(counter) == 2:
            counts = sorted(counter.values(), reverse=True)
            if counts[0] >= len(password) * 0.6:
                return True
        
        return False
    
    def _analyze_keyboard_pattern(self, password: str) -> float:
        if self._is_numpad_vertical(password):
            return 6.0

        if self._is_numpad_horizontal(password):
            return 5.0
        
        if self._is_qwerty_sequence(password):
            return 4.0
        
        if self._is_diagonal_pattern(password):
            return 3.0
        
        return 0.0
    
    def _is_numpad_vertical(self, password: str) -> bool:
        columns = ['1470', '2580', '369']
        return any(all(char in col for char in password) for col in columns)
    
    def _is_numpad_horizontal(self, password: str) -> bool:
        rows = ['123', '456', '789', '0']
        return any(all(char in row for char in password) for row in rows)
    
    def _is_qwerty_sequence(self, password: str) -> bool:
        qwerty_row = '1234567890'
        return password in qwerty_row or password[::-1] in qwerty_row
    
    def _is_diagonal_pattern(self, password: str) -> bool:
        diagonals = ['159', '357', '159753', '357951']
        return password in diagonals or password[::-1] in diagonals
    
    def _analyze_entropy(self, password: str) -> float:
        unique_chars = len(set(password))
        total_chars = len(password)

        if unique_chars == 1:
            return 8.0
        elif unique_chars == 2:
            return 6.0
        elif unique_chars == 3:
            return 4.0
        elif unique_chars >= total_chars * 0.75:
            return 0.0
        else:
            return 2.0
    
    def _analyze_social(self, password: str) -> float:
        if len(password) == 4:
            year = int(password)
            if 1980 <= year <= 1999:
                return 7.0
            elif 2000 <= year <= 2010:
                return 5.0
            elif 2011 <= year <= 2024:
                return 3.0
            elif 1950 <= year <= 1979:
                return 2.0

        if password in ['100', '200', '300', '400', '500', 
                       '123', '1234', '12345', '123456']:
            return 4.0
        
        return 0.0
    
    def _analyze_cultural(self, password: str) -> float:
        if password in self.special_numbers:
            return 5.0
        if len(set(password)) == 1 and len(password) >= 3:
            digit = password[0]
            if digit in '789':
                return 3.0
            elif digit == '6':
                return 2.0
        
        return 0.0
    
    def _analyze_geographic(self, password: str) -> float:
        if len(password) >= 2:
            first_two = password[:2]
            if first_two in self.plate_codes:
                return 3.0

        if len(password) == 5 and password.isdigit():
            return 1.0
        
        return 0.0
    
    def get_detailed_breakdown(self, password: str) -> Dict:
        analysis = self.analyze_password(password)
        
        breakdown = {
            'password': password,
            'total_score': analysis['total_score'],
            'risk_level': self._get_risk_level(analysis['total_score']),
            'details': {
                'length_analysis': f"{analysis['length_score']}/8 - Uzunluk riski",
                'sequential_analysis': f"{analysis['sequential_score']}/7 - Ardışıklık",
                'repetition_analysis': f"{analysis['repetition_score']}/6 - Tekrar pattern'i",
                'keyboard_analysis': f"{analysis['keyboard_score']}/6 - Klavye pattern'i", 
                'entropy_analysis': f"{analysis['entropy_score']}/8 - Entropi düşüklüğü",
                'social_analysis': f"{analysis['social_score']}/7 - Sosyal mühendislik",
                'cultural_analysis': f"{analysis['cultural_score']}/5 - Kültürel referans",
                'geographic_analysis': f"{analysis['geographic_score']}/3 - Coğrafi pattern"
            }
        }
        
        return breakdown
    
    def _get_risk_level(self, score: float) -> str:
        if score >= 40:
            return "🚨 VERY HIGH RISK"
        elif score >= 30:
            return "⚠️ HIGH RISK" 
        elif score >= 20:
            return "🎯 ORTA RİSK"
        elif score >= 10:
            return "✅ MEDIUM RISK"
        else:
            return "🛡️  SECURE"