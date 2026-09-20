-- Воронка по шагам

SELECT event_type, COUNT(DISTINCT user_id)
FROM events
GROUP BY event_type
ORDER BY CASE event_type
	WHEN 'signup' THEN 1
	WHEN 'onboarding_done' THEN 2
	WHEN 'trial_start' THEN 3
	WHEN 'activation' THEN 4
END


-- Конверсия по шагам воронки

SELECT 
	event_type,
	COUNT(DISTINCT user_id),
	round(count(DISTINCT user_id)::NUMERIC / 
	LAG(COUNT(DISTINCT user_id)) OVER (
		ORDER BY CASE event_type 
		WHEN 'signup' THEN 1
		WHEN 'onboarding_done' THEN 2
		WHEN 'trial_start' THEN 3
		WHEN 'activation' THEN 4
	END	) * 100, 1) AS conversion_from_prev
FROM events 
GROUP BY event_type 
ORDER BY CASE event_type 
	WHEN 'signup' THEN 1
	WHEN 'onboarding_done' THEN 2
	WHEN 'trial_start' THEN 3
	WHEN 'activation' THEN 4
END


-- Когортный анализ (retention "сейчас", без учёта возраста когорты)
SELECT 
    DATE_TRUNC('month', u.signup_date) AS cohort_month,
    COUNT(DISTINCT u.id) AS cohort_size,
    COUNT(CASE WHEN s.status = 'active' THEN 1 END) AS active_users,
    ROUND(
        COUNT(CASE WHEN s.status = 'active' THEN 1 END)::numeric 
        / COUNT(DISTINCT u.id) * 100, 1
    ) AS active_pct
FROM users u
LEFT JOIN subscriptions s ON u.id = s.user_id
GROUP BY cohort_month
ORDER BY cohort_month ASC