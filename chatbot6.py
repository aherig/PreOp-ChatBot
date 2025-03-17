import streamlit as st
from fuzzywuzzy import fuzz

# Define chatbot responses using pairs
pairs = [
    ("Should heparin be ordered for open inguinal hernia cases?", "Heparin should not be ordered or given for open inguinal hernia cases."),
    ("Do open inguinal hernia cases need heparin?", "Do not order or give heparin for open inguinal hernia cases."),
    ("Do I give heparin for open inguinal hernia cases?", "Do not order or give heparin for open inguinal hernia cases."),
    ("Should heparin be ordered for hybrid cases?", "Heparin should not be ordered for hybrid cases."),
    ("Do hybrid cases need heparin?", "Do not order or give heparin for hybrid cases."),
    ("Do vascular cases need heparin?", "Do not order or give heparin for vascular cases."),
    ("Should heparin be ordered for vascular cases?", "Heparin should not be ordered for vascular cases."),
    ("Do hybrid/vascular cases need heparin?", "Do not order or give heparin for hybrid/vascular cases."),
    ("Should heparin be ordered for hybrid/vascular cases?", "Heparin should not be ordered for hybrid/vascular cases."),
    ("Do partial nephrectomy cases need heparin?", "Do not order or give heparin for partial nephrectomy cases."),
    ("Should heparin be ordered for partial nephrectomy cases?", "Heparin should not be ordered for partial nephrectomy cases."),
    ("Do PD cath placement cases need heparin?", "Do not order or give heparin for PD cath placement cases."),
    ("Should heparin be ordered for PD cath placement cases?", "Heparin should not be ordered for PD cath placement cases."),
# Drs that do not want heparin pulled or given
    ("Which Dr's don't want me to pull or give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Which doctors don't want me to pull or give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Does Dr Moritz want me to give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Does Dr Talluri want me to give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Does Dr Parsee want me to give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Does Dr Chu want me to give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Does Dr Al Masri want me to give heparin?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Moritz patients?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Talluri patients?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Parsee patients?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Chu patients?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Al Masri patients?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Moritz cases?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Talluri cases?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Parsee cases?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Chu cases?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Do I order heparin for Al Masri cases?", "The Dr's that want heparin ordered but don't want you to pull or give it are Moritz, Talluri, Parsee, and Chu/Al Masri."),
# Refer to protocol for heparin guidelines
    ("Do I order heparin for a cholecystectomy?", "For laprascopic or open cholecystectomy please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for Cholecystectomy cases?", "For laprascopic or open cholecystectomy please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for cholecystectomies?", "For laprascopic or open cholecystectomy please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a appendectomy?", "For laprascopic or open appendectomy please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for appendectomy cases?", "For laprascopic or open appendectomy please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for appendectomies?", "For laprascopic or open appendectomy please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a hiatal hernia?", "For laprascopic or open hiatal hernia please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for hiatal hernia cases?", "For laprascopic or open hiatal hernia please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for hiatal hernias?", "For laprascopic or open hiatal hernia please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a incisional hernia of abdomen?", "For laprascopic or open incisional hernia of abdomen please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for incisional hernia of abdomen cases?", "For laprascopic or open incisional hernia of abdomen please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for incisional hernia of abdomen?", "For laprascopic or open incisional hernia of abdomen please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for an umbilical hernia?", "For laprascopic or open umbilical hernia please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for umbilical hernia cases?", "For laprascopic or open umbilical hernia please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for umbilical hernias?", "For laprascopic or open umbilical hernia please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a VATS procedure?", "For a VATS procedure please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for VATS procedures?", "For a VATS procedure please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for VATS procedures?", "For a VATS procedure please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a lobectomy?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for lobectomy cases?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for lobectomies?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a wedge resection?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for wedge resection cases?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for wedge resections?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a lung resection?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for lung resection cases?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for lung resections?", "For laprascopic or open lobectomy/wedge resection/lung resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a colectomy?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for colectomy cases?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for colectomies?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a op lap?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for op lap cases?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for op laps?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a ex lap?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for ex lap cases?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for ex laps?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a bowel resection?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for bowel resection cases?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for bowel resections?", "For laprascopic or open colectomy/op lap/ex lap/bowel resection please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a total nephrectomy?", "For laprascopic or open total nephrectomy please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for total nephrectomy cases?", "For laprascopic or open total nephrectomy please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for total nephrectomies?", "For laprascopic or open total nephrectomy please refer to specific guidelines when ordering protocol."),
    ("Do I order heparin for a sacrocolpopexy?", "For laprascopic or open sacrocolpopexy please refer to specific guidelines when ordering protocol unless accompanied by a gyne surgery or a sling."),
    ("Should heparin be ordered for sacrocolpopexy cases?", "For laprascopic or open sacrocolpopexy please refer to specific guidelines when ordering protocol unless accompanied by a gyne surgery or a sling."),
    ("Do I give heparin for total sacrocolpopexies?", "For laprascopic or open sacrocolpopexy please refer to specific guidelines when ordering protocol unless accompanied by a gyne surgery or a sling."),
    ("Do I order heparin for a laparascopic inguinal hernia?", "For a laparascopic inguinal hernia please refer to specific guidelines when ordering protocol."),
    ("Should heparin be ordered for laparascopic inguinal hernia cases?", "For a laparascopic inguinal hernia please refer to specific guidelines when ordering protocol."),
    ("Do I give heparin for laparascopic inguinal hernias?", "For a laparascopic inguinal hernia please refer to specific guidelines when ordering protocol."),
# Indocyanin Green (ICG) Dye cheat sheet
    ("How do I reconstitute indocyanine green dye?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How do I reconstitute ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How do I reconstitute indocyanine green dye?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How much sterile water do I reconstitute ICG with?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("When do I administer ICG dye?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("Where is the sterile water I mix with the ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("Where do I find the sterile water mixed with ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("Do I need to do a flush after I give ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How much saline do I flush with after I administer ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How much reconstituted ICG do I give?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How many ml of indocyanine green do I administer?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("how many ml of ICG do I administer?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How much indocyanine green dye do I give?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How many mg ICG do I give?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How long prior to a procedure do I give ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How much time before a procedure do I need to give ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
    ("How long before a procedure do I need to administer ICG?", "Indocyanine green dye comes in a vial that contains 25mg. Reconstitute with 10ml sterile water. Sterile water is in the same pyxis drawer as the dye. Administer 6.5mg or roughly 2.5ml of reconstituted dye. Follow administration of dye with 10-12ml saline flush. Usually given 30-45 minutes prior to cholecystectomy."),
# IV placement restrictions
    ("Where do I put an IV for an anterior total hip?", "For an anterior total hip place the IV on the opposite side of the surgery."),
    ("Which side does the IV for an anterior total hip procedure go?", "For an anterior total hip place the IV on the opposite side of the surgery."),
    ("Are there restrictions for IV placement with anterior total hip procedure?", "For an anterior total hip place the IV on the opposite side of the surgery."),
    ("Where should I put an IV for an anterior total hip?", "For an anterior total hip procedure place the IV on the opposite side of the surgery."),
    ("Where do I put an IV for a hip arthroscopy?", "For a hip arthroscopy procedure place the IV on the opposite side of the surgery."),
    ("Which side does the IV for a hip arthroscopy procedure go?", "For a hip arthroscopy procedure place the IV on the opposite side of the surgery."),
    ("Are there restrictions for IV placement with a hip arthroscopy procedure?", "For a hip arthroscopy procedure place the IV on the opposite side of the surgery."),
    ("Where should I put an IV for a hip arthroscopy?", "For a hip arthroscopy procedure place the IV on the opposite side of the surgery."),
    ("Where do I put an IV for a posterior total hip?", "For a posterior total hip procedure place the IV on the same side of the surgery."),
    ("Which side does the IV for a posterior total hip procedure go?", "For a posterior total hip procedure place the IV on the same side of the surgery."),
    ("Are there restrictions for IV placement with a posterior total hip procedure?", "For a posterior total hip procedure place the IV on the same side of the surgery."),
    ("Where should I put an IV for a posterior total hip?", "For a posterior total hip procedure place the IV on the same side of the surgery."),
    ("Where do I put an IV for a colonoscopy?", "For a colonoscopy place the IV on the right side."),
    ("Which side does the IV for a colonoscopy go?", "For a colonoscopy place the IV on the right side."),
    ("Are there restrictions for IV placement for a colonoscopy?", "For a colonoscopy place the IV on the right side."),
    ("Where should I put an IV for a colonoscopy?", "For a colonoscopy place the IV on the right side.")
]

# Function to find the best match based on similarity
def get_best_response(user_input, pairs, threshold=70):
    best_match = None
    highest_score = 0
    
    for pattern, response in pairs:
        similarity = fuzz.ratio(user_input.lower(), pattern.lower())
        
        if similarity > highest_score and similarity >= threshold:
            highest_score = similarity
            best_match = response

    return best_match if best_match else "I'm not sure how to respond to that."

# Streamlit App UI
st.markdown("<h1 style='color: blue; text-align: center;'>PreOp ChatBot</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; color: gray; text-align: center;'>Ask your preop-related questions below:</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("<h2 style='color: red;'>Chatbot Troubleshooting</h2>", unsafe_allow_html=True)
st.sidebar.write("✅ For commonly asked preop questions.")
st.sidebar.write("✅ Mispelled words can result in wrong response.")
st.sidebar.write("✅ More specific questions will get best results.")

# User input
user_input = st.text_input("")

if st.button("Ask"):
    if user_input:
        st.markdown(f"<p style='color: green; font-size:18px;'><b>You:</b> {user_input}</p>", unsafe_allow_html=True)
        response = get_best_response(user_input, pairs, threshold=65)
        st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:10px;'>"
                    f"<b>PreOpBot:</b> {response}</div>", unsafe_allow_html=True)
