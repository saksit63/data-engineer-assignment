WITH sales_rank AS (
	SELECT 
		pc.product_class_name,
		RANK() OVER(PARTITION BY pc.product_class_name ORDER BY SUM(st.quantity * pd.retail_price) DESC, SUM(st.quantity)) AS rank,
		pd.product_name,
		SUM(st.quantity * pd.retail_price) AS sales_value
	FROM Sales_Transaction AS st
	JOIN Product AS pd
	ON st.product_id = pd.product_id
	JOIN Product_Class AS pc
	ON pd.product_class_id = pc.product_class_id
	GROUP BY 1, 3
)

SELECT 
    *
FROM sales_rank
WHERE RANK <= 2
ORDER BY 1,2
;
