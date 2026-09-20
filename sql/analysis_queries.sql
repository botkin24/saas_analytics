-- Задача 1: Воронка по шагам (абсолютные числа)
SELECT event_type, COUNT(DISTINCT user_id)
FROM events
GROUP BY event_type
ORDER BY CASE event_type
	WHEN 'signup' THEN 1
	WHEN 'onboarding_done' THEN 2
	WHEN 'trial_start' THEN 3
	WHEN 'activation' THEN 4
END


-- Задача 2: Конверсия по шагам воронки (% перехода от предыдущего шага, через LAG)
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


-- Задача 3а: Когортный анализ (retention "сейчас", без учёта возраста когорты)
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


-- Задача 3б (проверочный шаг): проверка вычисления возраста когорты в месяцах через AGE/EXTRACT
SELECT
	p.payment_date,
	u.signup_date,
	AGE(p.payment_date, u.signup_date) AS raw_age,
	EXTRACT(YEAR FROM age(p.payment_date, u.signup_date)) * 12 +
		EXTRACT(MONTH FROM age(p.payment_date, u.signup_date)) AS cohort_age_months
FROM payments p
JOIN subscriptions s ON p.subscription_id = s.id
JOIN users u ON s.user_id = u.id
LIMIT 10


-- Задача 3в (проверочный шаг): внутренность будущего CTE — платежи, помеченные когортой и возрастом
SELECT
    u.id AS user_id,
    DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
    (EXTRACT(YEAR FROM AGE(p.payment_date, u.signup_date)) * 12 +
     EXTRACT(MONTH FROM AGE(p.payment_date, u.signup_date)))::int AS cohort_age_months
FROM payments p
JOIN subscriptions s ON p.subscription_id = s.id
JOIN users u ON s.user_id = u.id
WHERE p.status = 'succeeded'


-- Задача 3г: Когортный retention по возрасту (CTE) — сколько юзеров платят на N-м месяце жизни в каждой когорте
WITH cohort_data AS (
    SELECT
        u.id AS user_id,
        DATE_TRUNC('month', u.signup_date)::date AS cohort_month,
        (EXTRACT(YEAR FROM AGE(p.payment_date, u.signup_date)) * 12 +
         EXTRACT(MONTH FROM AGE(p.payment_date, u.signup_date)))::int AS cohort_age_months
    FROM payments p
    JOIN subscriptions s ON p.subscription_id = s.id
    JOIN users u ON s.user_id = u.id
    WHERE p.status = 'succeeded'
)
SELECT
    cohort_month,
    cohort_age_months,
    COUNT(DISTINCT user_id) AS active_users
FROM cohort_data
GROUP BY cohort_month, cohort_age_months
ORDER BY cohort_month, cohort_age_months


-- Задача 4а: Помесячная выручка (только успешные платежи)
SELECT
    DATE_TRUNC('month', payment_date)::date AS payment_month,
    SUM(amount) AS monthly_revenue
FROM payments
WHERE status = 'succeeded'
GROUP BY DATE_TRUNC('month', payment_date)::date
ORDER BY payment_month;


-- Задача 4б: Помесячная выручка с накопительным итогом (SUM() OVER)
SELECT
    DATE_TRUNC('month', payment_date)::date AS payment_month,
    SUM(amount) AS monthly_revenue,
    SUM(SUM(amount)) OVER (
        ORDER BY DATE_TRUNC('month', payment_date)::date
    ) AS cumulative_revenue
FROM payments
WHERE status = 'succeeded'
GROUP BY DATE_TRUNC('month', payment_date)::date
ORDER BY payment_month;