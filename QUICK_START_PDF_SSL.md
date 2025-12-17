# Quick Start Guide: PDF Reader and SSL Model

This guide helps you quickly get started with the new PDF reading and SSL (Self-Supervised Learning) model features.

## Installation

### Basic Installation (PDF Reader Only)
```bash
pip install PyPDF2 reportlab scikit-learn
```

### Full Installation (PDF Reader + SSL Model)
```bash
pip install PyPDF2 reportlab scikit-learn torch transformers
```

Note: torch and transformers are large packages (~2GB). Install only if you need SSL model features.

## Quick Examples

### 1. Read a PDF Document

```python
from pdf_reader import PDFReader

reader = PDFReader()

# Read entire PDF
text = reader.read_pdf("document.pdf")
print(text)

# Read by pages
pages = reader.read_pdf_pages("document.pdf")
for i, page in enumerate(pages, 1):
    print(f"Page {i}: {page[:100]}...")

# Get metadata
metadata = reader.get_pdf_metadata("document.pdf")
print(f"Pages: {metadata['num_pages']}")
print(f"Author: {metadata['author']}")
```

### 2. Use SSL Model for Text Summarization

```python
from ssl_model import SSLTextModel

# Initialize model
model = SSLTextModel(model_name="facebook/bart-large-cnn")

# Summarize text
long_text = "Your long text here..."
summary = model.summarize(long_text, max_length=150, min_length=50)
print(f"Summary: {summary}")

# Extract key sentences
key_sentences = model.extract_key_sentences(long_text, num_sentences=5)
for sentence in key_sentences:
    print(f"- {sentence}")

# Compute similarity
similarity = model.compute_similarity(text1, text2)
print(f"Similarity: {similarity:.4f}")
```

### 3. Combine PDF Reader with SSL Model

```python
from pdf_reader import PDFReader
from ssl_model import SSLTextModel

# Read PDF
reader = PDFReader()
content = reader.read_pdf("document.pdf")

# Summarize with SSL model
model = SSLTextModel()
summary = model.summarize(content, max_length=150)
print(f"PDF Summary: {summary}")
```

### 4. Integrate with Existing AI Summarizer

```python
from pdf_reader import PDFReader
from ai_summarizer import AISummarizer

# Requires OPENAI_API_KEY in .env
reader = PDFReader()
summarizer = AISummarizer()

content = reader.read_pdf("document.pdf")

system_prompt = "Summarize the following document concisely."
summary = summarizer.summarize(system_prompt, content)
print(summary)
```

## Running Tests

### Test PDF Reader (Fast, no heavy dependencies)
```bash
python test_pdf_reader.py
```

### Test SSL Model (Requires torch and transformers)
```bash
python test_ssl_model.py
```

### Run Interactive Demo
```bash
python demo_pdf_ssl.py
```

### Test with Your Own PDF
```bash
python pdf_summarizer_example.py your_document.pdf
```

## Common Use Cases

### Use Case 1: Extract and Summarize Research Papers
```python
from pdf_reader import PDFReader
from ssl_model import SSLTextModel

reader = PDFReader()
model = SSLTextModel()

# Read research paper
paper = reader.read_pdf("research_paper.pdf")

# Get summary
summary = model.summarize(paper, max_length=200)

# Extract key findings
key_points = model.extract_key_sentences(paper, num_sentences=5)
```

### Use Case 2: Compare Document Similarity
```python
from pdf_reader import PDFReader
from ssl_model import SSLTextModel

reader = PDFReader()
model = SSLTextModel()

doc1 = reader.read_pdf("document1.pdf")
doc2 = reader.read_pdf("document2.pdf")

similarity = model.compute_similarity(doc1, doc2)
print(f"Documents are {similarity*100:.1f}% similar")
```

### Use Case 3: Batch Process Multiple PDFs
```python
from pdf_reader import PDFReader
from ssl_model import SSLTextModel
from pathlib import Path

reader = PDFReader()
model = SSLTextModel()

pdf_dir = Path("pdfs/")
for pdf_file in pdf_dir.glob("*.pdf"):
    content = reader.read_pdf(str(pdf_file))
    summary = model.summarize(content)
    print(f"\n{pdf_file.name}:")
    print(summary)
```

## Troubleshooting

### Problem: "No module named 'torch'"
**Solution**: Install PyTorch
```bash
pip install torch
```

### Problem: "No module named 'transformers'"
**Solution**: Install Transformers
```bash
pip install transformers
```

### Problem: PDF reading returns None
**Solution**: Check that:
1. File path is correct
2. File exists
3. File is a valid PDF
4. You have read permissions

### Problem: SSL model is slow
**Solution**: 
- Use GPU if available (model automatically detects CUDA)
- Use a smaller model: `SSLTextModel(model_name="facebook/bart-base")`
- Process shorter text chunks

## Model Information

### Default SSL Model
- **Name**: facebook/bart-large-cnn
- **Type**: Sequence-to-Sequence Transformer
- **Parameters**: ~400M
- **Best for**: Summarization tasks

### Alternative Models
- **bart-base**: Smaller, faster (140M params)
- **t5-small**: Good for general tasks (60M params)
- **distilbart-cnn**: Lighter version (306M params)

To use a different model:
```python
model = SSLTextModel(model_name="facebook/bart-base")
```

## Performance Tips

1. **For PDF Reading**: No special optimization needed, very fast
2. **For SSL Model**:
   - First run downloads the model (one-time, ~1.6GB)
   - Use GPU for faster processing
   - Process documents in batches
   - Cache model instance, don't recreate

## Support

For issues or questions:
1. Check the test files for examples
2. Run the demo script: `python demo_pdf_ssl.py`
3. Review README.md for detailed documentation
4. Check GitHub issues

## What's Next?

Explore advanced features:
- Text embeddings for semantic search
- Custom summarization parameters
- Multi-document summarization
- Topic extraction
- Named entity recognition (extend the SSL model)

Happy coding! 🚀
