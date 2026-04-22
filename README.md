# Real Estate Valuation

Полное описание проекта: от структуры репозитория и ролей каждого файла до пошагового алгоритма расчёта (подготовка выборки, валидация, подбор регуляризации, оценка метрик, интерпретация и вывод результата).

---

## 1) Что делает проект

Проект оценивает удельную стоимость недвижимости с помощью ridge-регрессии для модели:

\[
V = \beta \cdot S + \alpha \cdot Q
\]

где:
- `V` — цена объекта,
- `S` — площадь дома,
- `Q` — площадь участка,
- `β` и `α` — искомые коэффициенты.

Используются априорные значения (`beta_prior`, `alpha_prior`) и регуляризация `λ`.

---

## 2) Пайплайн вычислений (от данных до результата)

Ниже — фактический поток текущей реализации.

1. **Загрузка/ввод данных на фронтенде**
   Пользователь выбирает источник (файл или ручной ввод), вводит априоры и режим `auto_lambda` либо ручное `lambda_value`.

2. **Формирование запроса к API**
   Frontend отправляет `POST /calculate` с массивом объектов `properties`.

3. **API-валидация**
   Проверяется:
   - положительность цены/площадей;
   - минимум 5 наблюдений;
   - если `auto_lambda=false`, то `lambda_value` обязателен и > 0.

4. **Разделение train/test и LOOCV**
   В текущей версии **нет отдельного фиксированного train/test split** как отдельного шага хранения выборок по файлам; вместо этого применяется **LOOCV (leave-one-out)** на всех наблюдениях: каждое наблюдение по очереди служит «мини-тестом», остальные — «мини-тренировкой». Это и является механизмом оценки обобщающей способности при малом объёме данных.

5. **Подбор λ**
   - `auto_lambda=true`: берётся фиксированная сетка значений λ и выбирается минимум LOOCV-MSE.
   - `auto_lambda=false`: используется одно заданное `lambda_value`.

6. **Финальная оценка коэффициентов**
   После выбора `lambda_star` модель обучается на полном наборе наблюдений.

7. **Метрики и неопределённость**
   Считаются `RMSE`, `MAE`, `MAPE`, `R²`, средний остаток, доверительные интервалы 95% для коэффициентов.

8. **Интерпретация и визуализация**
   Формируется текстовая интерпретация (поведение модели, влияние регуляризации, ограничения), и всё выводится в UI и экспортируется в отчёт.

---

## 3) Архитектура

- **Backend (`backend/src`)** — чистая слоистая архитектура:
  - `presentation` (HTTP/API),
  - `application` (use-case, DTO, валидация, orchestration),
  - `domain` (математика и бизнес-логика),
  - `infrastructure` (DI, логирование, отчёты, чтение файлов).
- **Frontend (`frontend/src`)** — React + TypeScript UI.

---

## 4) Файлы проекта и что в них происходит

> Ниже перечислены файлы репозитория и их назначение.

### Корень репозитория

- `README.md` — этот документ: архитектура, пайплайн, карта файлов.
- `LICENSE` — лицензия проекта.
- `package.json` — корневые npm-скрипты/зависимости монорепо.
- `package-lock.json` — lock-файл зависимостей npm.

### Backend: конфигурация и входные точки

- `backend/__init__.py` — маркер python-пакета backend.
- `backend/pyproject.toml` — конфигурация Python-проекта (линтеры/форматтеры и т.п.).
- `backend/requirements.txt` — Python-зависимости backend.

### Backend: слой presentation

- `backend/src/presentation/__init__.py` — пакет presentation.
- `backend/src/presentation/main.py` — старт FastAPI-приложения, подключение роутов/middleware.
- `backend/src/presentation/health.py` — health-check endpoint.

#### API
- `backend/src/presentation/api/__init__.py` — пакет API.
- `backend/src/presentation/api/routes.py` — endpoint `POST /calculate`, вызов use-case, HTTP-ошибки.
- `backend/src/presentation/api/schemas.py` — Pydantic-схемы request/response и правила валидации API.
- `backend/src/presentation/api/mappers.py` — преобразование API-схем ↔ application DTO.
- `backend/src/presentation/api/dependencies.py` — DI-зависимости FastAPI.
- `backend/src/presentation/api/exception_handlers.py` — централизованные обработчики исключений.

#### Middleware
- `backend/src/presentation/api/middleware/correlation_middleware.py` — correlation-id для трассировки запроса.
- `backend/src/presentation/api/middleware/logging_middleware.py` — логирование HTTP-запросов/ответов.

### Backend: слой application

- `backend/src/application/__init__.py` — пакет application.

#### DTO
- `backend/src/application/dto/__init__.py` — пакет DTO.
- `backend/src/application/dto/calculate_input.py` — входной DTO расчёта (`properties`, priors, `auto_lambda`, `lambda_value`).
- `backend/src/application/dto/calculate_result.py` — выходной DTO с параметрами, метриками, CV-кривой, диагностикой, интерпретацией.

#### Use case
- `backend/src/application/use_cases/__init__.py` — пакет use_cases.
- `backend/src/application/use_cases/calculate_ridge_use_case.py` — сценарий расчёта: валидировать вход и вызвать сервис.

#### Validators
- `backend/src/application/validators/__init__.py` — пакет validators.
- `backend/src/application/validators/calculate_validator.py` — бизнес-валидация входных данных (минимум наблюдений, положительность, ручной λ).

#### Services
- `backend/src/application/services/__init__.py` — пакет services.
- `backend/src/application/services/ridge_application_service.py` — главный оркестратор математики: подготовка матриц, LOOCV, выбор λ, финальный фит, метрики и интерпретация.

#### Mappers
- `backend/src/application/mappers/__init__.py` — пакет mappers.
- `backend/src/application/mappers/input_mapper.py` — преобразование входного DTO в доменные модели.
- `backend/src/application/mappers/result_mapper.py` — преобразование доменного результата в выходной DTO.

#### Factories
- `backend/src/application/factories/__init__.py` — пакет factories.
- `backend/src/application/factories/gamma_strategy_factory.py` — выбор стратегии регуляризации (авто/ручная).

#### Ports
- `backend/src/application/ports/__init__.py` — пакет ports.
- `backend/src/application/ports/property_reader_port.py` — абстракция чтения входных данных.
- `backend/src/application/ports/report_generator_port.py` — абстракция генерации отчёта.

### Backend: слой domain

- `backend/src/domain/__init__.py` — пакет domain.
- `backend/src/domain/exceptions.py` — доменные исключения.

#### Модели
- `backend/src/domain/models/__init__.py` — пакет моделей.
- `backend/src/domain/models/property.py` — сущность объекта недвижимости.
- `backend/src/domain/models/regression_data.py` — контейнер набора наблюдений.
- `backend/src/domain/models/ridge_prior.py` — априорные параметры модели.
- `backend/src/domain/models/ridge_parameters.py` — структура коэффициентов `β`, `α`.
- `backend/src/domain/models/regression_result.py` — итоговый доменный результат регрессии.

#### Сервисы (математика)
- `backend/src/domain/services/__init__.py` — пакет сервисов.
- `backend/src/domain/services/matrix_builder.py` — построение матриц признаков/цели.
- `backend/src/domain/services/ridge_solver.py` — решение ridge-системы линейной алгебры.
- `backend/src/domain/services/gamma_strategy.py` — стратегии выбора регуляризации.
- `backend/src/domain/services/ridge_estimator.py` — оценка ridge-параметров на доменном уровне.
- `backend/src/domain/services/metrics.py` — расчёт метрик качества.
- `backend/src/domain/services/uncertainty_estimator.py` — оценка неопределённости параметров (SE/CI).
- `backend/src/domain/services/model_interpreter.py` — формирование текстовой интерпретации результата.

### Backend: слой infrastructure

- `backend/src/infrastructure/__init__.py` — пакет infrastructure.

#### DI / config
- `backend/src/infrastructure/di/container.py` — сборка зависимостей и контейнер приложения.
- `backend/src/infrastructure/config/__init__.py` — пакет конфигурации.
- `backend/src/infrastructure/config/settings.py` — настройки окружения/backend.

#### Logging
- `backend/src/infrastructure/logging/__init__.py` — пакет логирования.
- `backend/src/infrastructure/logging/logger.py` — конфигурация логгера.
- `backend/src/infrastructure/logging/json_formatter.py` — JSON-формат логов.
- `backend/src/infrastructure/logging/context.py` — контекстные поля логирования.

#### Readers
- `backend/src/infrastructure/readers/__init__.py` — пакет readers.
- `backend/src/infrastructure/readers/base_reader.py` — базовая абстракция чтения данных.
- `backend/src/infrastructure/readers/csv_reader.py` — чтение CSV.
- `backend/src/infrastructure/readers/excel_reader.py` — чтение Excel.

#### Reporting
- `backend/src/infrastructure/reporting/__init__.py` — пакет reporting.
- `backend/src/infrastructure/reporting/excel_report_generator.py` — генерация Excel-отчёта с итогами модели.

### Frontend: конфигурация

- `frontend/README.md` — локальный README фронтенда.
- `frontend/package.json` — npm-зависимости и скрипты frontend.
- `frontend/package-lock.json` — lock-файл frontend.
- `frontend/tsconfig.json` — базовый TS-конфиг.
- `frontend/tsconfig.app.json` — TS-конфиг приложения.
- `frontend/tsconfig.node.json` — TS-конфиг node-инструментов.
- `frontend/vite.config.ts` — конфигурация Vite.
- `frontend/eslint.config.js` — правила ESLint.
- `frontend/postcss.config.js` — PostCSS-конфиг.
- `frontend/tailwind.config.js` — Tailwind-конфиг.
- `frontend/index.html` — HTML-шаблон Vite.
- `frontend/public/vite.svg` — публичный ассет.

### Frontend: исходный код

- `frontend/src/main.tsx` — вход React-приложения.
- `frontend/src/App.tsx` — корневой компонент приложения.
- `frontend/src/App.css` — стили App.
- `frontend/src/index.css` — глобальные стили.
- `frontend/src/assets/react.svg` — иконка/ассет.

#### API / types / utils / hooks
- `frontend/src/api/httpClient.ts` — HTTP-клиент (axios).
- `frontend/src/api/ridgeApi.ts` — функции API-вызовов (`/calculate`, отчёт).
- `frontend/src/types/apiTypes.ts` — типы запроса/ответа API.
- `frontend/src/utils/normalizeError.ts` — нормализация ошибок для UI.
- `frontend/src/hooks/useRidgeCalculation.ts` — хук выполнения расчёта с `loading/error`.

#### Страницы и UI-компоненты
- `frontend/src/pages/HomePage.tsx` — главная страница: сбор входа, запуск расчёта, рендер панелей результата.
- `frontend/src/components/DataSourceSelector.tsx` — выбор источника данных.
- `frontend/src/components/FileUpload.tsx` — загрузка файла с объектами.
- `frontend/src/components/ManualTableInput.tsx` — ручной ввод таблицы объектов.
- `frontend/src/components/PriorInput.tsx` — ввод априорных `β0`, `α0`.
- `frontend/src/components/GammaSelector.tsx` — выбор режима регуляризации (`auto`/ручной λ).
- `frontend/src/components/ResultsPanel.tsx` — основные параметры/итоги модели.
- `frontend/src/components/ReliabilityPanel.tsx` — блок надёжности/неопределённости.
- `frontend/src/components/QualityPanel.tsx` — визуализация качества модели.
- `frontend/src/components/AnalysisPanel.tsx` — аналитика и дополнительные вычисления по результату.
- `frontend/src/components/InterpretationPanel.tsx` — текстовая интерпретация и выводы.
- `frontend/src/components/MetricsCard.tsx` — карточка метрик.
- `frontend/src/components/PriceChart.tsx` — график цен/оценок.
- `frontend/src/components/ErrorBoundary.tsx` — перехват ошибок рендера.

---

## 5) Где именно считаются train/test-аспекты, метрики и выводы

- **Аспект train/test через LOOCV:**
  `backend/src/application/services/ridge_application_service.py` — для каждого объекта формируется «тест» из 1 наблюдения, остальные `n-1` используются как «train», считаются предсказания и MSE по каждой λ.

- **Выбор лучшей λ:**
  `backend/src/application/services/ridge_application_service.py` + `backend/src/presentation/api/schemas.py` (режим авто/ручной).

- **Финальные коэффициенты и метрики:**
  `backend/src/application/services/ridge_application_service.py`, а также доменные `metrics.py`/`uncertainty_estimator.py` для специализированных расчётов.

- **Формирование итогового ответа API:**
  `backend/src/application/dto/calculate_result.py` + `backend/src/presentation/api/mappers.py` + `backend/src/presentation/api/schemas.py`.

- **Показ результатов на UI:**
  `frontend/src/pages/HomePage.tsx` и компоненты `ResultsPanel`, `ReliabilityPanel`, `QualityPanel`, `AnalysisPanel`, `InterpretationPanel`.

---

## 6) Кратко о запуске

1. Backend:
   - установить зависимости из `backend/requirements.txt`,
   - запустить FastAPI-приложение через `backend/src/presentation/main.py`.
2. Frontend:
   - `npm install` в `frontend`,
   - `npm run dev` (или `npm run build` для production-сборки).

---

Если нужно, могу дополнительно сделать вторую версию README в формате «файл → вход/выход → ключевые функции → пример payload/response» для ещё более технической документации.
