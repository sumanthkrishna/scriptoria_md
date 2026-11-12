from io import BytesIO
from zipfile import ZipFile
from utils.export_docx import export_docx
from utils.export_pptx import export_pptx

def test_docx_valid_package():
    data = export_docx("<h1>Section</h1><p>Body</p>", "Example")
    with ZipFile(BytesIO(data)) as archive:
        assert "word/document.xml" in archive.namelist()

def test_pptx_valid_package():
    data = export_pptx("<h1>Section</h1><p>Body</p>", "Example")
    with ZipFile(BytesIO(data)) as archive:
        assert "ppt/presentation.xml" in archive.namelist()
