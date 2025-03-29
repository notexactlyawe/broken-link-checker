import unittest
from unittest.mock import patch, MagicMock
import requests
from broken_links import extract_links


class TestExtractLinks(unittest.TestCase):
    @patch("broken_links.requests.get")
    def test_absolute_links(self, mock_get):
        """Test extraction of absolute http/https links"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="https://example.com">Example</a>
                <a href="http://test.com/page">Test</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        links = extract_links("https://example.org", "https://example.org")

        self.assertEqual(len(links), 2)
        self.assertIn("https://example.com", links)
        self.assertIn("http://test.com/page", links)

    @patch("broken_links.requests.get")
    def test_relative_links(self, mock_get):
        """Test extraction of relative links"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="/about">About</a>
                <a href="contact">Contact</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        links = extract_links("https://example.org/", "https://example.org/")

        self.assertEqual(len(links), 2)
        # Per current implementation, these are the expected URLs:
        self.assertIn("https://example.org/about", links)
        self.assertIn("https://example.org/contact", links)

    @patch("broken_links.requests.get")
    def test_invalid_links(self, mock_get):
        """Test handling of invalid links"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="">Empty</a>
                <a href="#">Hash</a>
                <a href="page#section">With Hash</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        links = extract_links("https://example.org/", "https://example.org/")

        # All these links are filtered out (empty or contain #)
        self.assertEqual(len(links), 0)

    @patch("broken_links.requests.get")
    def test_other_protocols(self, mock_get):
        """Test extraction of non-http protocol links"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="tel:+1234567890">Call</a>
                <a href="mailto:test@example.com">Email</a>
                <a href="ftp://example.com/file">FTP</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        links = extract_links("https://example.org/", "https://example.org/")

        self.assertEqual(len(links), 0)

    @patch("broken_links.requests.get")
    def test_request_error(self, mock_get):
        """Test handling of request errors"""
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        links = extract_links("https://example.org/", "https://example.org/")

        self.assertEqual(links, [])

    @patch("broken_links.requests.get")
    def test_non_200_response(self, mock_get):
        """Test handling of non-200 HTTP responses"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        links = extract_links("https://example.org/", "https://example.org/")

        self.assertEqual(links, [])


if __name__ == "__main__":
    unittest.main()
