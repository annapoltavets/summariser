"""
PDF Summarizer Example

This script demonstrates how to use the PDF reader with the existing
AI summarizer to create summaries of PDF documents.
"""

import logging
import sys
from pathlib import Path

from pdf_reader import PDFReader
from ai_summarizer import AISummarizer
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def summarize_pdf(pdf_path: str, model: str = "gpt-4o-mini") -> dict:
    """
    Read a PDF and generate a summary using OpenAI.
    
    Args:
        pdf_path: Path to the PDF file
        model: OpenAI model to use for summarization
        
    Returns:
        Dictionary containing PDF info and summary
    """
    logger.info(f"Processing PDF: {pdf_path}")
    
    # Initialize PDF reader
    reader = PDFReader()
    
    # Read PDF content
    content = reader.read_pdf(pdf_path)
    if content is None:
        logger.error("Failed to read PDF content")
        return None
    
    logger.info(f"Extracted {len(content)} characters from PDF")
    
    # Get PDF metadata
    metadata = reader.get_pdf_metadata(pdf_path)
    logger.info(f"PDF has {metadata['num_pages']} page(s)")
    
    # Initialize AI summarizer
    summarizer = AISummarizer(model=model)
    
    # Create system prompt for summarization
    system_prompt = """You are an expert at summarizing documents. 
    Create a concise, well-structured summary of the following text. 
    Highlight the main points and key takeaways."""
    
    # Generate summary
    logger.info("Generating summary...")
    summary = summarizer.summarize(system_prompt, content)
    
    if summary is None:
        logger.error("Failed to generate summary")
        return None
    
    logger.info("Summary generated successfully")
    
    # Return results
    return {
        'pdf_path': pdf_path,
        'title': metadata.get('title', 'Unknown'),
        'author': metadata.get('author', 'Unknown'),
        'num_pages': metadata['num_pages'],
        'content_length': len(content),
        'summary': summary
    }


def main():
    """Main function to demonstrate PDF summarization."""
    logger.info("=" * 60)
    logger.info("PDF Summarizer Example")
    logger.info("=" * 60 + "\n")
    
    # Check for command line argument
    if len(sys.argv) < 2:
        logger.info("Usage: python pdf_summarizer_example.py <path_to_pdf>")
        logger.info("\nExample: python pdf_summarizer_example.py document.pdf")
        logger.info("\nNote: This requires OPENAI_API_KEY to be set in .env file")
        
        # Create a demo PDF if reportlab is available
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            import tempfile
            
            logger.info("\n" + "=" * 60)
            logger.info("Creating demo PDF for testing...")
            logger.info("=" * 60 + "\n")
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                demo_pdf_path = tmp.name
            
            c = canvas.Canvas(demo_pdf_path, pagesize=letter)
            c.drawString(100, 750, "Sample Research Paper")
            c.drawString(100, 730, "=" * 50)
            c.drawString(100, 700, "Abstract")
            c.drawString(100, 680, "This paper discusses the fundamentals of machine learning")
            c.drawString(100, 660, "and its applications in various domains. Machine learning")
            c.drawString(100, 640, "enables computers to learn from data and improve their")
            c.drawString(100, 620, "performance over time without explicit programming.")
            c.drawString(100, 590, "")
            c.drawString(100, 570, "Introduction")
            c.drawString(100, 550, "Artificial intelligence has revolutionized how we process")
            c.drawString(100, 530, "information and make decisions. Deep learning models have")
            c.drawString(100, 510, "achieved remarkable results in image recognition, natural")
            c.drawString(100, 490, "language processing, and many other fields.")
            c.showPage()
            c.save()
            
            logger.info(f"Demo PDF created: {demo_pdf_path}")
            logger.info("\nProcessing demo PDF...")
            
            result = summarize_pdf(demo_pdf_path)
            
            if result:
                logger.info("\n" + "=" * 60)
                logger.info("Summary Results")
                logger.info("=" * 60)
                logger.info(f"PDF: {result['pdf_path']}")
                logger.info(f"Title: {result['title']}")
                logger.info(f"Pages: {result['num_pages']}")
                logger.info(f"Content Length: {result['content_length']} characters")
                logger.info(f"\nSummary:\n{result['summary']}")
                logger.info("=" * 60)
            
            # Clean up
            Path(demo_pdf_path).unlink()
            logger.info("\nDemo completed successfully!")
            
        except ImportError:
            logger.warning("\nreportlab not installed. Install with: pip install reportlab")
        
        return
    
    # Process the provided PDF
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    result = summarize_pdf(pdf_path)
    
    if result:
        logger.info("\n" + "=" * 60)
        logger.info("Summary Results")
        logger.info("=" * 60)
        logger.info(f"PDF: {result['pdf_path']}")
        logger.info(f"Title: {result['title']}")
        logger.info(f"Author: {result['author']}")
        logger.info(f"Pages: {result['num_pages']}")
        logger.info(f"Content Length: {result['content_length']} characters")
        logger.info(f"\nSummary:\n{result['summary']}")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
