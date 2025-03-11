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
    ("Which Dr's don't want me to pull or give heparin?", "The Dr's that don't want you to pull or give heparin are Moritz, Talluri, Parsee, and Chu/Al Masri."),
    ("Which doctors don't want me to pull or give heparin?", "The Dr's that don't want you to pull or give heparin are Moritz, Talluri, Parsee, and Chu/Al Masri."),
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
st.title("Medical Chatbot")
st.write("Ask a medical-related question below:")

# User input
user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        response = get_best_response(user_input, pairs, threshold=65)
        st.write("**Chatbot:**", response)
