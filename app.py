import streamlit as st
import requests

st.set_page_config(page_title="Resume Insight", layout="centered", page_icon="📄")

# --- Header Section ---
st.markdown("""
    <h1 style='text-align: center;'>📄 Resume Insight</h1>
    <p style='text-align: center; font-size: 18px;'>Upload your resume and get a smart score with deep insights.</p>
    <hr style="border: 0.5px solid #ccc;" />
""", unsafe_allow_html=True)

# --- Upload Section ---
uploaded_file = st.file_uploader("📤 Upload Resume (PDF Only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Analyzing resume..."):
        try:
            # ✅ LIVE BACKEND URL USED HERE
            res = requests.post(
                "https://resume-insight-backend.onrender.com/analyze/",
                files={"file": uploaded_file}
            )

            if res.status_code == 200:
                data = res.json()

                st.markdown("---")
                st.success("✅ Resume analyzed successfully!")

                # --- Layout in Columns ---
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**👤 Name:** `{data.get('name', 'N/A')}`")
                    st.markdown(f"**📧 Email:** `{data.get('email', 'N/A')}`")
                    st.markdown(f"**📱 Phone:** `{data.get('phone', 'N/A')}`")

                with col2:
                    st.markdown("**🎓 Education:**")
                    for edu in data.get("education", []):
                        st.markdown(f"- {edu}")

                # --- Projects Section ---
                st.markdown("### 💼 Projects")
                for p in data.get("projects", []):
                    st.markdown(f"- {p}")

                # --- Skills Section ---
                st.markdown("### 🧠 Skills Found")
                skills = data.get("skills_found", [])
                if skills:
                    st.markdown("✅ `" + "`, `".join(skills) + "`")
                else:
                    st.warning("No matching skills found!")

                # --- Score Section ---
                score = data.get("score", 0)
                st.markdown("### 📊 Resume Score")

                st.progress(score / 100)
                score_msg = f"🎯 Your Resume Score: **{score}/100**"

                if score >= 80:
                    st.success(score_msg + " — Excellent! 🔥")
                elif score >= 50:
                    st.warning(score_msg + " — Needs Improvement ⚠️")
                else:
                    st.error(score_msg + " — Too Low ❌")

            else:
                st.error("❌ Server Error: Unable to analyze resume.")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

else:
    st.info("👆 Upload a resume to begin.")
