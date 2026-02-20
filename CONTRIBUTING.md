# Contributing to OpenCut

Thank you for your interest in contributing to OpenCut! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your operating system and Python version

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/OpenCut.git
cd OpenCut

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

## Code Style

- Follow PEP 8 style guidelines
- Write docstrings for functions and classes
- Keep functions focused and modular
- Add comments for complex logic

## Testing

Before submitting a PR:
- Test on your local machine
- Ensure the GUI works correctly
- Test the GIF export functionality
- Verify screen capture works

## Questions?

Feel free to open an issue for any questions!

## Code of Conduct

Be respectful and constructive in all interactions.
