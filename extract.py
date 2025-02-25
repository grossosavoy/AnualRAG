from pathlib import Path
from docling.document_converter import DocumentConverter,PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
    TableFormerMode,   
)
from docling_core.types.doc import ImageRefMode
import pandas as pd

def extract_text(source_pdf, output_folder="parsed"):
    pipeline_options = PdfPipelineOptions()
    accelerator_options = AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.AUTO
        )
    pipeline_options.accelerator_options = accelerator_options
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    pipeline_options.table_structure_options.do_cell_matching = True

    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    output_markdown = output_folder / "output.md"

    converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}) 
    result = converter.convert(source_pdf)

    for table_ix, table in enumerate(result.document.tables):
        table_df: pd.DataFrame = table.export_to_dataframe()
        print(f"## Table {table_ix}")
        print(table_df.to_markdown())

        # Save the table as csv
        element_csv_filename = output_folder / f"doc_filename-table-{table_ix+1}.csv"
        table_df.to_csv(element_csv_filename)

        # Save the table as html
        element_html_filename = output_folder / f"doc_filename-table-{table_ix+1}.html"
        print(f"Saving HTML table to {element_html_filename}")
        with element_html_filename.open("w") as fp:
            fp.write(table.export_to_html())

    if result and hasattr(result, "document") and result.document:
        result.document.save_as_markdown(output_markdown, strict_text=False, escaping_underscores=False, image_mode=ImageRefMode.PLACEHOLDER,
)
        print(f"✅ Markdown file saved at: {output_markdown}")
        return output_markdown
    else:
        print("❌ Error: Document conversion failed.")
        return None