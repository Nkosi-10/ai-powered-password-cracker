"""
AI-Powered Password Guesser Module

Uses Google Gemini AI to intelligently select attack methods and generate
password candidates based on context and patterns.
"""

import os
import time
import json
from typing import Optional, Tuple, List, Dict
import google.generativeai as genai
from utils.hash_utils import verify_hash


class AIGuesser:
    """
    AI-powered password guessing using Google Gemini.
    
    This class analyzes password context and uses AI to select
    optimal attack strategies and generate intelligent guesses.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AI guesser.
        
        Args:
            api_key: Google Gemini API key. If None, tries to get from environment.
        """
        # Try multiple environment variable names for compatibility
        if not api_key:
            api_key_names = ['GOOGLE_API_KEY', 'MY_API_KEY', 'GEMINI_API_KEY']
            for key_name in api_key_names:
                api_key = os.getenv(key_name)
                if api_key:
                    break
        
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Google Gemini API key required. Set GOOGLE_API_KEY, MY_API_KEY, or GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        self.ai_analysis = None
    
    def crack(self, target_hash: str, context: str = "") -> Tuple[Optional[str], int, float]:
        """
        Attempt to crack password using AI-powered analysis.
        
        Args:
            target_hash: The hash to crack (must be synthetic)
            context: Optional context about the password (e.g., "user's birthday")
            
        Returns:
            Tuple of (cracked_password, attempts_made, time_taken)
        """
        if not self._validate_input(target_hash):
            raise ValueError("Invalid input detected. Only synthetic hashes allowed.")
        
        self.attempts = 0
        self.start_time = time.time()
        
        print(f"🧠 Starting AI-Powered Attack...")
        print(f"🔍 Analyzing password context...")
        
        try:
            # Get AI analysis and recommendations
            self.ai_analysis = self._analyze_with_ai(target_hash, context)
            print(f"🤖 AI Analysis: {self.ai_analysis.get('recommendation', 'No specific recommendation')}")
            
            # Generate AI-suggested passwords
            ai_passwords = self._generate_ai_passwords(target_hash, context)
            print(f"💡 AI generated {len(ai_passwords)} password candidates")
            
            # Try AI-generated passwords
            for password in ai_passwords:
                self.attempts += 1
                print(f"🔍 AI trying: {password}")
                
                if verify_hash(password, target_hash):
                    return self._success(password)
            
            # If AI fails, try hybrid approach with common patterns
            print(f"🔄 AI approach failed, trying hybrid method...")
            hybrid_passwords = self._hybrid_approach(target_hash, context)
            
            for password in hybrid_passwords:
                self.attempts += 1
                if verify_hash(password, target_hash):
                    return self._success(password)
            
            return self._failure()
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            print(f"🔄 Falling back to basic pattern matching...")
            return self._fallback_attack(target_hash)
    
    def _analyze_with_ai(self, target_hash: str, context: str) -> Dict:
        """Analyze password with AI to get recommendations."""
        prompt = f"""
        You are a cybersecurity expert analyzing a password hash for educational purposes.
        
        Hash: {target_hash}
        Context: {context or "No specific context provided"}
        
        Based on this information, provide:
        1. Recommended attack strategy (brute force, dictionary, rule-based, or hybrid)
        2. Reasoning for the recommendation
        3. Estimated success probability
        4. Any patterns you notice
        
        Respond in JSON format:
        {{
            "recommendation": "attack_type",
            "reasoning": "explanation",
            "probability": "high/medium/low",
            "patterns": ["pattern1", "pattern2"]
        }}
        
        IMPORTANT: This is for educational simulation only. Only provide general security insights.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON response
            analysis = json.loads(response.text)
            return analysis
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            return {
                "recommendation": "hybrid",
                "reasoning": "AI analysis unavailable, using fallback",
                "probability": "medium",
                "patterns": []
            }
    
    def _generate_ai_passwords(self, target_hash: str, context: str) -> List[str]:
        """Generate password candidates using AI."""
        prompt = f"""
        Generate 10-15 password candidates based on this context:
        
        Hash: {target_hash}
        Context: {context or "No specific context"}
        
        Consider:
        - Common password patterns
        - Context-appropriate words
        - Common variations (numbers, symbols, capitalization)
        - Keyboard patterns
        
        Return only the passwords, one per line, no explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            passwords = [line.strip() for line in response.text.split('\n') if line.strip()]
            return passwords[:15]  # Limit to 15 passwords
        except Exception as e:
            print(f"⚠️ AI password generation failed: {e}")
            return []
    
    def _hybrid_approach(self, target_hash: str, context: str) -> List[str]:
        """Combine AI insights with common patterns."""
        passwords = []
        
        # Context-based patterns
        if context:
            context_words = context.lower().split()
            for word in context_words:
                if len(word) >= 3:
                    passwords.extend([
                        word,
                        word.capitalize(),
                        word.upper(),
                        f"{word}123",
                        f"123{word}",
                        f"{word}!",
                        f"!{word}"
                    ])
        
        # Common patterns based on AI analysis
        if self.ai_analysis and 'patterns' in self.ai_analysis:
            for pattern in self.ai_analysis['patterns']:
                if pattern and len(pattern) >= 3:
                    passwords.append(pattern)
        
        # Add some common passwords
        common = ['password', 'admin', '123456', 'qwerty', 'letmein']
        passwords.extend(common)
        
        return passwords
    
    def _fallback_attack(self, target_hash: str) -> Tuple[Optional[str], int, float]:
        """Fallback attack when AI fails."""
        print(f"🔄 Using fallback pattern matching...")
        
        # Try common passwords
        common_passwords = [
            'password', '123456', 'qwerty', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'master', 'freedom'
        ]
        
        for password in common_passwords:
            self.attempts += 1
            if verify_hash(password, target_hash):
                return self._success(password)
        
        return self._failure()
    
    def _success(self, password: str) -> Tuple[str, int, float]:
        """Handle successful password crack."""
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        print(f"✅ Password Found: {password}")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"📊 Attempts made: {self.attempts}")
        
        return password, self.attempts, time_taken
    
    def _failure(self) -> Tuple[None, int, float]:
        """Handle failed password crack."""
        self.end_time = time.time()
        time_taken = self.end_time - self.start_time
        
        print(f"❌ Password not found using AI")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"📊 Total attempts: {self.attempts}")
        
        return None, self.attempts, time_taken
    
    def _validate_input(self, target_hash: str) -> bool:
        """Validate input is safe for simulation."""
        suspicious_patterns = ['$2b$', '$2a$', '$1$', '$6$', '$5$']
        for pattern in suspicious_patterns:
            if target_hash.startswith(pattern):
                print(f"⚠️ Warning: Hash pattern '{pattern}' detected!")
                return False
        return True
    
    def get_stats(self) -> dict:
        """Get attack statistics."""
        if self.start_time is None:
            return {}
        
        time_taken = (self.end_time or time.time()) - self.start_time
        return {
            'method': 'AI-Powered Attack',
            'attempts': self.attempts,
            'time_taken': time_taken,
            'ai_analysis': self.ai_analysis,
            'success': self.attempts > 0 and self.end_time is not None
        }
    
    def get_ai_insights(self) -> Dict:
        """Get AI analysis insights."""
        return self.ai_analysis or {}
