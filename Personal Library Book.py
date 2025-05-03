import streamlit as st
import pandas as pd
import os

# File to store the book data
BOOKS_FILE = "library.csv"

# Load data from CSV
def load_books():
    if os.path.exists(BOOKS_FILE):
        return pd.read_csv(BOOKS_FILE)
    else:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Year"])

# Save data to CSV
def save_books(books_df):
    books_df.to_csv(BOOKS_FILE, index=False)

# Initialize
st.set_page_config(page_title="📚 Personal Library Manager")
st.title("📚 Personal Library Book Manager")

# Load current book list
books = load_books()

# --- Add a Book ---
st.header("➕ Add a New Book")
with st.form("add_book_form"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.text_input("Year Published")
    submitted = st.form_submit_button("Add Book")

    if submitted:
        if title and author and genre and year:
            new_book = pd.DataFrame([[title, author, genre, year]],
                                    columns=["Title", "Author", "Genre", "Year"])
            books = pd.concat([books, new_book], ignore_index=True)
            save_books(books)
            st.success(f"✅ '{title}' added to your library!")
        else:
            st.error("❌ Please fill in all fields.")

# --- View Book List ---
st.header("📖 Your Book Collection")
if not books.empty:
    st.dataframe(books)
else:
    st.info("Your library is empty. Add some books!")

# --- Delete a Book ---
st.header("🗑️ Delete a Book")
book_to_delete = st.selectbox("Select a book to delete", books["Title"].tolist() if not books.empty else [])

if st.button("Delete Book"):
    if book_to_delete:
        books = books[books["Title"] != book_to_delete]
        save_books(books)
        st.success(f"✅ '{book_to_delete}' has been deleted.")
    else:
        st.warning("No book selected.")

