# SaaS Product Analytics

Сквозной учебный проект по продуктовой аналитике: от генерации данных до статистических выводов и A/B-тестирования. Цель — собрать в одном проекте полный цикл работы продуктового/дата-аналитика на реалистичном датасете SaaS-сервиса.

> 🚧 Проект в активной разработке. Ниже — честный статус по спринтам.

## Что внутри

Синтетический, но реалистичный датасет пользователей SaaS-продукта (каналы привлечения, тарифные планы, страны, даты регистрации и активности), сгенерированный с учётом реальных пропорций (доли каналов, конверсия по каналам в платные планы и т.д.) и загруженный в PostgreSQL.

## Стек

- **Python:** Pandas, NumPy, Matplotlib, Seaborn, Plotly, SciPy, Statsmodels, Scikit-learn, Faker
- **База данных:** PostgreSQL (SQLAlchemy, psycopg2)
- **Инструменты:** Jupyter, python-dotenv

## Структура репозитория

```
saas_analytics/
├── notebooks/
│   ├── 01_eda.ipynb          # EDA и подготовка данных
│   ├── 02_stats_tests.ipynb  # статистика и проверка гипотез
│   └── 03_ab_testing.ipynb   # A/B-тестирование
├── sql/
│   ├── schema.sql            # схема БД
│   └── analysis_queries.sql  # аналитические запросы
├── src/
│   ├── generate_data.py      # генерация синтетических данных
│   ├── load_data.py          # загрузка данных в PostgreSQL
│   └── db_connection.py      # подключение к БД
└── requirements.txt
```

## Статус по спринтам

- [x] **Sprint 1 — EDA:** генерация синтетических данных, загрузка в PostgreSQL, первичная проверка целостности и разведочный анализ
- [ ] **Sprint 2 — SQL и аналитические запросы:** ключевые продуктовые метрики (воронка, retention, LTV) на SQL
- [ ] **Sprint 3 — Статистика:** проверка гипотез, распределения, доверительные интервалы
- [ ] **Sprint 4 — A/B-тестирование:** дизайн эксперимента, расчёт мощности, интерпретация результатов

## Как запустить

```bash
git clone https://github.com/botkin24/saas_analytics.git
cd saas_analytics
pip install -r requirements.txt
# настроить переменные окружения для подключения к PostgreSQL (.env)
python src/generate_data.py
python src/load_data.py
```

## Автор

Максим Боткин — [Telegram](https://t.me/mbotkin) · [GitHub](https://github.com/botkin24)
