## Тестовое задание по парсингу группы в Вконтакте: "vk_fishing"
## Test task to parse Vkontakte group: "vk_fishing"

### Результат находиться в папке [***photo_res***](https://github.com/Antirry/Test-Parsing-vk_fishing/tree/master/photo_res).
#### И файл с запросами -> [Тут](https://github.com/Antirry/Test-Parsing-vk_fishing/blob/master/project/Queries.py).
### Result can be found in the [***photo_res***](https://github.com/Antirry/Test-Parsing-vk_fishing/tree/master/photo_res) folder.
#### And the query file -> [here](https://github.com/Antirry/Test-Parsing-vk_fishing/blob/master/project/Queries.py).


Я использовал DBeaver для загрузки CSV файла
I used DBeaver to upload CSV file   
https://dbeaver.io/


Запросы для создания таблицы:
```SQL
CREATE DATABASE IF NOT EXISTS Group_Members ENGINE = Memory;

CREATE TABLE Group_Members.example_table
(
    `id` UInt32 NOT NULL,
    `fullname` String NOT NULL,
    `last_seen` datetime64,
    `town` String,
    `contacts` String,
    `friends_count` UInt16
)
ENGINE = MergeTree()
PRIMARY KEY (id)
ORDER BY (id);

```