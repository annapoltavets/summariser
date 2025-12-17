"""
Test Script for SSL Model and PDF Reader

This script tests the Self-Supervised Learning model and PDF reader functionality.
"""

import logging
import sys
from pathlib import Path
import tempfile
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_pdf_reader():
    """Test PDF reading functionality."""
    logger.info("=" * 50)
    logger.info("Testing PDF Reader")
    logger.info("=" * 50)
    
    try:
        from pdf_reader import PDFReader
        
        reader = PDFReader()
        logger.info("✓ PDFReader initialized successfully")
        
        # Test with non-existent file
        result = reader.read_pdf("non_existent.pdf")
        assert result is None, "Should return None for non-existent file"
        logger.info("✓ Correctly handles non-existent file")
        
        # Create a simple test PDF using reportlab if available
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                test_pdf_path = tmp.name
                
            # Create a simple PDF
            c = canvas.Canvas(test_pdf_path, pagesize=letter)
            c.drawString(100, 750, "Test PDF Document")
            c.drawString(100, 730, "This is a test document for the SSL model.")
            c.drawString(100, 710, "It contains some sample text for testing.")
            c.showPage()
            c.save()
            
            # Test reading the PDF
            content = reader.read_pdf(test_pdf_path)
            assert content is not None, "Should read PDF content"
            assert "Test PDF Document" in content, "Should contain expected text"
            logger.info("✓ Successfully read PDF content")
            
            # Test reading pages
            pages = reader.read_pdf_pages(test_pdf_path)
            assert pages is not None, "Should return list of pages"
            assert len(pages) > 0, "Should have at least one page"
            logger.info(f"✓ Successfully read {len(pages)} page(s)")
            
            # Test metadata extraction
            metadata = reader.get_pdf_metadata(test_pdf_path)
            assert metadata is not None, "Should extract metadata"
            assert 'num_pages' in metadata, "Should have num_pages in metadata"
            logger.info("✓ Successfully extracted PDF metadata")
            
            # Clean up
            Path(test_pdf_path).unlink()
            
        except ImportError:
            logger.warning("reportlab not installed, skipping PDF creation test")
            logger.info("  Install with: pip install reportlab")
        
        logger.info("\n✓ All PDF Reader tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ PDF Reader test failed: {e}")
        return False


def test_ssl_model():
    """Test SSL Model functionality."""
    logger.info("\n" + "=" * 50)
    logger.info("Testing SSL Model")
    logger.info("=" * 50)
    
    try:
        from ssl_model import SSLTextModel
        
        # Initialize model (using a smaller model for testing)
        logger.info("Initializing SSL model (this may take a moment)...")
        model = SSLTextModel(model_name="facebook/bart-large-cnn")
        logger.info("✓ SSLTextModel initialized successfully")
        
        # Get model info
        info = model.get_model_info()
        logger.info(f"✓ Model info: {info['model_name']}, {info['num_parameters']:,} parameters")
        
        # Test text encoding
        logger.info("\nTesting text encoding...")
        test_text = "This is a test sentence for encoding."
        embeddings = model.encode_text(test_text)
        assert embeddings is not None, "Should generate embeddings"
        logger.info(f"✓ Generated embeddings with shape: {embeddings.shape}")
        
        # Test summarization
        logger.info("\nTesting text summarization...")
        long_text = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, 
        in contrast to the natural intelligence displayed by humans and animals. 
        Leading AI textbooks define the field as the study of "intelligent agents": 
        any device that perceives its environment and takes actions that maximize 
        its chance of successfully achieving its goals. Colloquially, the term 
        "artificial intelligence" is often used to describe machines that mimic 
        "cognitive" functions that humans associate with the human mind, such as 
        "learning" and "problem solving". As machines become increasingly capable, 
        tasks considered to require "intelligence" are often removed from the 
        definition of AI, a phenomenon known as the AI effect. A quip in Tesler's 
        Theorem says "AI is whatever hasn't been done yet."
        """
        
        summary = model.summarize(long_text, max_length=100, min_length=30)
        assert summary is not None, "Should generate summary"
        assert len(summary) > 0, "Summary should not be empty"
        logger.info(f"✓ Generated summary: {summary[:100]}...")
        
        # Test key sentence extraction
        logger.info("\nTesting key sentence extraction...")
        key_sentences = model.extract_key_sentences(long_text, num_sentences=3)
        assert len(key_sentences) > 0, "Should extract key sentences"
        logger.info(f"✓ Extracted {len(key_sentences)} key sentences")
        for i, sentence in enumerate(key_sentences, 1):
            logger.info(f"  {i}. {sentence[:80]}...")
        
        # Test similarity computation
        logger.info("\nTesting similarity computation...")
        text1 = "Machine learning is a subset of artificial intelligence."
        text2 = "AI includes machine learning as one of its subfields."
        text3 = "The weather is nice today."
        
        similarity_high = model.compute_similarity(text1, text2)
        similarity_low = model.compute_similarity(text1, text3)
        
        assert similarity_high > similarity_low, "Similar texts should have higher similarity"
        logger.info(f"✓ Similarity (related): {similarity_high:.4f}")
        logger.info(f"✓ Similarity (unrelated): {similarity_low:.4f}")
        
        logger.info("\n✓ All SSL Model tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ SSL Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """Test integration of PDF Reader and SSL Model."""
    logger.info("\n" + "=" * 50)
    logger.info("Testing Integration: PDF Reader + SSL Model")
    logger.info("=" * 50)
    
    try:
        from pdf_reader import PDFReader
        from ssl_model import SSLTextModel
        
        # Check if we can import reportlab
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            logger.warning("reportlab not installed, skipping integration test")
            logger.info("  Install with: pip install reportlab")
            return True
        
        # Create a test PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            test_pdf_path = tmp.name
        
        c = canvas.Canvas(test_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Integration Test Document")
        c.drawString(100, 730, "This document tests the integration of PDF reading")
        c.drawString(100, 710, "and SSL model summarization capabilities.")
        c.drawString(100, 690, "Machine learning is a method of data analysis that")
        c.drawString(100, 670, "automates analytical model building. It is a branch")
        c.drawString(100, 650, "of artificial intelligence based on the idea that")
        c.drawString(100, 630, "systems can learn from data and make decisions.")
        c.showPage()
        c.save()
        
        # Read PDF
        reader = PDFReader()
        content = reader.read_pdf(test_pdf_path)
        assert content is not None, "Should read PDF content"
        logger.info("✓ Read PDF content successfully")
        
        # Summarize with SSL model
        model = SSLTextModel(model_name="facebook/bart-large-cnn")
        summary = model.summarize(content, max_length=80, min_length=20)
        assert summary is not None, "Should generate summary from PDF"
        logger.info(f"✓ Generated summary from PDF: {summary}")
        
        # Extract key sentences
        key_sentences = model.extract_key_sentences(content, num_sentences=2)
        logger.info(f"✓ Extracted {len(key_sentences)} key sentences from PDF")
        
        # Clean up
        Path(test_pdf_path).unlink()
        
        logger.info("\n✓ Integration test passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    logger.info("\n" + "=" * 50)
    logger.info("SSL Model and PDF Reader Test Suite")
    logger.info("=" * 50 + "\n")
    
    results = {
        'PDF Reader': test_pdf_reader(),
        'SSL Model': test_ssl_model(),
        'Integration': test_integration()
    }
    
    # Print summary
    logger.info("\n" + "=" * 50)
    logger.info("Test Summary")
    logger.info("=" * 50)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("\n✓ All tests passed successfully!")
        return 0
    else:
        logger.error("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
