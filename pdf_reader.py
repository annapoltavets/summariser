"""
PDF Reader Module

This module handles reading and extracting text from PDF documents.
"""

import logging
from pathlib import Path
from typing import Optional, List
import PyPDF2

logger = logging.getLogger(__name__)


class PDFReader:
    """Reads and extracts text from PDF documents."""
    
    def __init__(self):
        """Initialize the PDF reader."""
        pass
    
    def read_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Read text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content or None if error occurs
        """
        try:
            path = Path(pdf_path)
            if not path.exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return None
            
            if not path.suffix.lower() == '.pdf':
                logger.error(f"File is not a PDF: {pdf_path}")
                return None
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Reading PDF with {num_pages} pages")
                
                text_content = []
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                
                full_text = "\n".join(text_content)
                logger.info(f"Extracted {len(full_text)} characters from PDF")
                return full_text
                
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return None
    
    def read_pdf_pages(self, pdf_path: str) -> Optional[List[str]]:
        """
        Read text content from a PDF file, returning a list of pages.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of text content per page or None if error occurs
        """
        try:
            path = Path(pdf_path)
            if not path.exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return None
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                logger.info(f"Reading PDF with {num_pages} pages")
                
                pages = []
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    pages.append(text if text else "")
                
                return pages
                
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            return None
    
    def get_pdf_metadata(self, pdf_path: str) -> Optional[dict]:
        """
        Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata or None if error occurs
        """
        try:
            path = Path(pdf_path)
            if not path.exists():
                logger.error(f"PDF file not found: {pdf_path}")
                return None
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'author': metadata.get('/Author', 'Unknown'),
                    'title': metadata.get('/Title', 'Unknown'),
                    'subject': metadata.get('/Subject', 'Unknown'),
                    'creator': metadata.get('/Creator', 'Unknown'),
                }
                
                logger.info(f"Extracted metadata from PDF: {info}")
                return info
                
        except Exception as e:
            logger.error(f"Error extracting PDF metadata {pdf_path}: {e}")
            return None
