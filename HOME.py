import streamlit as st

# Define the pages
main_page = st.Page("Assinaturas.py", title="LOGIN", icon="🔐")
page_2 = st.Page("Modificação PCM.py", title="PCM", icon="⚙️")


# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()