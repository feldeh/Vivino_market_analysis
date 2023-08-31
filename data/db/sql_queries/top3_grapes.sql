SELECT 
	grapes.name AS grape_name,
	grapes.id AS grapes_id,
	sum(most_used_grapes_per_country.wines_count) AS global_wine_count
FROM grapes
JOIN most_used_grapes_per_country ON most_used_grapes_per_country.grape_id = grapes_id
GROUP BY grape_id
ORDER BY global_wine_count 
DESC
LIMIT 3;
