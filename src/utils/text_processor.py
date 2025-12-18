import re

class TextProcessor:
    @staticmethod
    def normalize_math_symbols(text: str) -> str:
        """
        Convert math symbols to natural language for better TTS experience.
        """
        if not text:
            return ""

        # Superscripts
        text = text.replace("²", "平方")
        text = text.replace("³", "立方")
        text = re.sub(r"\^2", "平方", text)
        text = re.sub(r"\^3", "立方", text)
        
        # Roots
        text = text.replace("√", "根号")
        
        # Basic operators (Context dependent, but generally safe replacements for clarity)
        # Note: Modern TTS engines handle + - * / well, but explicit text ensures consistency
        text = text.replace("≥", "大于等于")
        text = text.replace("≤", "小于等于")
        text = text.replace("≠", "不等于")
        text = text.replace("≈", "约等于")
        
        # Fractions could be complex, leaving simple / for now
        
        return text

    @staticmethod
    def split_text(text: str, max_length: int = 450) -> list[str]:
        """
        Split text into chunks smaller than max_length, respecting sentence boundaries.
        """
        if len(text) <= max_length:
            return [text]
            
        chunks = []
        current_chunk = ""
        
        # Split by common sentence delimiters
        sentences = re.split(r'([。！？；.!?;\n])', text)
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
                
        if current_chunk:
            chunks.append(current_chunk)
            
        return chunks
