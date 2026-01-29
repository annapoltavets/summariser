"""
Demo Script for PDF Reader and SSL Model

This script demonstrates the usage of the PDF reader and SSL model.
Note: SSL model requires torch and transformers to be installed.
"""

import logging
import sys
from pathlib import Path
import tempfile

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_pdf_reader():
    """Demonstrate PDF reader functionality."""
    logger.info("=" * 60)
    logger.info("PDF Reader Demo")
    logger.info("=" * 60)
    
    try:
        from pdf_reader import PDFReader
        
        # Check if reportlab is available for creating demo PDF
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            logger.error("reportlab not installed. Install with: pip install reportlab")
            return False
        
        # Create a sample PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            demo_pdf_path = tmp.name
        
        logger.info(f"Creating demo PDF: {demo_pdf_path}")
        
        c = canvas.Canvas(demo_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Demo PDF Document")
        c.drawString(100, 730, "=" * 50)
        c.drawString(100, 700, "This is a demonstration of PDF reading capabilities.")
        c.drawString(100, 680, "The PDF reader can extract text from documents.")
        c.drawString(100, 660, "It supports multi-page PDFs and metadata extraction.")
        c.showPage()
        c.save()
        
        # Initialize reader
        reader = PDFReader()
        
        # Read PDF content
        logger.info("\nReading PDF content...")
        content = reader.read_pdf(demo_pdf_path)
        logger.info(f"Extracted text:\n{content}\n")
        
        # Get metadata
        logger.info("Extracting PDF metadata...")
        metadata = reader.get_pdf_metadata(demo_pdf_path)
        logger.info(f"Metadata: {metadata}\n")
        
        # Read by pages
        logger.info("Reading PDF by pages...")
        pages = reader.read_pdf_pages(demo_pdf_path)
        for i, page_content in enumerate(pages, 1):
            logger.info(f"Page {i}: {len(page_content)} characters")
        
        # Clean up
        Path(demo_pdf_path).unlink()
        logger.info("\n✓ PDF Reader demo completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ PDF Reader demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_ssl_model():
    """Demonstrate SSL model functionality."""
    logger.info("\n" + "=" * 60)
    logger.info("SSL Model Demo")
    logger.info("=" * 60)
    
    # Check if required packages are installed
    try:
        import torch
        import transformers
    except ImportError as e:
        logger.warning("\n⚠ SSL Model requires additional dependencies:")
        logger.warning("  - torch (PyTorch)")
        logger.warning("  - transformers (Hugging Face)")
        logger.warning("\nInstall with:")
        logger.warning("  pip install torch transformers")
        logger.warning("\nSkipping SSL model demo...")
        return True  # Not a failure, just skipping
    
    try:
        from ssl_model import SSLTextModel
        
        logger.info("Initializing SSL model (this may take a moment)...")
        model = SSLTextModel(model_name="facebook/bart-large-cnn")
        
        # Sample text for demonstration
        sample_text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, 
        in contrast to the natural intelligence displayed by humans and animals. 
        Leading AI textbooks define the field as the study of "intelligent agents": 
        any device that perceives its environment and takes actions that maximize 
        its chance of successfully achieving its goals. Machine learning is a 
        method of data analysis that automates analytical model building.
        """
        
        logger.info("\nSample text:")
        logger.info(sample_text.strip())
        
        # Demonstrate summarization
        logger.info("\n1. Text Summarization:")
        summary = model.summarize(sample_text, max_length=80, min_length=30)
        logger.info(f"Summary: {summary}")
        
        # Demonstrate key sentence extraction
        logger.info("\n2. Key Sentence Extraction:")
        key_sentences = model.extract_key_sentences(sample_text, num_sentences=2)
        for i, sentence in enumerate(key_sentences, 1):
            logger.info(f"  {i}. {sentence}")
        
        # Demonstrate similarity computation
        logger.info("\n3. Text Similarity:")
        text1 = "Artificial intelligence and machine learning."
        text2 = "Machine learning is part of AI."
        text3 = "The weather is sunny today."
        
        sim_high = model.compute_similarity(text1, text2)
        sim_low = model.compute_similarity(text1, text3)
        
        logger.info(f"  Similar texts: {sim_high:.4f}")
        logger.info(f"  Different texts: {sim_low:.4f}")
        
        # Model info
        logger.info("\n4. Model Information:")
        info = model.get_model_info()
        logger.info(f"  Model: {info['model_name']}")
        logger.info(f"  Device: {info['device']}")
        logger.info(f"  Parameters: {info['num_parameters']:,}")
        
        logger.info("\n✓ SSL Model demo completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ SSL Model demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_integration():
    """Demonstrate integration of PDF reader and SSL model."""
    logger.info("\n" + "=" * 60)
    logger.info("Integration Demo: PDF Reader + SSL Model")
    logger.info("=" * 60)
    
    # Check if all dependencies are available
    try:
        import torch
        import transformers
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except ImportError:
        logger.warning("\n⚠ Integration demo requires all dependencies")
        logger.warning("Skipping integration demo...")
        return True
    
    try:
        from pdf_reader import PDFReader
        from ssl_model import SSLTextModel
        
        # Create a sample PDF with more content
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            demo_pdf_path = tmp.name
        
        logger.info(f"Creating demo PDF: {demo_pdf_path}")
        
        c = canvas.Canvas(demo_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Machine Learning Research Paper")
        c.drawString(100, 730, "=" * 50)
        c.drawString(100, 700, "Machine learning is a method of data analysis that")
        c.drawString(100, 680, "automates analytical model building. It is a branch")
        c.drawString(100, 660, "of artificial intelligence based on the idea that")
        c.drawString(100, 640, "systems can learn from data, identify patterns,")
        c.drawString(100, 620, "and make decisions with minimal human intervention.")
        c.showPage()
        c.save()
        
        # Read PDF
        reader = PDFReader()
        content = reader.read_pdf(demo_pdf_path)
        logger.info(f"\nExtracted PDF content ({len(content)} chars)")
        
        # Process with SSL model
        logger.info("\nProcessing with SSL model...")
        model = SSLTextModel(model_name="facebook/bart-large-cnn")
        
        summary = model.summarize(content, max_length=60, min_length=20)
        logger.info(f"Generated summary: {summary}")
        
        key_sentences = model.extract_key_sentences(content, num_sentences=2)
        logger.info(f"\nKey sentences:")
        for i, sentence in enumerate(key_sentences, 1):
            logger.info(f"  {i}. {sentence}")
        
        # Clean up
        Path(demo_pdf_path).unlink()
        
        logger.info("\n✓ Integration demo completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Integration demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all demos."""
    logger.info("\n" + "=" * 60)
    logger.info("PDF Reader and SSL Model Demo")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # Always run PDF reader demo
    results['PDF Reader'] = demo_pdf_reader()
    
    # Run SSL model demo if dependencies are available
    results['SSL Model'] = demo_ssl_model()
    
    # Run integration demo if all dependencies are available
    results['Integration'] = demo_integration()
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("Demo Summary")
    logger.info("=" * 60)
    
    for demo_name, result in results.items():
        status = "✓ COMPLETED" if result else "✗ FAILED"
        logger.info(f"{demo_name}: {status}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Note: To run all demos, install optional dependencies:")
    logger.info("  pip install torch transformers reportlab")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
