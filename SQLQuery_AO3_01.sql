-- Starting with just looking at one of our tables
SELECT * from dbo.worksData_01;

-- Now, we want to get relevant data from our tables when grouping creation_date together
SELECT
	dbo.worksData_01.creation_date,
	COUNT(*) as number_of_works,
	SUM(dbo.worksData_01.word_count) as total_number_of_words
FROM dbo.worksData_01
GROUP BY dbo.worksData_01.creation_date
ORDER BY dbo.worksData_01.creation_date;

SELECT
	dbo.worksData_02.creation_date,
	COUNT(*) as number_of_works,
	SUM(dbo.worksData_02.word_count) as total_number_of_words
FROM dbo.worksData_02
GROUP BY dbo.worksData_02.creation_date
ORDER BY dbo.worksData_02.creation_date;

SELECT
	dbo.worksData_03.creation_date,
	COUNT(*) as number_of_works,
	SUM(dbo.worksData_03.word_count) as total_number_of_words
FROM dbo.worksData_03
GROUP BY dbo.worksData_03.creation_date
ORDER BY dbo.worksData_03.creation_date;

SELECT
	dbo.worksData_04.creation_date,
	COUNT(*) as number_of_works,
	SUM(dbo.worksData_04.word_count) as total_number_of_words
FROM dbo.worksData_04
GROUP BY dbo.worksData_04.creation_date
ORDER BY dbo.worksData_04.creation_date;

--We have independently saved the results as csv files to be used by Jupyter Notebooks later
