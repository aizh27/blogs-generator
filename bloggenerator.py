import streamlit as st
import google.generativeai as genai
from streamlit_extras.stylable_container import stylable_container

# Configure Gemini API
genai.configure(api_key="AIzaSyCYu6e6CpC2IjFChKIXbws1gDv0-SOukOg")

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# App Title
st.set_page_config(page_title="AI Blog Generator", layout="centered")
st.title("📝 AI Blog Generator (Gemini Powered)")
st.markdown("Generate full blogs from a single prompt using Google Gemini AI.")

# Input Section
with st.form("blog_form"):
    prompt = st.text_input("Enter your blog idea (One-liner):", placeholder="e.g., How AI is changing classrooms")
    tone = st.selectbox("Choose the Tone of Writing:", ["Professional", "Friendly", "Inspirational", "Casual", "Humorous"])
    num_lines = st.slider("Blog Length (in approx. lines):", 5, 50, 15)
    key_points = st.text_area("Any points/keywords to include? (Optional)", placeholder="e.g., Include ChatGPT, NEP 2020")

    submitted = st.form_submit_button("Generate Blog")

# Generation Logic
if submitted and prompt:
    with st.spinner("Generating blog using Gemini..."):
        blog_prompt = (
            f"Write a blog post on: '{prompt}'. "
            f"Tone: {tone}. "
            f"Length: around {num_lines} lines. "
        )
        if key_points:
            blog_prompt += f"Include these points: {key_points}."

        try:
            response = model.generate_content(blog_prompt)
            blog_content = response.text

            # Display in Modal using stylable_container
            with stylable_container(
                key="modal",
                css="""
                    {
                        border: 2px solid #eee;
                        padding: 2rem;
                        border-radius: 1rem;
                        background-color: #f9f9f9;
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
                    }
                """
            ):
                st.subheader("🖋️ Generated Blog")
                st.write(blog_content)
                st.download_button("📄 Download Blog as TXT", blog_content, file_name="generated_blog.txt")

        except Exception as e:
            st.error(f"❌ Failed to generate blog: {e}")
else:
    st.info("👆 Please enter a prompt and click 'Generate Blog'.")
