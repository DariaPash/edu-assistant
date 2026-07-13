# EDU Assistant

A configurable LLM-powered assistant for education.

The assistant can answer questions about mathematics, history, and other subjects. You can choose an OpenAI-compatible cloud provider or a local Ollama model, configure the assistant's role, and select the desired response format.

[English](#english) · [Русский](#русский)

---

# English

## Features

* **Multiple LLM providers** — use an OpenAI-compatible API or run a model locally with Ollama.
* **Configurable assistant roles** — define separate instructions for a mathematics tutor, history tutor, or any other role.
* **Response templates** — generate either detailed explanations with exercises or short one-sentence answers.
* **Centralized configuration** — models, roles, prompts, timeouts, and output limits are stored in `config.yml`.
* **Configuration validation** — project settings are loaded and validated with Pydantic.
* **Simple Python interface** — generate an answer with a single `create_response()` call.
* **Environment-based secrets** — API keys are loaded from a local `.env` file.

## How it works

1. The application loads settings from `config.yml`.
2. It selects an LLM provider using `llm_key`.
3. It combines the selected role with a response template.
4. It sends the resulting system instructions and user prompt to the model.
5. It returns the generated answer as a string.

## Requirements

* Git
* [`uv`](https://docs.astral.sh/uv/)
* Python 3.14 or newer
* An API key for an OpenAI-compatible provider, or a locally running Ollama instance

## Installation

### 1. Install `uv`

Linux and macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, follow the installation instructions in the official `uv` documentation.

### 2. Clone the repository

```bash
git clone https://github.com/DariaPash/edu-assistant.git
cd edu-assistant
```

### 3. Install dependencies

```bash
uv sync
```

`uv` will create a virtual environment and install the dependencies from `pyproject.toml` and `uv.lock`.

## Environment configuration

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your-api-key
```

Do not commit `.env` or real API keys to the repository.

### Using a cloud API

Specify the provider's model and OpenAI-compatible endpoint in `config.yml`:

```yaml
llms:
  api:
    model: "your-model-name"
    base_url: "https://your-provider.example.com/v1/"
    timeout: 60
    max_output_tokens: 512
```

Then add the provider's token to `.env`:

```dotenv
OPENAI_API_KEY=your-real-api-key
```

### Using Ollama

Install Ollama and download the configured model:

```bash
ollama pull gemma3:1b
```

Start the Ollama server if it is not already running:

```bash
ollama serve
```

The default local configuration is:

```yaml
llms:
  ollama:
    model: "gemma3:1b"
    base_url: "http://localhost:11434/v1/"
    timeout: 60
    max_output_tokens: 512
```

The OpenAI Python client expects an API key even when the local Ollama server does not use authentication. Add any non-empty value to `.env`:

```dotenv
OPENAI_API_KEY=ollama
```

## Usage

Configure the request in `main.py`:

```python
from edu_assistant.assistant import create_response


def main() -> None:
    response = create_response(
        llm_key="api",
        role="math_tutor",
        template="tutor_quick_answer",
        prompt="What is a derivative?",
    )

    print(response)


if __name__ == "__main__":
    main()
```

Run the assistant:

```bash
uv run python main.py
```

To use Ollama, change the provider:

```python
llm_key="ollama"
```

## Request parameters

| Parameter  | Description                                     | Available default values                  |
| ---------- | ----------------------------------------------- | ----------------------------------------- |
| `llm_key`  | LLM configuration from `config.yml`             | `api`, `ollama`                           |
| `role`     | Assistant role and subject-specific instruction | `math_tutor`, `history_tutor`             |
| `template` | Response format                                 | `tutor_full_answer`, `tutor_quick_answer` |
| `prompt`   | User's question                                 | Any string                                |

## Configuration

All application settings are stored in `config.yml`.

### LLM providers

```yaml
llms:
  api:
    model: "gpt-5.4-nano"
    base_url: "https://llm.inzhenerka-cloud.com/"
    timeout: 60
    max_output_tokens: 512

  ollama:
    model: "gemma3:1b"
    base_url: "http://localhost:11434/v1/"
    timeout: 60
    max_output_tokens: 512
```

### Assistant roles

Each role contains a subject-specific system instruction:

```yaml
roles:
  math_tutor:
    instruction: |
      You are an enthusiastic mathematics teacher.
      Answer only questions related to mathematics.

  history_tutor:
    instruction: |
      You are a history teacher.
      Give concise and structured answers with dates.
```

### Response templates

Templates determine how the final answer should be structured:

```yaml
system_templates:
  tutor_full_answer: |
    {role_instruction}

    Response requirements:
    1. Explain the main idea in one or two sentences.
    2. Give a step-by-step explanation when appropriate.
    3. Provide two short exercises.
    4. Include answers to the exercises.

  tutor_quick_answer: |
    {role_instruction}

    Response requirements:
    1. Always answer in one concise sentence.
```

The `{role_instruction}` placeholder is replaced with the instruction of the selected role.

## Adding a new role

### 1. Add the role to `config.yml`

```yaml
roles:
  physics_tutor:
    instruction: |
      You are a physics teacher.
      Explain concepts using simple real-world examples.
```

### 2. Add the role name to `RoleType`

Update `src/edu_assistant/config.py`:

```python
type RoleType = Literal[
    "history_tutor",
    "math_tutor",
    "physics_tutor",
]
```

### 3. Use the new role

```python
response = create_response(
    llm_key="api",
    role="physics_tutor",
    template="tutor_full_answer",
    prompt="Explain Newton's second law.",
)
```

## Adding a new response template

### 1. Add the template to `config.yml`

```yaml
system_templates:
  tutor_with_examples: |
    {role_instruction}

    Explain the topic and provide three practical examples.
```

### 2. Add its name to `TemplateType`

Update `src/edu_assistant/config.py`:

```python
type TemplateType = Literal[
    "tutor_full_answer",
    "tutor_quick_answer",
    "tutor_with_examples",
]
```

## Project structure

```text
edu-assistant/
├── src/
│   └── edu_assistant/
│       ├── __init__.py
│       ├── assistant.py
│       ├── config.py
│       └── llm_client.py
├── .gitignore
├── config.yml
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

* `assistant.py` — builds the system instructions and sends the request to the LLM.
* `config.py` — loads and validates the YAML configuration.
* `llm_client.py` — creates an OpenAI-compatible client.
* `config.yml` — contains providers, roles, templates, and application settings.
* `main.py` — provides a minimal usage example.

---

# Русский

## Возможности

* **Несколько LLM-провайдеров** — можно использовать OpenAI-совместимое облачное API или локальную модель через Ollama.
* **Настраиваемые роли** — для учителя математики, истории или любого другого помощника можно задать отдельную системную инструкцию.
* **Шаблоны ответов** — ассистент может давать подробные объяснения с упражнениями или краткие ответы в одно предложение.
* **Единая конфигурация** — модели, роли, промпты, тайм-ауты и ограничения ответа хранятся в `config.yml`.
* **Проверка конфигурации** — настройки загружаются и валидируются с помощью Pydantic.
* **Простой Python-интерфейс** — для генерации ответа достаточно одного вызова `create_response()`.
* **Безопасное хранение секретов** — API-ключ загружается из локального файла `.env`.

## Как работает проект

1. Приложение загружает настройки из `config.yml`.
2. По значению `llm_key` выбирается LLM-провайдер.
3. Инструкция выбранной роли объединяется с шаблоном ответа.
4. Системная инструкция и вопрос пользователя отправляются модели.
5. Сгенерированный ответ возвращается в виде строки.

## Требования

* Git
* [`uv`](https://docs.astral.sh/uv/)
* Python 3.14 или новее
* API-ключ OpenAI-совместимого провайдера или локально запущенный Ollama

## Установка

### 1. Установите `uv`

Linux и macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Для Windows используйте инструкцию из официальной документации `uv`.

### 2. Склонируйте репозиторий

```bash
git clone https://github.com/DariaPash/edu-assistant.git
cd edu-assistant
```

### 3. Установите зависимости

```bash
uv sync
```

`uv` создаст виртуальное окружение и установит зависимости из `pyproject.toml` и `uv.lock`.

## Настройка окружения

Создайте файл `.env` в корне проекта:

```dotenv
OPENAI_API_KEY=ваш-api-ключ
```

Не добавляйте `.env` и настоящие API-ключи в репозиторий.

### Использование облачного API

Укажите модель и OpenAI-совместимый адрес провайдера в `config.yml`:

```yaml
llms:
  api:
    model: "название-модели"
    base_url: "https://your-provider.example.com/v1/"
    timeout: 60
    max_output_tokens: 512
```

Добавьте токен провайдера в `.env`:

```dotenv
OPENAI_API_KEY=ваш-настоящий-api-ключ
```

### Использование Ollama

Установите Ollama и загрузите модель, указанную в конфигурации:

```bash
ollama pull gemma3:1b
```

Запустите сервер Ollama, если он ещё не работает:

```bash
ollama serve
```

Конфигурация локальной модели по умолчанию:

```yaml
llms:
  ollama:
    model: "gemma3:1b"
    base_url: "http://localhost:11434/v1/"
    timeout: 60
    max_output_tokens: 512
```

Python-клиент OpenAI ожидает наличие API-ключа, даже если локальный Ollama не использует авторизацию. Поэтому добавьте в `.env` любое непустое значение:

```dotenv
OPENAI_API_KEY=ollama
```

## Использование

Настройте запрос в `main.py`:

```python
from edu_assistant.assistant import create_response


def main() -> None:
    response = create_response(
        llm_key="api",
        role="math_tutor",
        template="tutor_quick_answer",
        prompt="Что такое производная?",
    )

    print(response)


if __name__ == "__main__":
    main()
```

Запустите ассистента:

```bash
uv run python main.py
```

Для использования Ollama измените провайдера:

```python
llm_key="ollama"
```

## Параметры запроса

| Параметр   | Описание                                | Доступные значения по умолчанию           |
| ---------- | --------------------------------------- | ----------------------------------------- |
| `llm_key`  | Конфигурация модели из `config.yml`     | `api`, `ollama`                           |
| `role`     | Роль ассистента и предметная инструкция | `math_tutor`, `history_tutor`             |
| `template` | Формат ответа                           | `tutor_full_answer`, `tutor_quick_answer` |
| `prompt`   | Вопрос пользователя                     | Любая строка                              |

## Конфигурация

Все настройки приложения хранятся в `config.yml`.

### LLM-провайдеры

```yaml
llms:
  api:
    model: "gpt-5.4-nano"
    base_url: "https://llm.inzhenerka-cloud.com/"
    timeout: 60
    max_output_tokens: 512

  ollama:
    model: "gemma3:1b"
    base_url: "http://localhost:11434/v1/"
    timeout: 60
    max_output_tokens: 512
```

### Роли ассистента

Каждая роль содержит отдельную предметную инструкцию:

```yaml
roles:
  math_tutor:
    instruction: |
      Ты увлечённый учитель математики.
      Отвечай только на вопросы, связанные с математикой.

  history_tutor:
    instruction: |
      Ты учитель истории.
      Давай краткие структурированные ответы с датами.
```

### Шаблоны ответов

Шаблоны определяют структуру итогового ответа:

```yaml
system_templates:
  tutor_full_answer: |
    {role_instruction}

    Требования к ответу:
    1. Кратко объясни основную идею в одном-двух предложениях.
    2. Дай пошаговое объяснение, если это уместно.
    3. Приведи два небольших упражнения.
    4. Добавь ответы к упражнениям.

  tutor_quick_answer: |
    {role_instruction}

    Требования к ответу:
    1. Всегда отвечай кратко, одним предложением.
```

Вместо `{role_instruction}` автоматически подставляется инструкция выбранной роли.

## Добавление новой роли

### 1. Добавьте роль в `config.yml`

```yaml
roles:
  physics_tutor:
    instruction: |
      Ты учитель физики.
      Объясняй понятия на простых примерах из жизни.
```

### 2. Добавьте название роли в `RoleType`

Измените `src/edu_assistant/config.py`:

```python
type RoleType = Literal[
    "history_tutor",
    "math_tutor",
    "physics_tutor",
]
```

### 3. Используйте новую роль

```python
response = create_response(
    llm_key="api",
    role="physics_tutor",
    template="tutor_full_answer",
    prompt="Объясни второй закон Ньютона.",
)
```

## Добавление нового шаблона

### 1. Добавьте шаблон в `config.yml`

```yaml
system_templates:
  tutor_with_examples: |
    {role_instruction}

    Объясни тему и приведи три практических примера.
```

### 2. Добавьте его название в `TemplateType`

Измените `src/edu_assistant/config.py`:

```python
type TemplateType = Literal[
    "tutor_full_answer",
    "tutor_quick_answer",
    "tutor_with_examples",
]
```

## Структура проекта

```text
edu-assistant/
├── src/
│   └── edu_assistant/
│       ├── __init__.py
│       ├── assistant.py
│       ├── config.py
│       └── llm_client.py
├── .gitignore
├── config.yml
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

* `assistant.py` — формирует системную инструкцию и отправляет запрос модели.
* `config.py` — загружает и проверяет YAML-конфигурацию.
* `llm_client.py` — создаёт OpenAI-совместимый клиент.
* `config.yml` — содержит настройки провайдеров, ролей, шаблонов и приложения.
* `main.py` — содержит минимальный пример использования.
