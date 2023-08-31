import streamlit as st
import sqlite3
from pathlib import Path

db_path = Path.cwd() / 'data' / 'db' / 'vivino.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


@st.cache_data
def fetch_primary_keywords():
    all_primary_keywords_query = """
        SELECT DISTINCT keywords.name
        FROM keywords_wine
        JOIN keywords ON keywords.id = keywords_wine.keyword_id
        WHERE keyword_type = 'primary' AND keywords_wine.count > 10
    """
    cursor.execute(all_primary_keywords_query)
    result = cursor.fetchall()
    print('result:', result, 'fetch_primary_keywords END')

    return [row[0] for row in result]


# @st.cache_data
def fetch_wines(selected_keywords):
    keyword_conditions = " AND ".join([f"keyword_list LIKE '%{keyword}%'" for keyword in selected_keywords])
    query = f"""
        SELECT
            wines.name AS wine_name,
            keywords_wine.count AS keyword_count,
            keywords.name AS keyword_name,
            group_concat(CASE WHEN keywords_wine.keyword_type = 'primary' THEN keywords.name ELSE NULL END) AS keyword_list,
            keywords_wine.group_name,
            keywords_wine.keyword_type
        FROM wines
        JOIN keywords_wine ON keywords_wine.wine_id = wines.id
        JOIN keywords ON keywords.id = keywords_wine.keyword_id
        WHERE
            keyword_count > 10
        GROUP BY wine_name
        HAVING {keyword_conditions};
    """
    cursor.execute(query)
    return cursor.fetchall()


def main():
    st.title("Wine keyword search")

    primary_keywords = fetch_primary_keywords()

    selected_keywords = st.multiselect("Select primary keywords", primary_keywords)

    if not selected_keywords:
        st.warning("Please select at least one primary keyword")
        return

    results = fetch_wines(selected_keywords)

    if not results:
        st.warning("No wines found matching the selected keywords")
    else:
        st.subheader("Matching wines :wine_glass::")
        for result in results:
            st.write("**Wine name:**", result[0])
            st.write("Keyword count:", result[1])
            st.write("Primary keywords:", result[2])
            st.write("All keywords:", result[3])
            st.write("Group name:", result[4])
            st.write("Keyword type:", result[5])
            st.write("---")


if __name__ == "__main__":
    main()
