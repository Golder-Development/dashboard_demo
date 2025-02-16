import streamlit as st

# Define a class for managing multiple pages in a Streamlit app


class MultiPage:

    def __init__(self, app_name) -> None:
        self.pages = []  # List to store the pages
        self.app_name = app_name  # Name of the app

        # Set the page configuration
        st.set_page_config(
            page_title=self.app_name,
            page_icon=":computer:"
        )

    # Method to add a new page to the app
    def add_page(self, title, func) -> None:
        self.pages.append({"title": title, "function": func})

    # Method to run the app
    def run(self):
        st.title(self.app_name)  # Display the app title
        page = st.sidebar.radio("Menu",
                                self.pages,
                                format_func=lambda page: page["title"])
        page["function"]()  # Run the selected page's function
