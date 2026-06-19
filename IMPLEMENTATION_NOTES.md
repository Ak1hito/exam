# Заметки по реализации вариантов

Шаблон в репозитории реализует **products** и **events**. Ниже — что нужно
учесть при адаптации под другие варианты билета (например, `employees` и
`posts`). Здесь собраны именно «грабли», на которых легко потерять баллы.

## 1. Поля DATE (`hire_date`, `published_at`) — уже обработаны

`setup_form_fields` в `exam/forms.py` отдельно обрабатывает `DateField`
(`type="date"` + явный формат `%Y-%m-%d`), так что нативный календарь и
префилл на редактировании работают из коробки.

Почему это важно (и почему нельзя просто полагаться на `else`): при локали
`ru-ru` `DATE_INPUT_FORMATS = ['%d.%m.%Y', ...]`, а нативный
`<input type=date>` принимает только `%Y-%m-%d`. Без явного формата значение
существующей записи рендерилось бы как `%d.%m.%Y` и **поле оказывалось бы
пустым** при редактировании.

Нюанс реализации: `DateTimeField` проверяется **до** `DateField`, потому что
`DateTimeField` — его подкласс (иначе `isinstance(..., DateField)` поймал бы
и datetime-поля).

## 2. Значения по умолчанию для дат — передавать callable

`published_at DATE, по умолчанию сегодня`:

```python
from datetime import date

published_at = models.DateField("Дата публикации", default=date.today)  # без ()!
```

`default=date.today()` (со скобками) зафиксирует дату **на момент запуска
процесса**, а не «сегодня» в момент создания записи.

## 3. Проверка «не в будущем» — сравнивать с датой, а не datetime

Для `DateField` сравнивайте с `date.today()`, а не с `timezone.now()`
(это datetime — получите ошибку сравнения типов):

```python
def clean(self):
    errors = {}
    if self.hire_date and self.hire_date > date.today():
        errors["hire_date"] = "Дата не может быть в будущем."
    if errors:
        raise ValidationError(errors)
```

(Для `event_date`/`published_at` в виде `DateTimeField` остаётся
`timezone.now()`, как в текущем `Event`.)

## 4. email: уникальность + наличие `@`

Берите `EmailField` — он даёт встроенную проверку формата (включая `@`),
а `unique=True` — уникальность. Ошибка дубликата всплывёт в форме сама
(ModelForm проверяет `unique`), отдельный код не нужен.

```python
email = models.EmailField("Email", max_length=100, unique=True)
```

## 5. Числовые поля: «больше 0» vs «не отрицательное»

* `salary > 0`, `max_guests > 0` — обычный `DecimalField`/`IntegerField`
  + проверка в `clean()`.
* `views` «не может быть отрицательным» (0 допустим) — это ровно
  `PositiveIntegerField`, дополнительная валидация не нужна.

## 6. Что уже работает «из коробки» (менять не нужно)

* **`DateField`** (`hire_date`, `published_at`) — `setup_form_fields` даёт
  `type="date"` и формат `%Y-%m-%d` (см. п.1).
* **`BooleanField`** (`is_published`) — `setup_form_fields` вешает
  `form-check-input`, а `form.html` рендерит чекбокс отдельной веткой.
* **`TextField`** (`content`) — ModelForm сам подставляет `<textarea>`,
  ветка `else` лишь добавляет класс `form-control`.
* **404** на несуществующей записи — дают дженерик-вьюхи.
* **HTTP 400** при невалидной форме — `FormStatusMixin`.

## 7. Не забыть про шаблоны и поля

* `created_at` (`auto_now_add=True`) **не включать** в `Meta.fields` формы.
* Списочные шаблоны (`*_list.html`) и колонки таблицы — под новые имена
  полей (`full_name`, `position`, `title`, `views`, …).
* В `*_list.html` булево поле удобно показывать как «Да/Нет»:
  `{{ post.is_published|yesno:"Да,Нет" }}`.
</content>
</invoke>
