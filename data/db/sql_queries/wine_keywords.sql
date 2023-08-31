SELECT
    wines.name AS wine_name,
    keywords_wine.count AS keyword_count,
    keywords.name AS keyword_name,
    group_concat(keywords.name) AS keyword_list,
	keywords_wine.group_name
FROM wines
JOIN keywords_wine ON keywords_wine.wine_id = wines.id
JOIN keywords  ON keywords.id = keywords_wine.keyword_id
WHERE 
    keyword_count > 10
GROUP BY wine_name
HAVING 
	keyword_list LIKE '%coffee%'
	AND	keyword_list LIKE '%toast%'
	AND	keyword_list LIKE '%green apple%'
	AND	keyword_list LIKE '%cream%'
	AND	keyword_list LIKE '%citrus%';
	
	