"""Собирает index.html из исходника трекера и публикует изменения.

Исходник лежит в рабочем проекте курса, здесь — только опубликованная копия.
Скрипт переносит файл и подставляет то, что нужно веб-версии: заголовок
вкладки, запрет индексации, описание, цвет темы и иконку.

Запуск:  python deploy.py            — собрать index.html
         python deploy.py --push     — собрать, закоммитить и отправить
"""
import io, subprocess, sys

ИСХОДНИК = r"C:\Projects\Ux-Ui design обучающий курс\Материалы\Модуль 7\Трекер исследования.html"
ЦЕЛЬ = "index.html"

ЗАГОЛОВОК = "Курс по UX/UI дизайну · Модуль 7"

МЕТАТЕГИ = """<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Трекер исследования перед проектом. Материал модуля 7 курса по UX/UI дизайну.">
<meta name="theme-color" content="#F4F6FC">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%232F6BFF'/%3E%3Cpath d='M9 16.5l4.5 4.5L23 11.5' stroke='white' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E">"""


def собрать():
    s = io.open(ИСХОДНИК, encoding="utf-8").read()
    начало = s.index("<title>")
    конец = s.index("</title>") + len("</title>")
    s = s[:начало] + "<title>" + ЗАГОЛОВОК + "</title>\n" + МЕТАТЕГИ + s[конец:]
    io.open(ЦЕЛЬ, "w", encoding="utf-8", newline="").write(s)
    print("index.html собран из исходника")


def отправить():
    subprocess.run(["git", "add", "-A"], check=True)
    статус = subprocess.run(["git", "status", "--porcelain"],
                            capture_output=True, text=True).stdout.strip()
    if not статус:
        print("изменений нет, отправлять нечего")
        return
    subprocess.run(["git", "commit", "-q", "-m", "Обновление трекера"], check=True)
    subprocess.run(["git", "push", "-q", "origin", "main"], check=True)
    print("отправлено, страница обновится через минуту-две")


if __name__ == "__main__":
    собрать()
    if "--push" in sys.argv:
        отправить()
