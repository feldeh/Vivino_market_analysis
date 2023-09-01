import streamlit as st


def run():
    st.set_page_config(
        page_title="Vivinio",
        page_icon="🍷",
    )

    st.markdown(
        """

        ## Vivino :wine_glass:

        ---

        #### A wine market analysis by:

        - **Felicien de Hertogh**
        - **Andreia Azevedo Heringer Negreira**
        - **George Hollingdale**

        ---

        As Junior Data Engineers/Analysts, we've been tasked by Vivino to analyse their database.

        We have come up with some useful statistics to help them with their marketing strategies, and to provide deeper knowledge of their products and users.

        Our findings are covered in this application.

        """
    )


if __name__ == "__main__":
    run()
