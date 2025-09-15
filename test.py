import json
import os
from difflib import get_close_matches
import streamlit as st

DATA_FILE = "books.json"

def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

st.title("📚 Book Manager")

menu = st.sidebar.radio(
    "menu",
    [
        "📥 Add Book",
        "🗑 Remove Book",
        "✏️ Edit Book",
        "🔍 Search",
        "🔢 Sort",
        "📊 Report",
        "🤝 Recommend",
        "📜 Show All"
    ]
)

if menu == "📥 Add Book":
    st.header("Add a New Book")
    with st.form("add_form", clear_on_submit=True):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year", step=1, format="%d")
        pages = st.number_input("Pages", step=1, format="%d")
        submit = st.form_submit_button("➕ Add")
    if submit:
        books = load_books()
        books.append({"title": title, "author": author, "year": int(year), "pages": int(pages)})
        save_books(books)
        st.success("✅ Book added successfully.")

elif menu == "🗑 Remove Book":
    st.header("Remove a Book")
    books = load_books()
    if books:
        titles = [b["title"] for b in books]
        choice = st.selectbox("Select book to remove:", titles)
        if st.button("🗑️ Remove"):
            new_books = [b for b in books if b["title"] != choice]
            save_books(new_books)
            st.success("Book removed.")
    else:
        st.info("No books available.")

elif menu == "✏️ Edit Book":
    st.header("Edit Book Info")
    books = load_books()
    if books:
        titles = [b["title"] for b in books]
        sel = st.selectbox("Select book to edit:", titles)
        book = next(b for b in books if b["title"] == sel)
        with st.form("edit_form"):
            new_title = st.text_input("Title", book["title"])
            new_author = st.text_input("Author", book["author"])
            new_year = st.number_input("Year", value=book["year"], step=1, format="%d")
            new_pages = st.number_input("Pages", value=book["pages"], step=1, format="%d")
            submit = st.form_submit_button("💾 Save")
        if submit:
            book.update({
                "title": new_title,
                "author": new_author,
                "year": int(new_year),
                "pages": int(new_pages),
            })
            save_books(books)
            st.success("✅ Book updated.")
    else:
        st.info("No books to edit.")

elif menu == "🔍 Search":
    st.header("Search Books")
    keyword = st.text_input("Enter keyword (title or author):")
    if keyword:
        books = load_books()
        results = [b for b in books if keyword.lower() in b["title"].lower()
                   or keyword.lower() in b["author"].lower()]
        if results:
            st.subheader("Results")
            st.table(results)
        else:
            st.warning("❌ No results found.")

elif menu == "🔢 Sort":
    st.header("Sort Books")
    books = load_books()
    if books:
        option = st.radio("Sort by:", ["Year", "Pages", "Title"])
        if option == "Year":
            sorted_books = sorted(books, key=lambda b: b["year"])
        elif option == "Pages":
            sorted_books = sorted(books, key=lambda b: b["pages"])
        else:
            sorted_books = sorted(books, key=lambda b: b["title"].lower())
        st.table(sorted_books)
    else:
        st.info("No books available.")

elif menu == "📊 Report":
    st.header("Summary Report")
    books = load_books()
    if books:
        total = len(books)
        avg_pages = sum(b["pages"] for b in books) / total
        max_book = max(books, key=lambda b: b["pages"])
        min_year = min(books, key=lambda b: b["year"])
        max_year = max(books, key=lambda b: b["year"])
        st.write(f"**Total books:** {total}")
        st.write(f"**Average pages:** {avg_pages:.2f}")
        st.write(f"**Most pages:** {max_book['title']} ({max_book['pages']} pages)")
        st.write(f"**Oldest book:** {min_year['title']} ({min_year['year']})")
        st.write(f"**Newest book:** {max_year['title']} ({max_year['year']})")
    else:
        st.info("No books available.")

elif menu == "🤝 Recommend":
    st.header("Recommend a Book")
    keyword = st.text_input("Enter a title or author you liked:")
    if keyword:
        books = load_books()
        if not books:
            st.info("No books to recommend.")
        else:
            author_matches = [b for b in books if keyword.lower() in b["author"].lower()]
            if author_matches:
                st.subheader("Based on Author")
                st.table(author_matches)
            else:
                titles = [b["title"] for b in books]
                close_matches = get_close_matches(keyword, titles, n=5, cutoff=0.3)
                if close_matches:
                    st.subheader("Based on Similar Titles")
                    st.table([next(b for b in books if b["title"] == m) for m in close_matches])
                else:
                    st.warning("No recommendations found.")

elif menu == "📜 Show All":
    st.header("All Books")
    books = load_books()
    if books:
        st.table(books)
    else:
        st.info("No books available.")
