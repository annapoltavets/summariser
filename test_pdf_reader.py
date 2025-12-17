"""
Test Script for PDF Reader

This script tests the PDF reading functionality without requiring heavy dependencies.
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


def test_pdf_reader_basic():
    """Test basic PDF reader functionality."""
    logger.info("=" * 50)
    logger.info("Testing PDF Reader - Basic Functionality")
    logger.info("=" * 50)
    
    try:
        from pdf_reader import PDFReader
        
        reader = PDFReader()
        logger.info("✓ PDFReader initialized successfully")
        
        # Test with non-existent file
        result = reader.read_pdf("non_existent.pdf")
        assert result is None, "Should return None for non-existent file"
        logger.info("✓ Correctly handles non-existent file")
        
        # Test with invalid file type
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            test_txt_path = tmp.name
            tmp.write(b"This is a text file")
        
        result = reader.read_pdf(test_txt_path)
        assert result is None, "Should return None for non-PDF file"
        logger.info("✓ Correctly handles non-PDF file")
        Path(test_txt_path).unlink()
        
        logger.info("\n✓ Basic PDF Reader tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ PDF Reader test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_reader_with_sample():
    """Test PDF reading with a sample PDF if reportlab is available."""
    logger.info("\n" + "=" * 50)
    logger.info("Testing PDF Reader - With Sample PDF")
    logger.info("=" * 50)
    
    try:
        from pdf_reader import PDFReader
        
        # Check if reportlab is available
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
        except ImportError:
            logger.warning("reportlab not installed, skipping PDF creation test")
            logger.info("  To run full tests, install: pip install reportlab")
            return True
        
        reader = PDFReader()
        
        # Create a simple test PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            test_pdf_path = tmp.name
        
        c = canvas.Canvas(test_pdf_path, pagesize=letter)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 730, "This is a test document for PDF reading.")
        c.drawString(100, 710, "It contains multiple lines of text.")
        c.drawString(100, 690, "Line 4 of the test document.")
        c.showPage()
        
        # Add second page
        c.drawString(100, 750, "Second Page")
        c.drawString(100, 730, "This is the second page of the document.")
        c.showPage()
        c.save()
        
        logger.info(f"Created test PDF: {test_pdf_path}")
        
        # Test reading the entire PDF
        content = reader.read_pdf(test_pdf_path)
        assert content is not None, "Should read PDF content"
        assert "Test PDF Document" in content, "Should contain expected text"
        assert len(content) > 50, "Should have substantial content"
        logger.info("✓ Successfully read PDF content")
        logger.info(f"  Content length: {len(content)} characters")
        
        # Test reading pages individually
        pages = reader.read_pdf_pages(test_pdf_path)
        assert pages is not None, "Should return list of pages"
        assert len(pages) == 2, "Should have 2 pages"
        assert "Test PDF Document" in pages[0], "First page should contain expected text"
        assert "Second Page" in pages[1], "Second page should contain expected text"
        logger.info(f"✓ Successfully read {len(pages)} pages individually")
        
        # Test metadata extraction
        metadata = reader.get_pdf_metadata(test_pdf_path)
        assert metadata is not None, "Should extract metadata"
        assert 'num_pages' in metadata, "Should have num_pages in metadata"
        assert metadata['num_pages'] == 2, "Should report 2 pages"
        logger.info("✓ Successfully extracted PDF metadata")
        logger.info(f"  Metadata: {metadata}")
        
        # Clean up
        Path(test_pdf_path).unlink()
        logger.info("✓ Cleaned up test file")
        
        logger.info("\n✓ PDF Reader with sample tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"✗ PDF Reader sample test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all PDF reader tests."""
    logger.info("\n" + "=" * 50)
    logger.info("PDF Reader Test Suite")
    logger.info("=" * 50 + "\n")
    
    results = {
        'Basic Functionality': test_pdf_reader_basic(),
        'Sample PDF': test_pdf_reader_with_sample()
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
        logger.info("\n✓ All PDF reader tests passed successfully!")
        return 0
    else:
        logger.error("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
