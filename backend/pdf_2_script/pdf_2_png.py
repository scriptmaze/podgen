import fitz
import os

def create_output_folder(pdf_path, base_output_folder):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    output_folder = os.path.join(base_output_folder, pdf_name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    return output_folder

def convert_pdf_to_png(pdf_path, base_output_folder):
    output_folder = create_output_folder(pdf_path, base_output_folder)
    
    document = fitz.open(pdf_path)
    
    for page_num in range(document.page_count):
        page = document.load_page(page_num)  
        
        pix = page.get_pixmap(dpi=300)
        
        output_image_path = f"{output_folder}/page_{page_num + 1}.png"
        pix.save(output_image_path)
        print(f"Saved {output_image_path}")
