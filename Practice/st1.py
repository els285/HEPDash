import streamlit as st



st.title("Streamlit Tests")

if st.button("click this button"):
	st.write("YES")
else: 
	st.write("NO")


if st.checkbox("Display Name"):
	st.write("Ethan L Simpson")
else:
	st.write("CAZ")	