"""
Self-Supervised Learning Model for Text Summarization

This module implements a Self-Supervised Learning (SSL) model that can be used
for text processing and summarization tasks.
"""

import logging
import os
from typing import Optional, List, Dict, Any
import torch
from transformers import (
    AutoTokenizer, 
    AutoModel,
    AutoModelForSeq2SeqLM,
    pipeline
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)


class SSLTextModel:
    """
    Self-Supervised Learning model for text processing.
    
    This model uses pre-trained transformers and self-supervised learning
    techniques to process, encode, and summarize text documents.
    """
    
    def __init__(
        self, 
        model_name: str = "facebook/bart-large-cnn",
        device: Optional[str] = None
    ):
        """
        Initialize the SSL text model.
        
        Args:
            model_name: Name of the pre-trained model to use
            device: Device to use ('cuda', 'cpu', or None for auto-detect)
        """
        self.model_name = model_name
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"Initializing SSL model on device: {self.device}")
        
        # Initialize tokenizer and model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            # Initialize summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            logger.info(f"Successfully loaded model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def encode_text(self, text: str) -> Optional[torch.Tensor]:
        """
        Encode text into embeddings using the SSL model.
        
        Args:
            text: Input text to encode
            
        Returns:
            Tensor containing text embeddings or None if error occurs
        """
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                max_length=1024,
                truncation=True,
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.model.encoder(**inputs)
                embeddings = outputs.last_hidden_state
            
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return None
    
    def summarize(
        self,
        text: str,
        max_length: int = 150,
        min_length: int = 50,
        do_sample: bool = False
    ) -> Optional[str]:
        """
        Generate a summary of the input text using SSL.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            do_sample: Whether to use sampling for generation
            
        Returns:
            Generated summary or None if error occurs
        """
        try:
            # Split text into chunks if it's too long
            max_chunk_length = 1024
            text_chunks = self._chunk_text(text, max_chunk_length)
            
            summaries = []
            for chunk in text_chunks:
                result = self.summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=do_sample
                )
                summaries.append(result[0]['summary_text'])
            
            # Combine summaries
            final_summary = " ".join(summaries)
            
            logger.info(f"Generated summary of length: {len(final_summary)}")
            return final_summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None
    
    def extract_key_sentences(
        self,
        text: str,
        num_sentences: int = 5
    ) -> List[str]:
        """
        Extract key sentences from text using TF-IDF and cosine similarity.
        
        Args:
            text: Input text
            num_sentences: Number of key sentences to extract
            
        Returns:
            List of key sentences
        """
        try:
            # Split into sentences
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if len(sentences) <= num_sentences:
                return sentences
            
            # Calculate TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Calculate sentence importance
            sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
            
            # Get top sentences
            top_indices = sentence_scores.argsort()[-num_sentences:][::-1]
            top_indices = sorted(top_indices)  # Keep original order
            
            key_sentences = [sentences[i] for i in top_indices]
            
            logger.info(f"Extracted {len(key_sentences)} key sentences")
            return key_sentences
            
        except Exception as e:
            logger.error(f"Error extracting key sentences: {e}")
            return []
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        try:
            embeddings1 = self.encode_text(text1)
            embeddings2 = self.encode_text(text2)
            
            if embeddings1 is None or embeddings2 is None:
                return 0.0
            
            # Average pooling
            emb1 = embeddings1.mean(dim=1).cpu().numpy()
            emb2 = embeddings2.mean(dim=1).cpu().numpy()
            
            # Cosine similarity
            similarity = cosine_similarity(emb1, emb2)[0][0]
            
            logger.info(f"Computed similarity: {similarity:.4f}")
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0
    
    def _chunk_text(self, text: str, max_length: int) -> List[str]:
        """
        Split text into chunks of maximum length.
        
        Args:
            text: Input text
            max_length: Maximum chunk length in tokens
            
        Returns:
            List of text chunks
        """
        # Simple word-based chunking
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(self.tokenizer.encode(word, add_special_tokens=False))
            if current_length + word_length > max_length and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary containing model information
        """
        return {
            'model_name': self.model_name,
            'device': self.device,
            'num_parameters': sum(p.numel() for p in self.model.parameters()),
            'model_type': type(self.model).__name__
        }
