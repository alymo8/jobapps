import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS))
HAS_FITZ = importlib.util.find_spec("fitz") is not None


@unittest.skipUnless(HAS_FITZ, "PyMuPDF not installed")
class PreviewPngTest(unittest.TestCase):
    def test_preview_goes_to_temp_dir_per_posting(self):
        import build_resume

        name = "Acme-test-preview-png"
        folder = Path(tempfile.gettempdir()) / "jobapps-preview" / name
        shutil.rmtree(folder, ignore_errors=True)
        self.addCleanup(shutil.rmtree, folder, True)

        pdf = Path("postings") / name / "the user_Resume_Acme.pdf"
        png = build_resume.preview_png(pdf)

        self.assertEqual(png, folder / "the user_Resume_Acme.png")
        self.assertTrue(folder.is_dir())


if __name__ == "__main__":
    unittest.main()
