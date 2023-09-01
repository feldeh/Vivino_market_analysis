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

    return [row[0] for row in result]


# @st.cache_data
def fetch_wines(selected_keywords):
    # append HAVING condition for each selected keyword
    keyword_conditions = " AND ".join([f"keyword_list LIKE '%{keyword}%'" for keyword in selected_keywords])
    # append SUM of keyword count for each selected keyword
    keyword_counts = ", ".join([f"SUM(CASE WHEN keywords.name = '{keyword}' THEN keywords_wine.count ELSE 0 END) AS {keyword}_count" for keyword in selected_keywords])
    # append each selected keywords keyword count to ORDER BY clause
    order_by_keyword = ", ".join([f"{keyword}_count DESC" for keyword in selected_keywords])

    query = f"""
        SELECT
            wines.name AS wine_name,
            {keyword_counts},
            group_concat(CASE WHEN keywords_wine.keyword_type = 'primary' THEN keywords.name ELSE NULL END) AS keyword_list,
            keywords_wine.group_name
        FROM wines
        JOIN keywords_wine ON keywords_wine.wine_id = wines.id
        JOIN keywords ON keywords.id = keywords_wine.keyword_id
        WHERE
            keywords_wine.count > 10
        GROUP BY wine_name
        HAVING {keyword_conditions}
        ORDER BY {order_by_keyword};
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
        st.subheader(f"Total Matching Wines: {len(results)} :wine_glass:")

        for result in results:
            st.write(result[0])
            for keyword in selected_keywords:
                print(keyword)
                print(selected_keywords.index(keyword))
                keyword_index = selected_keywords.index(keyword) + 1
                st.write(f"{keyword} count:", result[keyword_index])
            st.write("---")


if __name__ == "__main__":
    main()
