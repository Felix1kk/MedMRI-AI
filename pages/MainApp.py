
import streamlit as st
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image as RLImage, Spacer, PageBreak
import google.generativeai as genai
import io

def main_app():
  if not st.session_state.get("logged_in", False):
        st.error("Unauthorized access. Please log in.")
        st.session_state["page"] = "Login"
        st.rerun()

  st.title("Top G MedMRI AI ☢️")
  st.subheader(f"Welcome, {st.session_state.get('username', 'User')}!")

  # Add the brain tumor detection functionality here.

  def create_pdf(report_texts, images):
      buffer = io.BytesIO()
      doc = SimpleDocTemplate(buffer, pagesize=letter)
      elements = []
      styles = getSampleStyleSheet()
      title_style = ParagraphStyle(name='Title', fontSize=24, leading=28, spaceAfter=12, alignment=1)
      elements.append(Paragraph("MRI Analysis Report", title_style))
      elements.append(Spacer(1, 24))
      normal_style = ParagraphStyle(name='Normal', fontSize=14, leading=18, spaceAfter=12)

      for i, (report_text, image_data) in enumerate(zip(report_texts, images)):
          elements.append(Paragraph(f"Image {i + 1}", normal_style))
          image = Image.open(io.BytesIO(image_data['data']))
          image_path = f"/tmp/temp_image_{i}.png"
          image.save(image_path)
          elements.append(RLImage(image_path, width=4 * inch, height=4 * inch))
          elements.append(Spacer(1, 12))
          bullet_points = report_text.split('\n')
          for point in bullet_points:
              if point.startswith('- '):
                  point = point[2:]
                  elements.append(Paragraph(f'• {point}', normal_style))
              else:
                  elements.append(Paragraph(point, normal_style))
          elements.append(Spacer(1, 24))
          if i < len(report_texts) - 1:
              elements.append(PageBreak())
      doc.build(elements)
      buffer.seek(0)
      return buffer

  # Set up the generative AI model (Add this section based on your existing setup)

  gemini_api_key = st.secrets["gemini"]["api_key"]
  #API_KEY = 'AIzaSyAyGrTbjkU6cGEVSOZB5z4E044GuNY4Z-Q'
  MODEL_NAME = 'gemini-1.5-flash'

  # Sophisticated Prompt
  INPUT_PROMPT = """
  You are an expert radiologist with vast experience in interpreting medical imaging, particularly MRI scans of the human body. You will receive input MRI images from different anatomical regions, and your role is to analyze these images and provide detailed and accurate findings.  

  For each MRI image:  
  1. Identify the anatomical region (e.g., brain, spine, abdomen, pelvis, cardiac, joints, or whole body).  
  2. Describe any notable features, patterns, abnormalities, or structures visible in the image.  
  3. Focus on identifying potential pathologies, such as tumors, lesions, cysts, inflammation, degeneration, or any unusual findings.  
  4. Use clear, clinical terminology in your description (e.g., 'hyperintense lesions', 'abnormal mass', 'degenerative changes').  
  5. If applicable, suggest possible conditions or diagnoses that align with the findings (e.g., 'The observed mass in the liver may suggest hepatocellular carcinoma').  
  6. Include observations about the size, shape, texture, or location of the findings relative to anatomical landmarks.  

  For brain MRIs, pay particular attention to structures like the cerebrum, cerebellum, brainstem, ventricles, and cortical regions.  
  For spinal MRIs, analyze the vertebral discs, spinal cord, nerve roots, and spinal canal.  
  For cardiac MRIs, assess the heart chambers, valves, and blood flow patterns.  
  For joint MRIs, focus on cartilage, ligaments, tendons, and joint spaces.  

  Output your findings in a concise bullet-point format for clarity. Avoid speculation and focus only on what can be observed in the image.  

  """

  # Set up the generative AI model
  try:
      genai.configure(api_key=gemini_api_key)
      model = genai.GenerativeModel(MODEL_NAME)
  except Exception as e:
      st.error(f"Error configuring the model: {e}")

  # Functions
  def get_gemini_response(input_text, images, prompt):
      try:
          responses = []
          for image in images:
              response = model.generate_content([input_text, image, prompt])
              responses.append(response.text)
          return responses
      except Exception as e:
          st.error(f"Error generating content: {e}")
          return None

  def input_image_setup(uploaded_files):
      if uploaded_files:
          image_parts = [
              {
                  "mime_type": uploaded_file.type,
                  "data": uploaded_file.getvalue()
              }
              for uploaded_file in uploaded_files
          ]
          return image_parts
      else:
          raise FileNotFoundError("No files uploaded")

  # Streamlit App
  #st.header("Top G Brain Tumor App 🧠")

  uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

  if uploaded_files:
      for uploaded_file in uploaded_files:
          image = Image.open(uploaded_file)
          st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True)

  input_text = st.text_input("Input prompt:", key="input")

  submit = st.button("Analyze MRI Images")

  if submit:
      if not uploaded_files:
          st.info("Please upload at least one image")
      else:
        with st.spinner("Analyzing images, please wait..."):
          try:
              image_data = input_image_setup(uploaded_files)
              responses = get_gemini_response(input_text, image_data, INPUT_PROMPT)
              if responses:
                  st.subheader("The Responses are")
                  for i, response in enumerate(responses):
                      st.write(f"Response for Image {i+1}:")
                      st.write(response)

                  # Generate and provide the PDF download
                  pdf_buffer = create_pdf(responses, image_data)
                  st.download_button(
                      label="Download Report as PDF",
                      data=pdf_buffer,
                      file_name="MRI_analysis_report.pdf",
                      mime="application/pdf"
                  )
          except FileNotFoundError as e:
              st.error(f"File not found: {e}")
          except Exception as e:
              st.error(f"An unexpected error occurred: {e}")
