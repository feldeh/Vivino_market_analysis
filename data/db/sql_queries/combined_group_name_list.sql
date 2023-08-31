SELECT 
    group_concat(DISTINCT group_name_list) AS combined_group_name_list
FROM (
    SELECT 
        keywords.name AS keyword_name,
        keyword_id,
        group_concat(DISTINCT group_name) AS group_name_list
    FROM keywords_wine
    JOIN keywords ON keywords.id = keywords_wine.keyword_id
    WHERE name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus')
    GROUP BY keyword_name, keyword_id
    ORDER BY keyword_name
);
